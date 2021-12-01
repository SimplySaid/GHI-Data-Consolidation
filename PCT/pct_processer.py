import pandas as pd
import time
import csv
import json
import re
import numpy as np
import os
import country_converter as coco



# for col in df:
#     if ['ISO3', 'Countries', 'Status of Mass Drug Administration', 'Type of Mass Drug Administration', 'Mapping status'] == col:
#         continue
    
#     for index, row in df[col].iteritems():
#         if(index == 0):
#             continue
    
#     data = {
#         'iso3' : row['ISO3'],
#         'country_name': row['countries'],
#         'indicator': col,
#         'value': row[]
#     }

#Function to process lf datset - requires you to unmerge all the cells and replace the merged cells with each individual value
def process_lf(df):
    indicators = list(df.columns.values)
    years = df.loc[0, :].values.tolist()


    output = []

    for index, row in df.iterrows():
        if index == 0:
            continue

        row = list(row.items())

        for i in range (2, len(row)):
            if (not pd.isnull(row[i][1])) and (not str(row[i][1]).isspace()):
                row_data = {
                    'country': row[1][1],
                    #'ISO3': row[0][1],
                    'year': years[i],
                    'cause': re.sub(r'.\d+$', '', indicators[i]),
                    'val': row[i][1] 
                }

                output.append(row_data)

    json_output = json.dumps(output)
    temp_df = pd.read_json(json_output)
    return temp_df
    #temp_df.to_csv('lf_output.csv', index=False)

#Function to process SCH and STH    
def process_SCH_STH(df):
    indicators = list(df.columns.values)
    output = []

    for index, row in df.iterrows():
        row = list(row.items())

        for i in range (3, len(row)):
            if indicators[i] == 'country_code':
                continue
            if (not pd.isnull(row[i][1])) and (not str(row[i][1]).isspace()):
                row_data = {
                    'country': row[1][1],
                    #'ISO3' : row[0][1],
                    'year' : row[2][1],
                    'cause': indicators[i],
                    'val' : row[i][1]
                }
                output.append(row_data)

    json_output = json.dumps(output)
    temp_df = pd.read_json(json_output)
    return temp_df   


lf = pd.read_excel('.\input\lf_data_modified.xlsx', engine = 'openpyxl')
sch = pd.read_excel('.\input\SCH_data.xlsx', engine = 'openpyxl')
sth = pd.read_excel('.\input\STH_data.xlsx', engine = 'openpyxl')

lf_parsed = process_lf(lf)
lf_parsed['disease'] = 'Lymphatic filariasis'

sch_parsed = process_SCH_STH(sch)
sch_parsed['disease'] = 'Schistosomiasis'

sth_parsed = process_SCH_STH(sth)
sth_parsed['disease'] = 'Soil-transmitted helminth'

all_parsed_data = pd.concat([lf_parsed, sch_parsed, sth_parsed], ignore_index = True, axis = 0)

c = coco.CountryConverter()

#Standardizes Country Name using Country Converter
all_parsed_data.insert(0, 'location', all_parsed_data['country'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None)))

#Adds ISO-3166 3 Digit Country Code - This will be used to join with other data sets
all_parsed_data.insert(1, 'iso3_location', all_parsed_data['location'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None)))

all_parsed_data = all_parsed_data.drop('country', 1)

#Adding filter
all_parsed_data = all_parsed_data.loc[all_parsed_data['year'].isin(['2017'])]

#Getting unique grouping
all_parsed_data = all_parsed_data.sort_values('year').groupby(['location', 'iso3_location', 'cause', 'disease']).tail(1)


data = pd.pivot_table(
    all_parsed_data, 
    index=['location', 'iso3_location'], 
    values=['val'],
    columns=['cause', 'disease'], aggfunc=[np.sum]
)

data = pd.DataFrame(data.to_records())
data.columns = [hdr.replace("('sum', 'val',", "").replace("'", "").replace(",","") \
                for hdr in data.columns]

#Outputs to target file
data.to_excel(os.path.join(os.path.dirname(__file__), 'pct_output.xlsx'), index=False)