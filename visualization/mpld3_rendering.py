from analysis import gene_expression as ge
from scipy import stats
import matplotlib.pyplot as plt
from mpld3 import fig_to_html, plugins, fig_to_dict
import seaborn as sns
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh import mpl
import mpld3_extra as extra

def plot_distribution_for_genes(data, genes):
    distributions = generate_distribution_for_genes(data, genes)
    sns.set_palette("deep", desat=.6)
    i = 0
    hist = None
    fig = plt.figure()
    for dist in distributions:
        plt.hist(dist, alpha=0.5, label=genes[i])
        i += 1

    plt.legend()
    plt.title(genes.__str__() + " distribution")

    #script, div = components(mpl.to_bokeh(), CDN)

    #return {"js": script, "html": div}
    plugins.connect(fig, extra.InteractiveLegendPlugin())
    return fig_to_html(fig)


def generate_distribution_for_genes(data, genes):
    subset = data[data.iloc[:, 0].isin(genes)]
    i = 0
    zscores = []
    while i < len(subset.iloc[:, 1:]):
        zscores.append(stats.zscore(subset.iloc[i, 1:]))
        i += 1

    return zscores


def build_plot_html(fig):
    return fig_to_html(fig)


def build_plot_json(fig):
    return fig_to_dict(fig)


def build_plot_png(fig):
    pass

#Tests

# plot_distribution_for_genes(ge.get_demo_normalized_set(), ["ENSG00000000003", "ENSG00000001460"])

# test_distribution = generate_distribution_for_genes(ge.get_demo_normalized_set(), ["ENSG00000000003", "ENSG00000001460"])

#test_plot = plot_distribution_for_genes(ge.get_demo_normalized_set(), ["ENSG00000000003", "ENSG00000001460"])

#mpld3.show()

#print plot_distribution_for_genes(ge.get_demo_normalized_set(),["ENSG00000000003"])