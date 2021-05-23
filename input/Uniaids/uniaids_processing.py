import csv
import pandas as pd
import os
from pathlib import Path

FOLDER_PATH = "../../output/Uniaids/"

path = os.path.join(os.path.dirname(__file__), FOLDER_PATH)

for file in os.listdir(path):
    if (file.endswith(".csv")):
        df = pd.read_csv(os.path.join(os.path.dirname(__file__), FOLDER_PATH + file))
        df['Indicator'] = Path(file).stem
        df.index.name = "Index"
        df.to_csv(os.path.join(os.path.dirname(__file__), FOLDER_PATH + file), encoding='utf-8')

