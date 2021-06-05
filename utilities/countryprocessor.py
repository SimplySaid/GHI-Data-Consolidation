import csv
import pandas as pd
import os
import country_converter as coco
from pathlib import Path

def countryprocessor (df, country_col_name):
    #Adds the Index. Index is used so AWS Glue can process headers
    if 'Index' in df:
        del df['Index']
    df.index.name = "Index"
    
    #Standardizes Country Name using Country Converter
    df[country_col_name] = df[country_col_name].apply(lambda x: coco.convert(names = x, to='name_short', not_found = None))

    #Adds ISO-3166 3 Digit Country Code - This will be used to join with other data sets
    df['Country Code'] = df[country_col_name].apply(lambda x: coco.convert(names = x, to = 'ISO3', not_found = None))

    return df

