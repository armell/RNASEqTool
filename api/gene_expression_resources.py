import os
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import stream_with_context, Response, request
from werkzeug.utils import secure_filename
import werkzeug

from pymysql import IntegrityError
from playhouse.shortcuts import *
from entities import datasets_rep as dr
from entities import experiments_rep as ex
from entities import identifier_generator as ig
from entities import processing_rep as pr
from entities import methods_rep as mr
from analysis.descriptive import sample_statistics as dp
from api import content_representations as cr
from visualization import expression_charts as nc
from transfer import expression_transfer_objects as eto
from analysis import expression_data as ed
from config import APP_CONFIG
import pandas as pd
from sklearn.preprocessing import scale


class Stream(restful.Resource):
    def get(self, taskId=None):
        print(taskId)
        mining_task = pr.get_mining_task(taskId)

        return Response(stream_with_context(
            ed.stream_detect_outliers_in_data(mining_task.dataset.public_identifier,
                                              mining_task.method.public_identifier,
                                              max_samples=mining_task.min_samples, min_dist=mining_task.min_distance,
                                              mining_id=mining_task.id)), content_type="application/json")


experiment_parser = reqparse.RequestParser()
experiment_parser.add_argument('linked_datasets', type=str, action='append')
experiment_parser.add_argument('unlinked_datasets', type=str, action='append')
experiment_parser.add_argument('public_identifier', type=str)
experiment_parser.add_argument('description', type=str)
experiment_parser.add_argument('type', type=str)

class Experiments(restful.Resource):
    def get(self):
        experiments = ex.get_experiments_all()
        return cr.JsonResource(eto.ExperimentsView(experiments).to_json())

    def post(self):
        args = experiment_parser.parse_args()
        res = ex.create_experiment(args.public_identifier, args.description, args.type)

        return cr.JsonResource(res.public_identifier)



class Experiment(restful.Resource):
    # TODO refactor get method
    def get(self, experimentId):
        # should not occur
        if experimentId.startswith("http://"):
            experimentId = experimentId.rsplit('/', 1)

        experiment = ex.get_experiment_by_identifier(experimentId)
        #print(experiment)
        return cr.JsonResource(eto.ExperimentView(experiment).to_json())


    def put(self, experimentId):
        args = experiment_parser.parse_args()
        datasets_to_attach = args.linked_datasets
        datasets_to_release = args.unlinked_datasets

        print(datasets_to_attach)

        for d in datasets_to_attach:
            ex.link_dataset_to_experiment(experimentId, d)

        return cr.StringApiResource("Datasets were attached"), 200


    def delete(self, experimentId):
        pass


class Methods(restful.Resource):
    def get(self):
        query = [eto.MethodView(e).to_json() for e in mr.get_list_of_methods()]

        return cr.JsonResource(query), 200


    def post(self):
        pass


class Method(restful.Resource):
    def get(self, methodId, package=None):
        if package == "all":
            query = [eto.PackageView(e, "method/" + methodId).to_json() for e in
                     mr.get_list_of_packages_by_method(methodId)]
        # TODO unique package

        return cr.JsonResource(query), 200

    def put(self, methodId, packages=None):
        pass

    def delete(self, methodId, packages=None):
        pass


chart_parser = reqparse.RequestParser()
chart_parser.add_argument("gene_set", type=str, action="append")
chart_parser.add_argument("analysis_type", type=str)
chart_parser.add_argument("dataset_identifier", type=str)
chart_parser.add_argument("zscore_values", type=bool)
chart_parser.add_argument("chart_type", type=str)
chart_parser.add_argument("experiment_identifier", type=str)
chart_parser.add_argument("sample_set", type=str, action="append")


