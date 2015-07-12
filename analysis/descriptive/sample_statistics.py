from bokeh.crossfilter.models import CrossFilter
from bokeh.sampledata.autompg import autompg
from bokeh.mpl import to_bokeh
from config import APP_CONFIG
from pandas import read_csv
from entities import datasets_rep as dr
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
from mpld3 import plugins

available_eda_plots = [
    "box",
    "scatter",
    "heatmap"
]

def test2():
    autompg['cyl'] = autompg['cyl'].astype(str)
    autompg['origin'] = autompg['origin'].astype(str)
    cross = CrossFilter.create(df=autompg)

    return cross


def test(datasets="", genes=None, samples=None, chart_type=None, scale=None):
    data = get_demo_normalized_set()
    sns.set_style("whitegrid")
    if chart_type is None or chart_type == "box":
        data.transpose().boxplot(column=[1, 2, 3], return_type="axes")
    elif chart_type == "scatter":
        pass

    return to_bokeh(name="descriptive")

def desc_data():
    pass

def desc_data_pca_dataset(method=None):
    pass

def query_set_gene(dataset,gene):
    pass

def get_demo_normalized_set():
    return read_csv(APP_CONFIG["demo_data_set_norm"], sep='\t', index_col=0)

def plot_bokeh_eda(fig, labels):
    pass

def plot_sample(dataset_identifiers, samples, type="boxplot"):
    pass

def plot_comparison(dataset_identifiers, features, type="boxplot"):
    sns.set_style("whitegrid")
    sns.set_palette("deep")
    generator = "matplot"
    f, axes = plt.subplots(1, 2)
    # dataset_identifiers = ['DESeq_1_18_0_umc_read_counts_table_without_8433',
    #                       'DESeq_1_18_0_genentech_read_counts_table']
    # features = ["ENSG00000002549"]
    path = APP_CONFIG["application_files_location"] + APP_CONFIG["application_store_name"]
    i = 0
    subset = None
    print features
    for d in dataset_identifiers:
        dataset = dr.get_data_frame_from_hdf(d, path)
        subset = dataset.ix[features, :]
        if type == "boxplot":
            axes[i].boxplot(subset)
        if type == "scatter":
            generator = "matplot"
            #print len(subset.ix[0, :])
            t = axes[i].plot(subset.transpose(), 'o')
            plugins.connect(f, plugins.PointLabelTooltip(t[0], labels=(list(subset.columns))))
        axes[i].set_xlabel(d)
        axes[i].set_ylabel(str(features))

        i += 1

    if generator == "bokeh":
        bk = to_bokeh(name="descriptive")
    else:
        bk = plt.gcf()
        sz = bk.get_size_inches()
        bk.set_size_inches((sz[0]*2.5, sz[1]*2))
    return bk



def test():
    ds = ['DESeq_1_18_0_umc_read_counts_table_without_8433', 'DESeq_1_18_0_genentech_read_counts_table']
    plot_comparison(ds, "ENSG00000000460", type="scatter")
    plt.show()

# test()
