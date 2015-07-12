from pandas import *
import matplotlib.pyplot as plt
from mining import outliers as out

from entities import datasets_rep as dr

from config import APP_CONFIG

#TODO exons are slightly different

def load_dataframe(dataset):
    return read_csv(dataset.intern_location, sep='\t', index_col=0)


def save_chart_to_file(chart):
    pass


def get_demo_raw_set():
    return read_csv(APP_CONFIG["demo_data_set_raw"], sep='\t', index_col=0)


def get_sample_mean():
    return get_demo_raw_set().mean(axis=1)


def get_demo_normalized_set():
    return read_csv(APP_CONFIG["demo_data_set_norm"], sep='\t', index_col=0)


def plot_distribution(counts):
    fig = plt.figure()
    plt.plot(get_demo_raw_set().iloc[1:100, 1:100], )

    return fig


# Returns subset
# TODO get full list when table ready
def get_list_of_genes(data):
    # sorted_elements = [rem.ix[idx, list(rem.ix[idx, :].isin(sorted(row, reverse=True)[:10]))] for idx, row in rem.head().iterrows()]
    return data.ix[1:, 0]


def remove_non_expressed_genes(data, source_identifier, custom_prefix="no_outliers_"):

    new_set = data[-(data.iloc[:, 1:].sum(1) == 0)]

    target_name = custom_prefix + source_identifier
    location = APP_CONFIG["application_base_location"] + target_name + ".txt"

    created = dr.create_data_set(identifier=target_name, type=dr.ACTION_TYPES["zcounts"], location=location)

    new_set.to_csv(location, index=False, sep="\t")

    return created


def get_descriptive_per_expression_set(data):
    samples_descriptives = data.describe()

    samples_descriptives.loc["id"] = ["S" + i for i in samples_descriptives.columns]
    return samples_descriptives


def get_outliers_per_gene(data, gene, method="mad", cutoff=2):
    result = None
    if method == "mad":
        result = out.mad_outliers(data, gene, cutoff)
    elif method == "kmeans":
        result = out.cluster_outliers(data, gene, cutoff)

    return result


def get_info_sample_and_genes(data):
    genes_descriptives = data.transpose().describe()
    return genes_descriptives


def normalize_dataset(data, source_identifier, custom_prefix, method="TC"):
    pass
