import json

default_config_file = "PATH_TO_CONFIG_FILE"

with open(default_config_file) as config_file:
    APP_CONFIG = json.load(config_file)


