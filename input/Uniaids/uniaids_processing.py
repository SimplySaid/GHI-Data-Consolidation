import csv
import pandas as pd
import os
import country_converter as coco
from pathlib import Path

FOLDER_PATH = "../../output/Uniaids/"

path = os.path.join(os.path.dirname(__file__), FOLDER_PATH)
combined_file = pd.DataFrame()

for file in os.listdir(path):
    #Open each file in Folder Path
    if (file.endswith(".csv")):
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), FOLDER_PATH + file))
        
        #Sets Indicator to Name of File
        df['Indicator'] = Path(file).stem
        
        #Adds the Index. Index is used so AWS Glue can process headers
        if 'Index' in df:
            del df['Index']
        df.index.name = "Index"
        
        #Standardizes Country Name using Country Converter
        df['Country'] = df['Country'].apply(lambda x: coco.convert(names = x, to='name_short', not_found = None))

        #Adds ISO-3166 3 Digit Country Code - This will be used to join with other data sets
        df['Country Code'] = df['Country'].apply(lambda x: coco.convert(names = x, to = 'ISO3', not_found = None))

        #Outputs to target file
        df.to_csv(os.path.join(os.path.dirname(__file__), FOLDER_PATH + Path(file).stem + '.parquet'))

