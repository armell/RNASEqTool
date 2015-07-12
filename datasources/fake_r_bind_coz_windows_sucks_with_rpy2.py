# This is a fake R binding when running the app on windows
# As RPY2 is not working well on this OS

class Result(object):
    frame = None
    package = ""
    version = ""
    identifier = ""

    def __init__(self):
        pass


def deseq_gene_expression_normalization(df_data):
    pass


def deseq2_gene_expression_normalization(df_data):
    pass


def edger_gene_expression_normalization(df_data):
    pass


def voom_gene_expression_normalization(df_data):
    pass
