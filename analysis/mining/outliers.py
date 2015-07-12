import json
import csv
import numpy as np
import pandas as pd
from sklearn import cluster
from sklearn.cluster import DBSCAN
from statsmodels.robust.scale import mad
from scipy.stats import itemfreq, scoreatpercentile

from entities import datasets_rep as dr
from entities import processing_rep as pr

def distribution_based_outliers(data, threshold, min_samples):
    pass


# TODO refactor mess
# TODO handle db connection outside clustering alg after demo
def cluster_outliers(data, genes, max_samples, min_dist=0.8, mining_id=1, as_json=True):
    estimator = cluster.KMeans(2)  # init kmeans
    samples_from_perc = round(max_samples * len(data.columns) / 100)
    print(samples_from_perc)
    ens = False
    info = None

    if str(genes[0]).startswith("ENSG"):
        res = dr.get_dataset_ensembl_info()
        ens = True
    outliers_id = []
    # debug_count = 0
    if as_json:
        yield (u"{\"outliers\":[")
    for g in genes:
        # if debug_count > 10:
        # break
        try:
            gene_row = data.loc[g, :].dropna()
            gene_row = gene_row.to_frame()

            estimator.fit(gene_row)  # conversion to dframe for model fit
            candidates = itemfreq(estimator.labels_)
            class_zero = candidates[0][1]
            class_one = candidates[1][1]
            support = min(class_one, class_zero)
            majority_class = class_one > class_zero
            dist = abs(max(gene_row[estimator.labels_ == majority_class]) - max(
                gene_row[estimator.labels_ == 1 - majority_class]))
            ran = gene_row.max() - gene_row.min()

            ndist = dist / float(ran)
            print(ndist)
            if 0 < support <= samples_from_perc and min_dist < ndist < 1:
                # debug_count += 1
                if ens:
                    info = [gene for gene in res if gene.ensemblgeneid == g][0]
                    formatted_info = {"identifier": g, "name": info.genename, "type": info.genetype, "samples": str(support),
                                      "distance": str(ndist), "range": str(ran)}
                else:
                    formatted_info = {"identifier": g, "name": "Not available", "type": "Not available", "samples": str(support),
                                      "distance": str(ndist), "range": str(ran)}

                outliers_id.append(formatted_info)
                print("outlier found :" + g)
                if as_json:
                    jinfo = json.dumps(formatted_info)
                    jinfo += u","
                    yield (jinfo)
                else:
                    yield (formatted_info)
        except:
            # if there is an issue on one gene (no variation, clustering impossible) the majority class
            # selection will obviously explode, we capture that in this block and just continue with the next gene (no harm done, there are
            # no outliers when the values are the same)
            pass

    if len(outliers_id) > 0:
        pr.save_outliers(mining_id, outliers_id)
        yield(str(u"]}"))


# with some variability (less than 50% of values are equal in the row)
#todo reactivate
def mad_outliers(data, genes, threshold, percentile=95, as_json=True):
    res = dr.get_dataset_ensembl_info()
    outliers_id = []
    if as_json:
        yield ("{\"outliers\":[")
    for g in genes:
        row_values = data.loc[g, :]
        cut_row_values = row_values
        med = cut_row_values.median()
        row_mad = mad(cut_row_values)

        if row_mad != 0.0:
            filtered = (cut_row_values - med) / row_mad
            support = len(filtered[filtered > threshold])

            if scoreatpercentile(filtered, 95) > threshold:

                info = [gene for gene in res if gene.ensemblgeneid == g][0]
                formatted_info = {"id": g, "name": info.genename, "type": info.genetype, "samples": str(support),
                                  "distance": "NA"}
                jinfo = json.dumps(formatted_info)
                jinfo += ","
                outliers_id.append(g)
                print("outlier found :" + g)
                if as_json:
                    yield (jinfo)
                else:
                    yield (formatted_info)
    if len(outliers_id) > 0:
        pr.save_outliers(1, outliers_id)

    if as_json:
        yield ("]}")


def dbscan_outliers(data, genes, eps, min_samples, max_samples=1, as_json=True):
    db = DBSCAN(eps=eps, min_samples=min_samples)
    # sd_scaler = StandardScaler()
    res = dr.get_dataset_ensembl_info()
    outliers_id = []
    for g in genes:
        # scaled = sd_scaler.fit(data.loc[g, :])
        fit = db.fit(np.reshape(data.loc[g, :], (196, 1)))

        candidates = itemfreq(fit.labels_)

        try:
            class_zero = candidates[0][1]
            class_one = candidates[1][1]

            support = min(class_one, class_zero)

            if min_samples < support <= max_samples:
                info = [gene for gene in res if gene.ensemblgeneid == g][0]
                formatted_info = {"id": g, "name": info.genename, "type": info.genetype, "samples": str(support),
                                  "distance": "NA"}
                jinfo = json.dumps(formatted_info)
                jinfo += ","
                outliers_id.append(g)
                print("outlier found :" + g)
                if as_json:
                    yield (jinfo)
                else:
                    yield (formatted_info)
        except:
            pass


# # # data_path = "D:\\Mining\\armel\\junctions_new_counts\\deseq_umc_raw_read_counts_table_without_8433.csv"
# data_path = "C:\\Users\\armelh\\Documents\\RnaSeqMiner\\Data\\TCGA\\deseq_CRC_RNASeq_rawcounts.csv"
# one_data_set = pd.read_csv(data_path, sep="\t", engine="python", index_col=0)
# # one_data_set = data_set[-(data_set.sum(1) <= 50)]  # THRESHOLD of 5
#
# print one_data_set.iloc[:, 0].count()
# outliers = []
# #res = mad_outliers(one_data_set, one_data_set.index, threshold=99, min_low=0)
# count = 0
# with open('outliers_deseq_CRC_RNASeq_rawcounts.txt', 'w') as f:
#     columns = ["identifier", 'name', "type", "samples", "distance", "range"]
#     writer = csv.DictWriter(f, columns)
#     writer.writeheader()
#     for o in cluster_outliers(one_data_set, one_data_set.index, 10, 0.6, as_json=False):
#         writer.writerow(o)

# for o in dbscan_outliers(one_data_set, one_data_set.index, 4, as_json=False):
# for o in dbscan_outliers(one_data_set, one_data_set.index, 2, 1, 2, as_json=False):





