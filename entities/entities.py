from peewee import *
from playhouse.db_url import connect

from config import APP_CONFIG



# database = connect(APP_CONFIG["db_string"]["sql_url"])

database = connect(APP_CONFIG["db_string"]["sql_url"])
#database = SqliteDatabase('./db/rnaseqtool.sqlite')

class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = database


class DatasetTypes(BaseModel):
    description = TextField()
    first_sample = IntegerField()
    name = CharField()

    class Meta:
        db_table = 'dataset_types'


class Packages(BaseModel):
    added_on = DateField()
    description = TextField()
    language = CharField()
    public_identifier = CharField()
    reference = CharField()
    url_source = CharField(null=True)
    version = CharField()
    name = CharField()

    class Meta:
        db_table = 'packages'


class Datasets(BaseModel):
    added_on = DateField()
    compressed_location = CharField(null=True)
    feature_type = CharField()
    generation_type = CharField()
    granularity_level = CharField()
    intern_identifier = CharField(null=True)
    intern_location = CharField()
    is_raw = IntegerField()
    number_features = IntegerField()
    number_samples = IntegerField()
    public_identifier = CharField(unique=True)
    raw_content = TextField(null=True)
    size = IntegerField()
    type = ForeignKeyField(db_column='type', null=True, rel_model=DatasetTypes, to_field='id')
    url = CharField()
    package = ForeignKeyField(db_column='package_id', null=True, rel_model=Packages, to_field='id')

    class Meta:
        db_table = 'datasets'


class MethodTypes(BaseModel):
    reference = CharField(db_column='Reference')
    description = TextField()
    name = CharField(unique=True)
    rank = IntegerField()

    class Meta:
        db_table = 'method_types'


class Methods(BaseModel):
    description = TextField()
    name = CharField()
    public_identifier = CharField(unique=True)
    type = ForeignKeyField(db_column='type', rel_model=MethodTypes, to_field='id')
    updated = DateField()

    class Meta:
        db_table = 'methods'


class DatasetGenesOutliers(BaseModel):
    dataset = ForeignKeyField(db_column='dataset_id', rel_model=Datasets, to_field='id')
    gene = CharField(db_column='gene_id', index=True)
    id = BigIntegerField(primary_key=True)
    method = ForeignKeyField(db_column='method_id', null=True, rel_model=Methods, to_field='id')
    rank_score = IntegerField(null=True)

    class Meta:
        db_table = 'dataset_genes_outliers'


class DatasetSamples(BaseModel):
    control = IntegerField()
    id = BigIntegerField(primary_key=True)
    identifier = CharField()
    sequencing_platform = CharField()

    class Meta:
        db_table = 'dataset_samples'


class EnsemblNameConversion(BaseModel):
    ensembl = CharField(db_column='ensembl_id', null=True)
    ensembl_version = CharField(null=True)
    id = BigIntegerField(primary_key=True)
    name = CharField(null=True)

    class Meta:
        db_table = 'ensembl_name_conversion'


class Experiments(BaseModel):
    context = TextField()
    created_on = DateField()
    description = TextField(null=True)
    id = BigIntegerField(primary_key=True)
    public_identifier = CharField(unique=True)
    type = CharField()

    class Meta:
        db_table = 'experiments'


class ExperimentDataset(BaseModel):
    dataset = ForeignKeyField(db_column='dataset_id', rel_model=Datasets, to_field='id')
    experiment = ForeignKeyField(db_column='experiment_id', rel_model=Experiments, to_field='id')

    class Meta:
        db_table = 'experiment_dataset'
        primary_key = CompositeKey('dataset', 'experiment')


class ExperimentPackage(BaseModel):
    experiment = ForeignKeyField(db_column='experiment_id', rel_model=Experiments, to_field='id')
    package = ForeignKeyField(db_column='package_id', rel_model=Packages, to_field='id')

    class Meta:
        db_table = 'experiment_package'
        primary_key = CompositeKey('experiment', 'package')


class Visualizations(BaseModel):
    chart_data = TextField()
    created_on = DateField()
    generated_by = CharField()
    id = BigIntegerField(primary_key=True)
    mime_type = CharField()
    public_identifier = CharField()
    type = CharField()

    class Meta:
        db_table = 'visualizations'


