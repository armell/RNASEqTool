import entities as ent
import datetime

def get_experiments_all():
    ent.database.connect()
    query = ent.Experiments.select()
    ent.database.close()
    return query


def get_experiment_by_identifier(experiment_identifier):
    ent.database.connect()
    query = ent.ExperimentDataset.select().join(ent.Experiments).switch(ent.ExperimentDataset).join(ent.Datasets).join(
        ent.DatasetTypes).where(ent.Experiments.public_identifier == experiment_identifier)

    ent.database.close()

    return query


def get_generated_content(dataset, method, experiment):
    ent.database.connect()
    query = ent.GeneratedContent.select().join(ent.Methods) \
        .switch(ent.GeneratedContent) \
        .join(ent.Experiments) \
        .switch(ent.GeneratedContent) \
        .join(ent.Datasets) \
        .where((ent.Methods.public_identifier == method) & (ent.Experiments.public_identifier == experiment) & (
        ent.Datasets.public_identifier == dataset))

    ent.database.close()

    return query


def link_dataset_to_experiment(experiment_identifier, dataset_identifier):
    ent.database.connect()
    experiment = ent.Experiments.get(ent.Experiments.public_identifier == experiment_identifier)
    dataset = ent.Datasets.get(ent.Datasets.public_identifier == dataset_identifier)

    new_link = ent.ExperimentDataset.create(experiment=experiment.id, dataset=dataset.id)
    ent.database.close()

    return new_link


def unlink_dataset_to_experiment(experiment_identifier, dataset_identifier):
    ent.database.connect()
    experiment = ent.Experiments.get(ent.Experiments.public_identifier == experiment_identifier)
    dataset = ent.Datasets.get(ent.Datasets.public_identifier == dataset_identifier)

    q = ent.ExperimentDataset.delete().where(ent.ExperimentDataset.experiment == experiment.id,
                                         ent.ExperimentDataset.dataset == dataset.id)
    q.execute()

    ent.database.close()


def get_generated_content_by_identifier(identifier):
    ent.database.connect()

    query = ent.GeneratedContent.select().join(ent.Methods) \
        .switch(ent.GeneratedContent) \
        .join(ent.Experiments) \
        .switch(ent.GeneratedContent) \
        .join(ent.Datasets) \
        .where(ent.GeneratedContent.public_identifier == identifier)

    ent.database.close()

    return query

def create_experiment(identifier, description, type):
    ent.database.connect()
    entity = ent.Experiments.create(public_identifier=identifier, description=description, type=type, created_on=datetime.date.today())

    ent.database.close()

    return entity



# create_experiment("olol", "OMG", "dunno")


def create_generated_content(identifier):
    pass


def test():
    for e in get_experiments_all():
        print e.public_identifier


def test2():
    for e in get_experiment_by_identifier("demo_exp_march"):
        print e.experiment.public_identifier


def test_link(exp, data):
    link_dataset_to_experiment(exp, data)


def test_unlink(exp, data):
    unlink_dataset_to_experiment(exp, data)

# test2()

# test_link("demo_exp_march", "voom_normalized_read")

# test_unlink("demo_exp_march", "voom_normalized_read")
