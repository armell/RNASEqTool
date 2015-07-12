from datetime import date

import entities as ent
from config import APP_CONFIG


def get_list_of_methods():
    ent.database.connect()
    res = ent.Methods.select().join(ent.MethodTypes)
    ent.database.close()
    return res


def get_list_of_methods_by_type(method_type):
    ent.database.connect()
    res = ent.Methods.select().join(ent.MethodTypes).where(ent.Methods.type.name == method_type)


def get_list_of_packages_by_method(method_identifier):
    ent.database.connect()
    res = ent.MethodPackage().select().join(ent.Methods).join(ent.MethodTypes).switch(ent.MethodPackage).join(
        ent.Packages).where(
        ent.Methods.public_identifier == method_identifier)
    ent.database.close()

    return res


def get_method_for_package(package_identifier):
    ent.database.connect()
    res = ent.MethodPackage().select().join(ent.Methods).switch(ent.MethodPackage).join(ent.Packages).get(
        ent.Packages.public_identifier == package_identifier)
    ent.database.close()

    return res


def get_method(method_identifier):
    ent.database.connect()

    res = ent.Methods.get(ent.Methods.public_identifier == method_identifier)

    ent.database.close()

    return res


def get_package(package_identifier):
    ent.database.connect()

    res = ent.Packages.get(ent.Packages.public_identifier == package_identifier)

    ent.database.close()

    return res


def get_package_by_name_and_version(name, version):
    ent.database.connect()

    try:
        res = ent.Packages.get(ent.Packages.name == name and ent.Packages.version == version)
    except ent.Packages.DoesNotExist:
        print version.replace(".", "_")
        res = ent.Packages.create(name=name, version=version, public_identifier=name + "_" + version.replace(".", "_"),
                                  description="Not available", language="R/Bioconductor", added_on=date.today(),
                                  url_source=APP_CONFIG["domain"] + "/static/app/index.html#/view2/help")

    ent.database.close()

    return res


# get_list_of_methods()

def test():
    for e in get_list_of_packages_by_method("deseq"):
        print e.package.name + " - - " + e.package.reference


def test_pack_by_name():
    print get_package_by_name_and_version("edger", "3.8.6").public_identifier


# test_pack_by_name()