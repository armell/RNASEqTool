import matplotlib

matplotlib.use('PDF')
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.charts import BoxPlot, HeatMap
from bokeh.plotting import ColumnDataSource
from bokeh.models import HoverTool
from bokeh import mpl
from bokeh import palettes as bp
import bokeh.plotting as bpl
from entities import datasets_rep as dr
from config import APP_CONFIG

# Dataset:
# genes in col 0
# samples in cols 1 -> N
def sample_distribution_for_genes(dataset_identifier, genes, title="", samples=None, unit="zscore", chart_type="heat",
                                  chart_rendering="html"):
    try:
        generator = None
        convert = False
        tooltip = False
        sns.set(style="whitegrid")
        #get path to HDF store from config file
        path_to_store = APP_CONFIG["application_files_location"] + APP_CONFIG["application_store_name"]

        print("path to store " + path_to_store)
        print(genes)

        #get data set as a pandas frame
        dataset = dr.get_data_frame_from_hdf(dataset_identifier, path_to_store)
        tooltip = None
        #filter selected genes
        gene_list = dataset.loc[genes, :]
        labels = list(gene_list.columns)

        #matplotlib settings
        ax = None
        fig = None

        #heatmap
        #html = dynamic plot
        #pdf = pdf file
        if chart_type == "heat":

            if chart_rendering == "html":
                print("bokeh heatmap")
                sns.set()
                title += " heatmap"
                generator = "bokeh"

                print("sns heatmap")
                fig = HeatMap(gene_list.dropna(), title=title)
            elif chart_rendering == "pdf":
                plt.switch_backend('Agg')
                title += " heatmap pdf"
                sns.set_context("paper", font_scale=0.8)
                generator = "matplot"
                ax = sns.heatmap(gene_list)
                #adapt label fontsize
                for tick in ax.xaxis.get_major_ticks():
                    tick.label.set_fontsize(2.0)
                    # tick.label.set
                print("axis loaded")
                print("heatmap with bokeh")
        elif chart_type == "box":
            #boxplot charts
            title += " boxplot"
            generator = "bokeh"
            # convert = True
            TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,previewsave,hover"
            print("creating box plot")
            # new_z_set = pd.DataFrame(stats.zscore(gene_list), index=gene_list.index, columns=gene_list.columns)
            t_genes = gene_list.transpose()
            # sns.boxplot(t_genes, color="coolwarm_r", names=t_genes.columns)
            fig = BoxPlot(t_genes, legend=True, tools=TOOLS)
            hover = fig.select(dict(type=HoverTool))
            hover.tooltips = [
                ("sample", "$index")
            ]
        elif chart_type == "scatter":
            if chart_rendering == "html":
                title += " scatter"
                generator = "bokeh"

                # tooltip = True
                TOOLS = "resize, crosshair, pan, wheel_zoom, box_zoom,reset, previewsave, hover"
                fig = bpl.figure(title=title, tools=TOOLS)
                current_palette = sns.color_palette()
                i = 0
                colors = bp.Spectral10
                # fig.scatter(dc, dc["index"])
                for e in gene_list.iterrows():
                    val = [v for v in e[1]]
                    idx = range(0, len(val))
                    col_data_source = ColumnDataSource(dict(
                        x=idx,
                        y=val,
                        sample=gene_list.columns[idx],
                    ))

                    fig.scatter('x', 'y', color=colors[i], legend=e[0], source=col_data_source)
                    i += 1

                hover = fig.select(dict(type=HoverTool))
                hover.tooltips = [
                    ("sample", "@sample"),
                    ("count", "$y")
                ]
            elif chart_rendering == "pdf":
                plt.switch_backend('PDF')
                sns.color_palette("deep")
                title += " scatter pdf"
                generator = "matplot"
                print("starting with matplot")
                transposed_data = gene_list.transpose()
                ax = transposed_data.plot(style='o')
                legend = plt.legend(frameon=1)
                frame = legend.get_frame()
                frame.set_edgecolor('blue')
                coll_len = len(gene_list.columns)
                for idx, gene in enumerate(gene_list.index):
                    for x, y in zip(range(0, coll_len), gene_list.iloc[idx, :]):
                        if y > gene_list.iloc[idx, :].quantile(0.99):
                            ax.annotate(labels[x], xy=(x, y), textcoords='data')
                # grid.add_legend(labels)
                print("plotted with matplot")

        if ax is not None:
            if generator == "matplot" and (title is not None):
                ax.set_title(title)
            elif generator == "matplot" and ax is not None:
                ax.set_title(title)

        if generator == "matplot":
            fig = plt.gcf()

        if convert is True and generator == "bokeh":
            fig = plt.gcf()
            fig = mpl.to_bokeh(fig)

        return {"generator": generator, "chart": fig}
    except BaseException as e:
        print(e.__str__())

        # generic dictionary with generator (str -> bokeh or matplot) and chart (matplot figure !!ALWAYS!)


def outliers_distribution_for_genes(data, genes, type, threshold):
    pass






