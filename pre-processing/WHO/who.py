import country_converter as coco
import pandas as pd
import numpy as np
import csv
import glob

def parseWHO(filters, p_index, p_columns, p_values = ['val']):
    path = (r'input')
    filenames = glob.glob(path + "/*.csv")

    WHOData = []
    for filename in filenames:
        filename = pd.read_csv(filename)
        filename = filename.dropna(subset = ['Numeric'])
        #filename = filename.loc[filename['sex_name'] == sex_name]
        WHOData.append(filename)
        #print(filename)
    WHOData = pd.concat(WHOData, ignore_index=True)


    c = coco.CountryConverter()    
    WHOData['location'] = WHOData['COUNTRY (DISPLAY)'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))
    WHOData['iso3_location'] = WHOData['REGION (CODE)'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))
    WHOData = WHOData.rename(columns = {"GHO (DISPLAY)": "measure", "Numeric" : "val", "High" : "upper", "Low": "lower", "YEAR (CODE)" : "year"})

    #WHOData = WHOData.filter()
    for key, value in filters.items():
        WHOData = WHOData.loc[WHOData[key].isin(value)]

    #
    WHOData = WHOData.sort_values('year').groupby(['location', 'iso3_location', 'measure']).tail(1)

    #print(WHOData.head())

    WHOData.to_excel('test1.xlsx')

    data = pd.pivot_table(
        WHOData, 
        index=p_index, 
        values=p_values,
        columns=p_columns, aggfunc=[np.sum]
    )

    data = pd.DataFrame(data.to_records())
    data.columns = [hdr.replace("('sum', 'val',", "").replace("'", "").replace(",","") \
                 for hdr in data.columns]

    data.to_excel('WHO_HIV_2017_output.xlsx', index = False)

parseWHO(
    filters = {
        #'measure': ['DALYs (Disability-Adjusted Life Years)'],
        #'metric': ['Number']
        'year': ['2017'],
    },
    p_index = ['location', 'iso3_location'],
    p_columns = ['measure', 'year']
)
            