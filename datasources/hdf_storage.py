import pandas as pd

from config import APP_CONFIG


def store_hdf(df, intern_identifier):
    store_path = APP_CONFIG["application_files_location"]
    store_name = APP_CONFIG["application_store_name"]

    join_path = store_path + store_name

    store = pd.HDFStore(join_path, complevel=9, complib='blosc')
    store[intern_identifier] = df
    store.close()

    return join_path


def retrieve_hdf(identifier, location):
    store = pd.HDFStore(location, complevel=9, complib='blosc')
    data = store[identifier]
    store.close()
    return data


def test():
    store_path = APP_CONFIG["application_files_location"]
    store_name = APP_CONFIG["application_store_name"]

    join_path = store_path + store_name

    store = pd.HDFStore(join_path, complevel=9, complib='blosc')

    test_frame = pd.read_csv(APP_CONFIG["demo_data_set_raw"], sep="\t", index_col=0)

    store["test"] = test_frame

    print store

    store.close()

    store = pd.HDFStore(join_path, complevel=9, complib='blosc')

    frame = store["test"]

    print frame.iloc[0, 0]