class Charts(restful.Resource):
    def get(self):
        pass


    def post(self):
        args = chart_parser.parse_args()
        selected_genes = args["gene_set"]
        selected_dataset = args["dataset_identifier"]
        selected_charttype = args["chart_type"]
        print args["chart_type"]

        request_to_handle = request.accept_mimetypes.best_match(['application/pdf', 'text/html'])

        if request_to_handle == 'application/pdf':
            accept = "pdf"
        else:
            accept = "html"

        chart_resource = nc.sample_distribution_for_genes(selected_dataset, selected_genes,
                                                          title=selected_dataset,
                                                          chart_type=selected_charttype,
                                                          chart_rendering=accept)

        # returns the write rendering based on generator [bokeh with bokehjs or matplot with mpld3]
        if accept == "html":
            if chart_resource["generator"] == "bokeh":
                return cr.BokehResource(chart_resource["chart"]), 201
            if chart_resource["generator"] == "matplot":
                return cr.MatPlotLibResource(chart_resource["chart"]), 201

        if accept == "pdf":
            filename = ig.get_generated_guid_as_string() + ".pdf"
            file_path = APP_CONFIG["domain"] + APP_CONFIG["static_documents"]
            chart_resource["chart"].savefig("." + APP_CONFIG["static_documents"] + filename)
            return cr.StringApiResource(file_path + filename), 201


class Chart(restful.Resource):
    def get(selfself, chartId):
        pass

    def put(self, chartId):
        pass

    def delete(self, chartId):
        pass

# TODO map it to preprocessing entity
dataset_parser = reqparse.RequestParser()
dataset_parser.add_argument("dataset_identifier", type=str)
dataset_parser.add_argument("target_dataset_identifier", type=str)
dataset_parser.add_argument("experiment_identifier", type=str)
dataset_parser.add_argument("preprocessing_action", type=str)
dataset_parser.add_argument("preprocessing_method_identifier", type=str)
dataset_parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files')
dataset_parser.add_argument("separator", type=str)
dataset_parser.add_argument("index", type=int)
dataset_parser.add_argument("dataset_type", type=str)


class Datasets(restful.Resource):
    def get(self):
        datasets = dr.get_all_datasets()
        transfer_datasets = []
        for d in datasets:
            transfer_datasets.append(eto.DatasetView(d).to_json())

        return cr.JsonResource(transfer_datasets)


    def post(self):
        args = dataset_parser.parse_args()
        print("dataset post received")
        # upload new dataset
        if args.dataset_identifier is None:
            print("creating new data set")
            new_file = args.file

            filename = secure_filename(new_file.filename)
            print("uploaded" + filename)
            intern_identifier = ig.get_generated_guid_as_string()
            new_file.save(filename)

            try:
                with open(filename, "rb") as fl:
                    frame = dr.get_data_frame_from_csv(fl)

                    intern_location = dr.store_data_frame_to_hdf(frame, intern_identifier)
                    # raw counts by default
                    data_entity = dr.create_data_set(intern_identifier,
                                                     public_identifier=filename,
                                                     dataset_type="raw gene counts",
                                                     experiment_identifier="raw_data_container")  # For demo -> add exp identifier
                    server_hash = ig.md5_for_file(fl)
                print(filename + " is saved")
                os.remove(filename)
                print("file removed")
                return cr.JsonResource(
                    {"filename": filename, "intern_identifier": data_entity.intern_identifier,
                     "public_identifier": data_entity.public_identifier, "server_md5": server_hash}), 201
            except IntegrityError:
                return cr.StringApiResource("Public identifier already taken"), 409
            except:
                return cr.StringApiResource("An error has occured, check if your data set comply with the expected format")
        else:
            # a new dataset is created based on source
            try:
                print("pre-processing existing dataset")
                source_data = args.dataset_identifier
                print("source data : " + source_data)
                # target_data = args.target_dataset_identifier
                # TODO link to experiment identifier!
                # experiment_identifier = args.experiment_identifier
                method_identifier = args.preprocessing_method_identifier

                print("source " + source_data + "method " + method_identifier)

                path = APP_CONFIG["application_files_location"] + APP_CONFIG["application_store_name"]
                df = dr.get_data_frame_from_hdf(source_data, path)
                print("data frame is loaded")
                new_data_set = ed.normalize_gene_counts(df, method_identifier,
                                                        target_identifier=source_data,
                                                        experiment_identifier=args.experiment_identifier)

                return cr.JsonResource(eto.SummaryDatasetView(new_data_set).to_json()), 201
            except Exception as e:
                print(e.__str__())
                return cr.StringApiResource("Explosion! Tool down..."), 409


