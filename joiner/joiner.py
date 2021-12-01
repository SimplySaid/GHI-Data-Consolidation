import country_converter as coco
import pandas as pd
import numpy as np
import csv
import glob

path = (r'input')
filenames = glob.glob(path + "/*.xlsx")

merged_data = pd.read_excel(path + '''/base.xlsx''', engine='openpyxl')
#merged_data = None

for filename in filenames:
    if 'base' or '~$' in filename:
        continue

    print(filename)

    file = pd.read_excel(filename, engine='openpyxl', mode = 'a')
    merged_data = pd.merge(merged_data, file,
        how = "left",
        on=["iso3_location"]
    )

merged_data.to_excel('output.xlsx', index = False)
