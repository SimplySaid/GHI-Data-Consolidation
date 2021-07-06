import csv
import pandas as pd
import os
import country_converter as coco
from pathlib import Path

def correct_country (df, country_col_name):    
    #Standardizes Country Name using Country Converter
    df[country_col_name] = df[country_col_name].apply(lambda x: coco.convert(names = x, to='name_short', not_found = None))

    return df


def add_iso_code (df, country_col_name):
    #Adds ISO-3166 3 Digit Country Code - This will be used to join with other data sets
    df['Country Code'] = df[country_col_name].apply(lambda x: coco.convert(names = x, to = 'ISO3', not_found = None))

    return df