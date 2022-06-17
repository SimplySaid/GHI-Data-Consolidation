from collections import OrderedDict

FILE_PATHS = {
    "INPUT_FOLDER" : "C:\\Users\\alex\\Documents\\Global Health Impact Organization\\GHI-Data-Consolidation\\pre-processing\\Generic\\input",
    "OUTPUT_FOLDER" : "C:\\Users\\alex\\Documents\\Global Health Impact Organization\\GHI-Data-Consolidation\\pre-processing\\Generic\\output\\",
    "CONFIG_FILE" : "C:\\Users\\alex\\Documents\\Global Health Impact Organization\\GHI-Data-Consolidation\\pre-processing\\Generic\\input\\config.ini"
}

CONFIGURATION_OPTIONS = {
    "COLUMN_MAPPINGS": {
        "location" : "",
        "aggregation_columns" : "",
        "year" : None,
        "use_most_recent_year_if_missing": False
    },
    "PIVOT_DATA" : {
        "enable" : False,
        "pivot_column": "",
        "aggregation_column" : "", 
    },
    "CITATIONS" : {
        "enable": False,
        "source_name" : "",
        "source_download_link" : "",
        "source_year" : None,
    },
}
