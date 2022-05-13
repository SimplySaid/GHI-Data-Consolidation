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
import cmd
import click

# Default column names and required
DEFAULT_COLUMN_NAMES = {
    'location_name': True,
    'value': True,
    'year' : False,
}

def fix_column_headers(df):
    df_column_headers = list(df.columns.values)

    for key, value in DEFAULT_COLUMN_NAMES.items():
        # for header in df_column_headers:
        #     if header.lower() == key:
        #         df.rename(columns={
        #             header: key
        #         })
        #         df_column_headers = list(df.columns.values)
        #         break
        if key in df_column_headers:
            continue
        else:
            user_column_header = None
                
            while user_column_header not in df_column_headers or (user_column_header == 'SKIP' and value == False):
                if user_column_header == 'SKIP':
                    user_column_header = input(f"{key} is mandatory cannot be skipped")        
                else:
                    user_column_header = input(f"Can't find {key}, please enter the equivalent column or SKIP to ignore (case sensitive)")        
            
            if user_column_header != 'SKIP':
                df.rename(columns={
                        user_column_header: key
                    })

def get_citations():
    source_name = input("What is the source name? (e.g., The World Bank: DataBank [Internet]. Washington D.C: The World Bank Group")
    source_download_link = input("What is the source link")
    source_year = input("What year do you want to extract? Enter 9999 for most recent available year by country")
    source = "Reference:%s;%s \n\nSource Link:%s" % (source_name, source_year, source_download_link)

    return source

def pivot_normalized_data(df, columns, index):
    try:
        df = pd.pivot_table(
            df, 
            values = 'value',
            columns = columns,
            index = index
        )
    except:
        print('Error Pivoting Data')

    return df

def process_generic_data(year = None, year_consolidation = False):
    data_path = (r'input')

    filenames = glob(data_path + "\[!~]*.xlsx") + glob(data_path + "\[!~]*.csv") + glob(data_path + "\[!~]*.xls")

    for filename in filenames:

        # Generate Inputs
        print("Processing" + " " + filename + ":")
        # citation = get_citations()

        ext = os.path.splitext(filename)[1]

        if ext == '.csv':
            file = pd.read_csv(filename, encoding='latin-1')
        elif ext == '.xls':
            file = pd.read_excel(filename)
        elif ext == '.xlsx':
            file = pd.read_excel(filename, engine='openpyxl')
        else:
            raise RuntimeError('File extension not recognized')

        file.columns = file.columns.str.lower()
        file = fix_column_headers(file)

        normalized = True # Need to create user input for this

        #file = pd.DataFrame()
        c = coco.CountryConverter() 

        file_headers = list(file)
        if 'location_name' in file_headers:
            try: 
                file['location_name'] = file['location_name'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))
                file['iso3_location'] = file['location_name'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))
            except:
                print("Error Occured: Check the file for footers")
        elif 'iso3_location' in file_headers:
            file['location_name'] = file['iso3_location'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))
            file['iso3_location'] = file['iso3_location'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))
        else:
            print("Critical Error: Missing location_name or iso3_location column, teminating script")
            return

        file_headers = list(file)

        # Need to write year hander for this.. should we use the most recent year with data? a static year with user input?
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

        file = pivot_normalized_data(
            file,
            columns = ['test'],
            val = 'val',
            index = ['location_name', 'iso3_location', 'year']
        )

        file = file.sort_values('location_name')

        file.to_excel('./output/' + filename.split('\\')[1] + '_output.xlsx', index = False)

process_generic_data(None, True)