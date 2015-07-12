from normalization import count_normalization as cn
from mining import outliers as om
from preprocessing import clean_counts as cc
from entities import processing_rep as pr
from entities import datasets_rep as dr
from entities import methods_rep as mr
from entities import experiments_rep as er
from datasources import hdf_storage
from entities import identifier_generator
from config import APP_CONFIG


def process_job_request(data, method, thresholds, target_identifier):
    method_type_name = pr.get_type_from_method(method)

    return select_processing[method_type_name](data, method, thresholds)


def stream_detect_outliers_in_data(data, method, min_dist, max_samples, mining_id):
    # if exists -> get from db
    processing_result = None
    store_path = APP_CONFIG["application_files_location"] + APP_CONFIG["application_store_name"]
    data = dr.get_data_frame_from_hdf(data, store_path)
    # For demo purposes (cleaning)
    data = data[-(data.sum(1) <= 5)]
    if method == "kmeans_outliers":
        return om.cluster_outliers(data, data.index, max_samples=max_samples, min_dist=min_dist, mining_id=mining_id)

    if method == "mad":
        return om.mad_outliers(data, data.index, max_samples)


def get_detected_outliers(data, method, min_distance, min_samples):
    return "lol"


def remove_low_counts(data, method="sum", threshold=50, target_identifier=""):
    params = cc.CleanParameters("umc")
    params.min_sum_count = threshold
    report = cc.clean_gene_count_file(data, params)

    dataset = dr.create_data_set(report.dataset_identifier, "genes low counts removed", report.dataset_location)
    print(dataset.added_on)
    return dataset


def normalize_gene_counts(data, method, threshold=None, target_identifier="", experiment_identifier=""):
    # if exists -> get from db
    processing_result = cn.bioconductor_normalization(data, method)

    new_intern_identifier = identifier_generator.get_generated_guid_as_string()
    hdf_storage.store_hdf(processing_result.frame, new_intern_identifier)
    print("compressed pytable storage done")
    package = mr.get_package_by_name_and_version(processing_result.package,
                                                 processing_result.version).public_identifier
    dataset = dr.create_data_set(new_intern_identifier, package + "_" + target_identifier, "genes normalized dataset",
                                 package_identifier=package,
                                 experiment_identifier=experiment_identifier)
    print("new dataset saved")
    #er.link_dataset_to_experiment(experiment_identifier, dataset.public_identifier)
    print("new dataset linked")
    return dataset


def save_pre_processing(old_data, new_data, information):
    package_used = information.package
    package_version = information.version


def record_processing_to_db():
    pass


select_processing = {
    "Normalization RNA-seq": normalize_gene_counts,
    "Outlier detection": get_detected_outliers,
    "Low expression removal": remove_low_counts
}

# print process_job_request("lol", "mad", 5)

