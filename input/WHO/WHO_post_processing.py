import csv
import pandas as pd
import os
import country_converter as coco
from pathlib import Path

INPUT_FILE_PATH = "WHO_pentaho_output.csv"
OUTPUT_FILE_PATH = "../../output/WHO/WHO_FINAL_OUTPUT.csv"

path = os.path.join(os.path.dirname(__file__), INPUT_FILE_PATH)

print(path)

df = pd.read_csv(os.path.join(os.path.dirname(__file__), INPUT_FILE_PATH), encoding='latin-1')
        
#Adds the Index. Index is used so AWS Glue can process headers
if 'Index' in df:
    del df['Index']
df.index.name = "Index"

#Standardizes Country Name using Country Converter
df['Country'] = df['Country'].apply(lambda x: coco.convert(names = x, to='name_short', not_found = None))


#Adds ISO-3166 3 Digit Country Code - This will be used to join with other data sets
df['Country Code'] = df['Country'].apply(lambda x: coco.convert(names = x, to = 'ISO3', not_found = None))


#Outputs to target file
df.to_csv(os.path.join(os.path.dirname(__file__), OUTPUT_FILE_PATH), index=False)
