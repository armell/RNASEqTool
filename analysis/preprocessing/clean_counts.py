import pandas as pd
from config import APP_CONFIG


class CleanParameters(object):
    def __init__(self,data_set_name, zero_values=False, min_samples=0, min_count_values=0, min_sum_count = 5):
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


class CleanReport(object):
    def __init__(self):
        self.removed_rows = 0
        self.removed_indexes = []
        self.dataset_location = ""
        self.dataset_identifier = ""

    def __str__(self):
        return str.format("{0} rows were removed", self.removed_rows)

#TODO clean dataset to store
#not copy but replace this time
def clean_gene_count_file(data_set, clean_parameters):
    report = CleanReport()
    filtered = data_set.sum(1) <= clean_parameters.min_sum_count

    filtered_data_set = data_set[-filtered]
    report.removed_rows = len(data_set.index) - len(filtered_data_set.index)
    report.removed_indexes = list(data_set.index.difference(filtered_data_set.index))

    #register to disk

    path = APP_CONFIG["application_files_location"] + "cleaned_" + clean_parameters.data_set_name + ".csv"
    report.dataset_location = path
    report.dataset_identifier = "cleaned_" + clean_parameters.data_set_name

    filtered_data_set.to_csv(path, sep="\t")
    return report


def test_clean_gene_count():
    data_path = "D:\\Mining\\armel\\junctions_new_counts\\umc_raw_read_counts_table.txt"
    data_set = pd.read_csv(data_path, sep="\t", engine="python", index_col=0)

    clean_parameters = CleanParameters(data_set_name="my_cleaning_experienceee", zero_values=True, min_sum_count=50)
    res = clean_gene_count_file(data_set, clean_parameters)

    print res
    print len(res.removed_indexes)

# test_clean_gene_count()