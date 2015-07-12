import datetime

import pandas as pd
from peewee import fn

import entities as ent
import experiments_rep as exp
import methods_rep as mr
import analysis
from datasources import hdf_storage
#query the DB for datasets

ACTION_TYPES = {"norm": "normalized",
                "zcounts": "zero counts removed"}


# caution, supposed to know the file format with tab separator in this case
def get_gene_intern_count_data_set_by_identifier(identifier, separator="\t"):
    ent.database.connect()
    loc = ent.Datasets.get(ent.Datasets.public_identifier == identifier).intern_location
    ent.database.close()
    print(loc)
    return pd.read_csv(loc, sep=separator, engine="python", index_col=0)


def get_all_datasets():
    ent.database.connect()
    # dataset_list = ent.Datasets.select().join(ent.ExperimentDataset).join(ent.Experiments)
    dataset_list = ent.ExperimentDataset.select().join(ent.Datasets).join(ent.DatasetTypes).switch(ent.Datasets).join(
        ent.Packages) \
        .switch(ent.ExperimentDataset) \
        .join(ent.Experiments)
    ent.database.close()

    return dataset_list

def get_data_frame_from_csv(fp, sep="\t", index=0):
    return pd.read_csv(fp, sep=sep, index_col=index)


def store_data_frame_to_hdf(df, identifier):
    return hdf_storage.store_hdf(df, identifier)


#gets file from HDF storage (not mysql)
def get_data_frame_from_hdf(public_identifier, store_location):
    ent.database.connect()
    entity = ent.Datasets.get(ent.Datasets.public_identifier == public_identifier)
    intern_identifier = entity.intern_identifier
    print intern_identifier
    return hdf_storage.retrieve_hdf(intern_identifier, store_location)


#update meta data, here public identifier after upload
def update_meta_data(dataset_intern_identifier, public_identifier):
    ent.database.connect()
    entity = ent.Datasets.get(ent.Datasets.intern_identifier == dataset_intern_identifier)
    entity.public_identifier = public_identifier
    # add method update
    entity.save()

    ent.database.close()


def create_data_set(intern_identifier, public_identifier, dataset_type, package_identifier="htseq_count",
                    experiment_identifier=""):
    ent.database.connect()
    data_type = ent.DatasetTypes.get(ent.DatasetTypes.name == dataset_type)
    print(data_type)

    created_dataset = ent.Datasets.create(intern_identifier=intern_identifier,
                                          public_identifier=public_identifier, intern_location="hdf",
                                          type=data_type, url="", size=0, generation_type="NA",
                                          granularity_level="gene", is_raw=True, number_samples=0, number_features=0,
                                          feature_type="gene",
                                          added_on=datetime.datetime.now(),
                                          package=ent.Packages.get(
                                              ent.Packages.public_identifier == package_identifier))

    if experiment_identifier is not None:
        print(experiment_identifier)
        exp.link_dataset_to_experiment(experiment_identifier, public_identifier)
    else:
        ent.database.close()

    return created_dataset


# TODO memory consumption gene name to ids linking
# link gene ids to ensembl data
def get_list_of_genes(datasetId):
    ent.database.connect()
    dataset = ent.Datasets.get(ent.Datasets.public_identifier == datasetId)
    loaded_dataframe = analysis.gene_expression.load_dataframe(dataset)
    genes_name_dataset = analysis.gene_expression.get_list_of_genes(loaded_dataframe)
    genes_meta_data = ent.NameGeneEnsembl.select(ent.NameGeneEnsembl.gene_name, ent.NameGeneEnsembl.gene_type,
                                                 ent.NameGeneEnsembl.ensembl_gene_id).where(
        ent.NameGeneEnsembl.ensembl_gene_id << list(genes_name_dataset))

    # temp output to grid
    genes_with_id = [{"id": g.ensembl_gene_id, "name": g.gene_name, "type": g.gene_type} for g in
                     genes_meta_data.iterator()]

    ent.database.close()

    return genes_with_id

# CAUTION: GRCh37 release 78 only
def get_list_of_genes_with_frame(frame):
    ent.database.connect()
    print("retrieve genes with ids")
    genes_with_id = None
    genes_meta_data = ent.NameGeneEnsembl.select(ent.NameGeneEnsembl.genename, ent.NameGeneEnsembl.genetype,
                                                 ent.NameGeneEnsembl.ensemblgeneid).where(
        ent.NameGeneEnsembl.ensemblgeneid << list(frame.index))

    if str(frame.index[0]).startswith("ENSG"):
        genes_with_id = [{"identifier": g.ensemblgeneid, "name": g.genename, "type": g.genetype} for g in
                         genes_meta_data.iterator()]
    else:
        print("no ENSEMBL id")
        genes_with_id = [{"identifier": g, "name": "not available", "type": "not available"} for idx, g in
                         enumerate(frame.index)]

    ent.database.close()

    return genes_with_id


def get_dataset_genes_with_ensembl_info(dataset_identifier, store=""):
    loaded_dataset = get_data_frame_from_hdf(dataset_identifier, store)

    return get_list_of_genes_with_frame(loaded_dataset)


def get_dataset_ensembl_info():
    ent.database.connect()
    res = ent.NameGeneEnsembl.select(ent.NameGeneEnsembl.genename, ent.NameGeneEnsembl.ensemblgeneid,
                                     ent.NameGeneEnsembl.genetype)
    ent.database.close()
    return res


def link_dataset_to_package(dataset_identifier, package_identifier):
    ent.database.connect()
    package = mr.get_package(package_identifier)

    q = ent.Datasets.update(package=package).where((ent.Datasets.public_identifier == dataset_identifier))
    q.execute()
    ent.database.close()


def test_dataset_info():
    ent.database.connect()

    query = ent.ExperimentDataset.select().join(ent.Datasets).join(ent.DatasetTypes) \
        .switch(ent.ExperimentDataset) \
        .join(ent.Experiments)

    for q in query:
        print q.dataset.public_identifier + " " + q.dataset.type.name + " exp " + q.experiment.public_identifier

# ent.database.close()

