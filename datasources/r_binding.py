import pandas as pd
import numpy
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.pandas2ri
# import rpy2.rinterface as ri

class Result(object):
    frame = None
    package = ""
    version = ""

    def __init__(self):
        pass


#TODO recored version and package of transformations in DB
def deseq_gene_expression_normalization(df_data):
    rpy2.robjects.pandas2ri.activate()
    df_data = df_data.dropna()

    r_data_set = robjects.conversion.py2ri(df_data)
    base = importr("base")
    deseq = importr("DESeq")
    bio_generics = importr("BiocGenerics")
    rdiv = robjects.r.get('/')

    conds = base.factor(base.c(base.colnames(r_data_set)))

    cds = deseq.newCountDataSet(base.round(r_data_set), conds)
    res_est = bio_generics.estimateSizeFactors(cds)

    normalized = base.t(rdiv(base.t(bio_generics.counts(res_est)), bio_generics.sizeFactors(res_est)))
    rpy2.robjects.pandas2ri.deactivate()
    res = Result()
    res.frame = pd.DataFrame(numpy.round(numpy.matrix(normalized)), index=normalized.rownames, columns=normalized.colnames)
    res.package = "DESeq"
    res.version = deseq.__version__

    return res


def deseq2_gene_expression_normalization(df_data):
    rpy2.robjects.pandas2ri.activate()
    df_data = df_data.dropna()

    r_data_set = robjects.conversion.py2ri(df_data)

    base = importr("base")
    deseq2 = importr("DESeq2")
    bio_generics = importr("BiocGenerics")
    gr = importr('GenomicRanges')
    vec = importr('S4Vectors')


    conds = vec.DataFrame(condition=base.factor(base.c(base.colnames(r_data_set))))
    print df_data.head()
    design = robjects.r('formula(~ condition)')

    dds = deseq2.DESeqDataSetFromMatrix(r_data_set, colData=conds, design=design)
    print("dds loaded")
    logs = deseq2.rlog(dds, fast=True)
    logs_count = gr.assay(logs)
    print("logs_count loaded")
    rpy2.robjects.pandas2ri.deactivate()
    res = Result()
    res.frame = pd.DataFrame(numpy.matrix(logs_count), columns=logs_count.colnames, index=logs_count.rownames)
    res.package = "DESeq2"
    res.version = deseq2.__version__

    return res


def edger_gene_expression_normalization(df_data):
    rpy2.robjects.pandas2ri.activate()
    df_data = df_data.dropna()
    r_data_set = robjects.conversion.py2ri(df_data)


    edger = importr("edgeR")
    base = importr("base")
    mult = robjects.r.get('*')

    factors = base.factor(base.c(base.colnames(r_data_set)))
    dge = edger.DGEList(counts=r_data_set, group=factors)
    y = edger.calcNormFactors(dge)
    y = edger.estimateCommonDisp(y)

    #y [counts] and y[samples][size factors] accessed by index
    #bit tricky but yeah...
    #there is a conversion between python 0 based index and r (1 based)
    #done by rpy2 which is a fabulous library!!!
    normalized = mult(y[0], y[1][2])

    rpy2.robjects.pandas2ri.deactivate()

    print("preparing result")
    res = Result()
    res.frame = pd.DataFrame(numpy.round(numpy.matrix(normalized)), columns=normalized.colnames, index=normalized.rownames)
    res.package = "edgeR"
    res.version = edger.__version__

    return res


def voom_gene_expression_normalization(df_data):
    rpy2.robjects.pandas2ri.activate()
    df_data = df_data.dropna()
    r_data_set = robjects.conversion.py2ri(df_data)

    limma = importr("limma")

    print("voom is applied")
    voom = limma.voom(r_data_set)
    #because pandas r interface was deprecated in the new release (v0.16.0) we must convert an R matrix
    #manually to a pandas dataframe
    #voom actually stores an array containing all the outputs of the "original
    #limma voom method but we are just interested in the normalized counts
    #and they are stored in the first item
    df = pd.DataFrame(numpy.matrix(voom[0]), columns=voom[0].colnames, index=voom[0].rownames)

    rpy2.robjects.pandas2ri.deactivate()

    res = Result()
    res.frame = df
    res.package = "limma"
    res.version = limma.__version__

    return res


def test_r_binding_vps():
    data_path = "/home/remu/Documents/an_umc_raw_read_counts_table.txt"
    data_set = pd.read_csv(data_path, sep="\t", engine="python", index_col=0)

    lol = deseq_gene_expression_normalization(data_set)
    #lol = voom_gene_expression_normalization(data_set)
    #lol = deseq2_gene_expression_normalization(data_set)
    #lol = edger_gene_expression_normalization(data_set)

    print lol.package
    print lol.version
    print lol.frame.head()

#test_r_binding_vps()