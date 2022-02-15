import country_converter as coco
import pandas as pd
import numpy as np
import csv
import glob

def parseIHME(filters, p_index, p_columns, p_values = ['val']):
    # CountryConcord = pd.read_csv(r'input\CountryConcordIHME.csv',encoding="ISO-8859-1")
    # SeriesConcord = pd.read_excel(r'input\SeriesConcordIHME.xlsx')

    path = (r'input')
    filenames = glob.glob(path + "/*.csv")

    GBDData = []
    for filename in filenames:
        filename = pd.read_csv(filename)
        filename = filename.dropna(how='any')
        #filename = filename.loc[filename['sex_name'] == sex_name]
        GBDData.append(filename)
        #print(filename)
    GBDData = pd.concat(GBDData, ignore_index=True)


    c = coco.CountryConverter()    
    GBDData['location'] = GBDData['location'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))
    GBDData['iso3_location'] = GBDData['location'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))

    #GBDData = GBDData.filter()
    for key, value in filters.items():
        GBDData = GBDData.loc[GBDData[key].isin(value)]

    GBDData = GBDData.sort_values('year').groupby(['location', 'iso3_location', 'sex', 'age', 'measure', 'metric', 'cause']).tail(1)

    GBDData.to_excel('test1.xlsx')

    data = pd.pivot_table(
        GBDData, 
        index=p_index, 
        values=p_values,
        columns=p_columns, aggfunc=[np.sum]
    )

    data = pd.DataFrame(data.to_records())
    data.columns = [hdr.replace("('sum', 'val',", "").replace("'", "").replace(",","") \
                    for hdr in data.columns]

    data.to_excel('2015_output.xlsx', index = False)

parseIHME(
    filters = {
        #'measure': ['DALYs (Disability-Adjusted Life Years)'],
        #'metric': ['Number']
        'year': ['2015'],
    },
    p_index = ['location', 'iso3_location'],
    p_columns = ['cause', 'age', 'measure']
)
            