class ExperimentVisualization(BaseModel):
    experiment = ForeignKeyField(db_column='experiment_id', rel_model=Experiments, to_field='id')
    visualization = ForeignKeyField(db_column='visualization_id', rel_model=Visualizations, to_field='id')

    class Meta:
        db_table = 'experiment_visualization'
        primary_key = CompositeKey('experiment', 'visualization')


class GeneLengthEnsembl(BaseModel):
    ensembl_gene_id = CharField(db_column='Ensembl Gene ID', null=True)
    gene_end = IntegerField(db_column='Gene End (bp)', null=True)
    gene_start = IntegerField(db_column='Gene Start (bp)', null=True)

    class Meta:
        db_table = 'gene_length_ensembl'


class GeneratedContent(BaseModel):
    binary_content = TextField()
    dataset = ForeignKeyField(db_column='dataset', rel_model=Datasets, to_field='id')
    experiment = ForeignKeyField(db_column='experiment', rel_model=Experiments, to_field='id')
    generated_on = DateField()
    id = BigIntegerField(primary_key=True)
    job_executed = IntegerField()
    method = ForeignKeyField(db_column='method', rel_model=Methods, to_field='id')
    mime_type = CharField()
    public_identifier = CharField()

    class Meta:
        db_table = 'generated_content'


class MetadataSources(BaseModel):
    description = TextField()
    name = CharField()
    public_identifier = CharField(unique=True)
    version = CharField()

    class Meta:
        db_table = 'metadata_sources'


class MethodPackage(BaseModel):
    applied_on = DateField()
    method = ForeignKeyField(db_column='method_id', rel_model=Methods, to_field='id')
    package = ForeignKeyField(db_column='package_id', rel_model=Packages, to_field='id')

    class Meta:
        db_table = 'method_package'
        primary_key = CompositeKey('method', 'package')


class Mining(BaseModel):
    created_on = DateField()
    dataset = ForeignKeyField(db_column='dataset_id', rel_model=Datasets, to_field='id')
    id = BigIntegerField(primary_key=True)
    method = ForeignKeyField(db_column='method_id', rel_model=Methods, to_field='id')
    min_distance = FloatField()
    min_samples = IntegerField()
    support = IntegerField()
    public_identifier = CharField()
    is_executed = BooleanField()
    experiment= ForeignKeyField(db_column='experiment_id', rel_model=Experiments, to_field='id')

    class Meta:
        db_table = 'mining'


class MiningResult(BaseModel):
    feature = CharField(db_column='feature_id', index=True)
    id = ForeignKeyField(db_column='id', primary_key=True, rel_model=Mining, to_field='id')
    mining = IntegerField(db_column='mining_id', index=True)
    distance = FloatField(db_column='distance', null=True)
    range = DecimalField(db_column='range', null=True)

    class Meta:
        db_table = 'mining_result'


class NameGeneEnsembl(BaseModel):
    ensemblgeneid = CharField(db_column='EnsemblGeneID', null=True)
    genename = CharField(db_column='GeneName', null=True)
    genetype = CharField(db_column='GeneType', null=True)
    version = CharField(db_column='Version')

    class Meta:
        db_table = 'name_gene_ensembl'


class PatientInformation(BaseModel):
    class Meta:
        db_table = 'patient_information'


class Preprocessing(BaseModel):
    colums_affected = IntegerField()
    dataset = ForeignKeyField(db_column='dataset_id', rel_model=Datasets, to_field='id')
    experiment = ForeignKeyField(db_column='experiment_id', rel_model=Experiments, to_field='id')
    package = ForeignKeyField(db_column='package_id', rel_model=Packages, to_field='id')
    generated_on = DateField()
    method = ForeignKeyField(db_column='method_id', rel_model=Methods, to_field='id')
    outlier_threshold = IntegerField()
    public_identifier = CharField()
    rows_affected = IntegerField()

    class Meta:
        db_table = 'preprocessing'


class Reports(BaseModel):
    binary = TextField()
    language = CharField()
    name = IntegerField()
    package = IntegerField()
    public_identifier = CharField()
    updated_on = DateField()

    class Meta:
        db_table = 'reports'