class Dataset(restful.Resource):
    def get(self, datasetId, elements=None):
        print("get dataset")
        print(datasetId)
        path = APP_CONFIG["application_files_location"] + APP_CONFIG["application_store_name"]
        if elements == "file":
            print("creating frame")
            print("accepting ")
            print(request.accept_mimetypes)
            # convert public to intern...
            return cr.DataFrameApiResource(dr.get_data_frame_from_hdf(datasetId, path), datasetId + ".tsv"), 201
        if elements == "genes":
            dataset_with_ensembl = dr.get_dataset_genes_with_ensembl_info(datasetId, path)

            return cr.JsonResource(dataset_with_ensembl), 201
        if elements == "desc":
            dataset = dr.get_data_frame_from_hdf(datasetId, path)
            filtered = dataset.sum(1) == 0
            d_filtered = dataset[-filtered]
            filtered_data_set = d_filtered  # pd.DataFrame(scale(d_filtered), index=d_filtered.index, columns=d_filtered.columns)
            json_message = {"meta":{"samples":len(filtered_data_set.columns), "genes":len(filtered_data_set.index)},
                "samples": [{"id": s} for idx, s in enumerate(filtered_data_set.columns)], "descriptive": [
                {"identifier": item[0], "mean": item[1].mean(), "sd": item[1].std(), "max": item[1].max()}
                for item in filtered_data_set.iterrows()
                ]}
            return cr.JsonResource(json_message), 201


    def put(self, datasetId, elements=None):
        print(datasetId)
        args = dataset_parser.parse_args()
        dataset_identifier = args.dataset_identifier

        print("id " + dataset_identifier)
        dr.update_meta_data(datasetId, dataset_identifier)

        return cr.StringApiResource("Updated"), 200

    def delete(self, datasetId):
        pass


job_parser = reqparse.RequestParser()
job_parser.add_argument("dataset_identifier", type=str)
job_parser.add_argument("method_identifier", type=str)
job_parser.add_argument("experiment_identifier", type=str)
job_parser.add_argument("min_samples", type=int)
job_parser.add_argument("min_distance", type=float)
job_parser.add_argument("min_support", type=str)
job_parser.add_argument("local", type=bool)
job_parser.add_argument("compare_datasets", type=str, action="append")
job_parser.add_argument("features", type=str, action="append")
job_parser.add_argument("chart_type", type=str)


class Tasks(restful.Resource):
    def get(self):
        args = job_parser.parse_args()
        res = pr.get_all_tasks()
        result = [eto.TaskView(t).to_json() for t in res]

        return cr.JsonResource(result), 200

    def post(self):
        args = job_parser.parse_args()
        if args.local:
            print args.compare_datasets
            if args.compare_datasets is not None:
                return cr.MatPlotLibResource(dp.plot_comparison(args.compare_datasets, args.features, args.chart_type))

        method = args.method_identifier
        dataset = args.dataset_identifier
        min_distance = args.min_distance
        min_samples = args.min_samples
        print(args.experiment_identifier)
        res = pr.create_mining_task(method + "_" + dataset + "_" + ig.get_generated_guid_as_string(),
                                    method, dataset, min_sample=min_samples, min_distance=min_distance,
                                    experiment_identifier=args.experiment_identifier)

        return cr.JsonResource(eto.JobView(res).to_json()), 201


class Task(restful.Resource):
    # get the results of a job from db (genes for now)
    def get(self, taskId):
        stream = Stream()
        return stream.get(taskId)

    def put(self, taskId):
        pass

    def delete(self, taskId):
        pass


class Packages(restful.Resource):
    def get(self):
        pass

    def post(self):
        pass


class Package(restful.Resource):
    def get(self, packageId):
        pass
