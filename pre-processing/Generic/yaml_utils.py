import generic_processing_config as config
import yaml
import json

CONFIG_OPTIONS = config.CONFIGURATION_OPTIONS

def generate_config_file(fileNames):
    output_json = dict()
    
    for file in fileNames:
        output_json[file] = CONFIG_OPTIONS

    yaml.Dumper.ignore_aliases = lambda *args : True
    with open(config.FILE_PATHS['CONFIG_FILE'], 'w') as outfile:
        yaml.dump(output_json, outfile)
    
def read_yaml():
    yaml_to_json = yaml.load(config.FILE_PATHS['CONFIG_FILE'])
    return yaml_to_json