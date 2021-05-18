#PyCountry
import pandas as pd
import numpy as np
import os
import extractconfig

#Read Raw Data into Pandas Dataframe
extract_file_path = os.path.join(os.path.dirname(__file__), extractconfig.RAW_DATA_FILE)
raw_data = pd.read_csv(extract_file_path)

#Read ExtractList into List
extract_list_path = os.path.join(os.path.dirname(__file__),extractconfig.EXTRACT_LIST_FILE)
extract_list = np.genfromtxt(extract_list_path, delimiter = ';' , dtype = str)
extract_list = extract_list[:].tolist()

#Create Pivot for each file in ExtractList.xlsx
for e in extract_list:
    if (not(e in raw_data['Indicator Name'].values)):
        print (e + "does not exist in raw data file")
    else:
        temp_df = raw_data.loc[raw_data['Indicator Name'] == e]
        temp_df = temp_df.drop(['Indicator Name', 'Indicator Code'], axis = 1)

        output_path = os.path.join(os.path.dirname(__file__),extractconfig.OUTPUT_PATH + e + ".xlsx")
        temp_df.to_excel(output_path)





