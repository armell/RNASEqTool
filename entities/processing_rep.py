import entities as ent


def get_chart_from_db(chart_identifier):
    pass


def get_type_from_method(method_identifer):
    ent.database.connect()
    res = ent.Methods.get(ent.Methods.public_identifier == method_identifer)
    ent.database.close()

    return res.type.name


def save_outliers(mining_id, outlier_features):
    ent.database.connect()
    # mining_job = ent.Methods.get(ent.Mining.id == mining_id)

    data_to_insert = [
        {'mining': mining_id, 'feature': o.identifier, 'samples': o.samples, 'distance': o.distance, 'range': o.range}
        for o in outlier_features]

    with ent.database.transaction():
        ent.MiningResult.insert_many(data_to_insert).execute()

    ent.database.close()


def create_mining_task(mining_public_identifier, method_identifier, dataset_identifier, min_sample, min_distance=0.6,
                       experiment_identifier=""):
    ent.database.connect()

    method = ent.Methods.get(ent.Methods.public_identifier == method_identifier)
    dataset = ent.Datasets.get(ent.Datasets.public_identifier == dataset_identifier)
    experiment = ent.Experiments.get(ent.Experiments.public_identifier == experiment_identifier)
    mining_task = ent.Mining.create(public_identifier=mining_public_identifier, method=method.id, dataset=dataset.id,
                                    min_distance=min_distance, min_samples=min_sample, experiment=experiment.id)

    ent.database.close()

    return mining_task


def get_mining_task(mining_identifier):
    ent.database.connect()
    mining_result = ent.Mining.select().join(ent.Methods).switch(ent.Mining).join(ent.Datasets).where(
        ent.Mining.public_identifier == mining_identifier).get()
    ent.database.close()

    return mining_result


def get_existing_mining_task(method_identifier, distance, range):
    ent.database.connect()

    # res = ent.MiningResult().select().join(ent.Mining).where(ent.MiningResult.mining.contains())

    ent.database.close()


# print get_type_from_method("mad")

def get_all_tasks_for_experiment(experiment_identifier):
    ent.database.connect()

    res = ent.Mining.select().join(ent.Methods).switch(ent.Mining).join(ent.Experiments).where(
        ent.Experiments.public_identifier == experiment_identifier)

    ent.database.close()

    return res


def get_all_tasks():
    ent.database.connect()

    res = ent.Mining.select().join(ent.Methods)\
             .switch(ent.Mining)\
             .join(ent.Experiments)\
             .switch(ent.Mining)\
             .join(ent.Datasets).join(ent.DatasetTypes)

    ent.database.close()

    return res


def test():
    print get_mining_task("kmeans_outliers_test_upload_april_9cb8f2c4-3664-43ce-abf1-a1d052c2c181")


# test()


