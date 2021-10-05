import csv
import pandas as pd
import os
import country_converter as coco
from pathlib import Path

INPUT_FILE_PATH = "./GPRM Source.csv"
OUTPUT_FILE_PATH = "../../output/GPRM/GPRM_final_output.parquet"

path = os.path.join(os.path.dirname(__file__), INPUT_FILE_PATH)

print(path)

df = pd.read_csv(os.path.join(os.path.dirname(__file__), INPUT_FILE_PATH))
        
#Adds the Index. Index is used so AWS Glue can process headers
if 'Index' in df:
    del df['Index']
df.index.name = "Index"

c = coco.CountryConverter()

#print(df.head())

#Standardizes Country Name using Country Converter
df['Country'] = df['Country'].apply(lambda x: c.convert(names = x, to='name_short', not_found = None))


#Adds ISO-3166 3 Digit Country Code - This will be used to join with other data sets
df['Country Code'] = df['Country'].apply(lambda x: c.convert(names = x, to = 'ISO3', not_found = None))


#Outputs to target file
df.to_parquet(os.path.join(os.path.dirname(__file__), OUTPUT_FILE_PATH), index=False)
