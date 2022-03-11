import country_converter as coco
import pandas as pd
import numpy as np
import csv
from glob import glob
import os

data_path = (r'input')

filenames = glob(data_path + "\[!~]*.xlsx") + glob(data_path + "\[!~]*.csv") + glob(data_path + "\[!~]*.xls")
output = pd.DataFrame()

for filename in filenames:
    # Gets extension of file
    ext = os.path.splitext(filename)[1]
    
    # Read data files as dataframe based on extension
    if ext == '.csv':
        file = pd.read_csv(filename)
    elif ext == '.xls':
        file = pd.read_excel(filename)
    elif ext == '.xlsx':
        file = pd.read_excel(filename, engine='openpyxl')
    else:
        raise RuntimeError('File extension not recognized')

    # Checks if first row contains includes, the re-read the dataframe starting from second row
    # Definitely not the most elegant way to do this
    file_headers = list(file)
    if 'include' in file_headers:
        idx_to_include = []
        # Grabs the indexes of headers with "include"
        for x in range (0, len(file_headers)):
            if file_headers[x] == "include" or file_headers[x].startswith('include') and file_headers[x][-1].isdigit():
                idx_to_include.append(x)
        
        # Skips the first row with includes, and only takes columns with includes (based on indexes)
        if ext == '.csv':
            file = pd.read_csv(filename, usecols=idx_to_include, skiprows=1)
        elif ext == '.xls':
            file = pd.read_excel(filename, usecols=idx_to_include, skiprows=1)
        elif ext == '.xlsx':
            file = pd.read_excel(filename, usecols=idx_to_include, engine='openpyxl', skiprows=1)
        else:
            raise RuntimeError('File extension not recognized')

    # If Location column not found, user can enter
    while "iso3_location" not in file.columns:
        location_column_name = input("ISO3 location not found for %s, please input exact column name or 'skip' to continue. \n If you put column indexes in your file, make sure you included iso3_location\n" % (filename))
        if location_column_name == "skip":
            print("Skipping " + filename)
            continue
        elif location_column_name in file.columns:
            file.rename(columns = {location_column_name, 'iso3_location'})

    # First file serves as the "base_file"
    if output.empty:
        output = file
    else:
        output = pd.merge(output, file,
            how = "outer", # Can set to left if a base file is designated
            on=["iso3_location"]
        )

output_file_name = input("Enter name of output file without file extension\n")
output.to_excel(output_file_name + '.xlsx', index = False)
