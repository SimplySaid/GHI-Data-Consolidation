import country_converter as coco
import pandas as pd
import numpy as np
import csv
from glob import glob
import os


# Shell (Base Model)
shell_path = (r'base')

# Data Files
data_path = (r'data')

#Stores all data file types in a list
filenames = glob(data_path + "/*.xlsx") + glob(data_path + "/*.csv") + glob(data_path + "/*.xls")

for filename in filenames:
    
    # Gets extension of file
    ext = os.path.splitext(filename)[1]
    
    # Read data files as dataframe based on extension
    if ext == '.csv':
        file = pd.read_csv(filename, skiprows=1)
    elif ext == '.xlsx' or ext == '.xls':
        file = pd.read_excel(filename, skiprows=1)
    else:
        raise RuntimeError('File extension not recognized')

    

    