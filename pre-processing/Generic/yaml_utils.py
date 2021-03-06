import generic_processing_config as config_options
import yaml
import copy

DEFAULT_CONFIG_OPTIONS = config_options.CONFIGURATION_OPTIONS

def generate_config_file(fileNames, CONFIG_OPTIONS = None):
    output_json = dict()
    
    if CONFIG_OPTIONS:
        output_json = CONFIG_OPTIONS
    else:
        for file in fileNames:
            if CONFIG_OPTIONS == None:
                output_json[file] = DEFAULT_CONFIG_OPTIONS
            else:
                output_json[file] = CONFIG_OPTIONS

    yaml.Dumper.ignore_aliases = lambda *args : True
    with open(config_options.FILE_PATHS['CONFIG_FILE'], 'w') as outfile:
        yaml.dump(output_json, outfile)

# Know this code is bad, didn't have time to write it properly
def generate_config_options(df):
    config_options = copy.deepcopy(DEFAULT_CONFIG_OPTIONS)
    file_headers = list(df)

    possible_location_names = ["location_name", "country_nane", "country", "location"]
    matching_location_names = [b for b in file_headers if b.lower() in (a.lower() for a in possible_location_names)]
    if len(matching_location_names) > 0:
        config_options["COLUMN_MAPPINGS"]["location"] = matching_location_names[0]
    
    possible_aggregation_columns = ["val", "total", "sum", "value"]
    matching_aggregation_columns = [b for b in file_headers if b.lower() in (a.lower() for a in possible_aggregation_columns)]
    if len(matching_aggregation_columns) > 0:
        config_options["COLUMN_MAPPINGS"]["aggregation_columns"] = matching_aggregation_columns[0]

    if "year" in file_headers:
        config_options["COLUMN_MAPPINGS"]["year"] = str(df.year.max())
        config_options["CITATIONS"]["source_year"] = str(df.year.max())
    return config_options

def read_yaml():
    try:
        with open(config_options.FILE_PATHS["CONFIG_FILE"], 'r') as f:
            yaml_to_json = yaml.safe_load(f)
        return yaml_to_json
    except:
        return None
