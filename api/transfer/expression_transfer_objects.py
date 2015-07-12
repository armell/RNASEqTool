from config import APP_CONFIG

# Resources have different representations
# These classes sends the appropriate representation
# Heavy use of JSON for now
class ApiView(object):
    def __init__(self):
        self.entity = None

    def to_json(self):
        pass

    def to_csv(self):
        return self.to_json()

    def get_collection_header(self, collection):
        return {"collection": {
            "href": APP_CONFIG["application_base_url"] + str.format("/expression/{0}/", collection)
        }}

    def get_collection_data(self):
        pass


class ExperimentsView(ApiView):
    def __init__(self, entity_collection):
        self.entity = entity_collection

    def get_collection_data(self):
        for e in self.entity:
            print(e.public_identifier)

        return {"items": [
            {"href": APP_CONFIG["application_base_url"] + str.format("/expression/experiment/{0}", e.public_identifier),
             "data": {"public_identifier": e.public_identifier, "description": e.description, "experiment_type": e.type,
                      "created_on": str(e.created_on)}} for e in self.entity]}

    def to_json(self):
        data = self.get_collection_data().copy()
        header = self.get_collection_header("experiments")
        print(data)
        return dict(header, **data)


class ExperimentView(ApiView):
    def __init__(self, entity):
        self.entity = entity

    def to_json(self):
        datasets = []
        e = None
        for e in self.entity:
            print("append dataset")
            d = e.dataset
            e = e.experiment
            if d is not None:
                datasets.append(SummaryDatasetView(d).to_json())

        if e is not None:
            experiment = {"experiment": e.public_identifier, "description": e.description,
                          "created_on": str(e.created_on), "experiment_type": e.type, "datasets": datasets}

        # print(experiment)
        return experiment


class DatasetView(ApiView):
    def __init__(self, entity):
        self.entity = entity

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/dataset/{0}",
                                                                        self.entity.dataset.public_identifier),
                "data": {"public_identifier": self.entity.dataset.public_identifier,
                         "type": self.entity.dataset.type.name, "experiment": self.entity.experiment.public_identifier,
                         "package": PackageView(self.entity.dataset, "package").to_json()}}


class SummaryDatasetView(ApiView):
    def __init__(self, entity):
        self.entity = entity

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/dataset/{0}",
                                                                        self.entity.public_identifier),
                "data": {"public_identifier": self.entity.public_identifier,
                         "type": self.entity.type.name, "package": PackageView(self.entity, "package").to_json()}}


class JustDatasetView(ApiView):
    def __init__(self, entity):
        self.entity = entity

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/dataset/{0}",
                                                                        self.entity.public_identifier),
                "data": {"public_identifier": self.entity.public_identifier,
                         "type": self.entity.type.name}}


# dataset, experiment, method, package, threshold, output (genes for now...)
class JobView(ApiView):
    def __init__(self, entity):
        self.entity = entity

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/stream/{0}",
                                                                        self.entity.public_identifier),
                "data": {"public_identifier": self.entity.public_identifier}}


class MethodView(ApiView):
    def __init__(self, entity, packages=None):
        self.entity = entity
        self.packages = packages

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/method/{0}",
                                                                        self.entity.public_identifier),
                "data": {"public_identifier": self.entity.public_identifier, "name": self.entity.name,
                         "updated": str(self.entity.updated), "type_name": self.entity.type.name,
                         "description": self.entity.description}}


class PackageView(ApiView):
    def __init__(self, entity, package_method):
        self.entity = entity
        self.package_method = package_method

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/{0}/{1}",
                                                                        self.package_method,
                                                                        self.entity.package.public_identifier),
                "data": {"public_identifier": self.entity.package.public_identifier,
                         "language": self.entity.package.language, "version": self.entity.package.version,
                         "url_source": self.entity.package.url_source, "reference": self.entity.package.reference,
                         "name": self.entity.package.name}}


class SummaryPackageView(ApiView):
    def __init__(self, entity):
        self.entity = entity

    def to_json(self):
        return {"href": APP_CONFIG["application_base_url"] + str.format("/expression/method/{0}/{1}",
                                                                        self.entity.method.public_identifier,
                                                                        self.entity.package.public_identifier),
                "data": {"public_identifier": self.entity.package.public_identifier,
                         "language": self.entity.package.language, "version": self.entity.package.version,
                         "url_source": self.entity.package.url_source, "reference": self.entity.package.reference,
                         "name": self.entity.package.name}}


class TaskView(ApiView):
    def __init__(self, entity):
        self.entity = entity


    def to_json(self):
        return {
            "href": APP_CONFIG["application_base_url"] + str.format("/expression/task/{0}",
                                                                    self.entity.public_identifier),
            "data": {"public_identifier": self.entity.public_identifier,
                     "distance": self.entity.min_distance,
                     "samples": self.entity.min_samples,
                     "method": MethodView(self.entity.method).to_json(),
                     "dataset": JustDatasetView(self.entity.dataset).to_json(),
                     "job": JobView(self.entity).to_json()}}

