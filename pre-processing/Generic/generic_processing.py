'''
Features:
Country Conversion / Standardization
Year Consolidation - Use most recent data for country up to X year 

'''

'''
Data MUST contain either contain a column called location_name or iso3_location
Inputs:
Year: Filters data by this year, or uses this as most recent year if Year Consolidation is enabled
Year Consolidation: True/False (If true, then uses this year for year consolidation)
'''

import country_converter as coco
import pandas as pd
import numpy as np
import csv
from glob import glob
import os


def process_generic_data(year = None, year_consolidation = False):

    data_path = (r'input')

    filenames = glob(data_path + "\[!~]*.xlsx") + glob(data_path + "\[!~]*.csv") + glob(data_path + "\[!~]*.xls")

    for filename in filenames:
        
        ext = os.path.splitext(filename)[1]

        if ext == '.csv':
            file = pd.read_csv(filename)
        elif ext == '.xls':
            file = pd.read_excel(filename)
        elif ext == '.xlsx':
            file = pd.read_excel(filename, engine='openpyxl')
        else:
            raise RuntimeError('File extension not recognized')

        file.columns = file.columns.str.lower()
        #file = pd.DataFrame()
        c = coco.CountryConverter() 

        file_headers = list(file)
        if 'location_name' in file_headers:
            file['location_name'] = file['location_name'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))
            file['iso3_location'] = file['location_name'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))
        elif 'iso3_location' in file_headers:
            file['location'] = file['iso3_location'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))
            file['iso3_location'] = file['iso3_location'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))
        else:
            print("Critical Error: Missing location_name or iso3_location column, teminating script")
            return

        file_headers = list(file)
        if 'year' in file_headers:
            if year_consolidation:
                if year != None:
                    file = file.loc[file['year'] <= year] 

            else:
                if year == None:
                    year = file['year'].max()

                file = file.loc[file['year'] == year]

            file_headers.remove('year')
            #print(file_headers)
            file = file.sort_values('year').groupby('location_name').tail(1)
            # file.loc[file.groupby(file_headers).year.idxmax()]

        file = file.sort_values('location_name')

        file.to_excel('./output/' + filename.split('\\')[1] + '_output.xlsx', index = False)

process_generic_data(None, True)