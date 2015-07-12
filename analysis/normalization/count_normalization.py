# edit to from datasources import fake_r_bind_coz_windows_sucks_with_rpy2 as r_binding
# if running on windows (R will not work)
from datasources import r_binding as r_binding
import pandas as pd


class NormalizationParameters(object):
    def __init__(self, data_set_name, zero_values=False, min_samples=0, min_count_values=0, min_sum_count=5):
        self.zero_values = zero_values
        self.min_samples = min_samples
        self.min_count_values = min_count_values
        self.min_sum_count = min_sum_count
        self.data_set_name = data_set_name

    def __str__(self):
        removed = ""
        if not self.zero_values:
            removed = "not"

        return str.format("Zero values were {0} removed", removed)


class NormalizationReport(object):
    def __init__(self):
        self.removed_rows = 0
        self.removed_indexes = []

    def __str__(self):
        return str.format("{0} rows were removed", self.removed_rows)


# calls an R environment and R packages to perform
# dataset normalization or transformation
def bioconductor_normalization(data, method="deseq"):
    # based on the package selected by the user, a different R code
    # is executed
    if str.lower(method).startswith("deseq2"):
        return r_binding.deseq2_gene_expression_normalization(data)
    if str.lower(method).startswith("deseq"):
        return r_binding.deseq_gene_expression_normalization(data)
    if str.lower(method).startswith("edger"):
        return r_binding.edger_gene_expression_normalization(data)
    if str.lower(method).startswith("limma"):
        return r_binding.voom_gene_expression_normalization(data)

    raise Exception("Method is not implemented")

# not used anymore, normalization with mean
def total_count_normalization_with_mean(data):
    divided = total_count_normalization(data)

    return divided.mul(data.mean(axis=1), 0)


def total_count_normalization(data):
    return data.div(data.sum(axis=0), 1)
