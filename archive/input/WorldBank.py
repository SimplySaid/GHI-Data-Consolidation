from ddf_utils.factory.worldbank import WorldBankLoader
import pandas as pd

w = WorldBankLoader()

md = w.load_metadata()
md.head()

w.bulk_download(
    dataset = 'WDI', 
    out_dir = '../output/WorldBank'
)

# df = pd.DataFrame(data=md)
# df = (df.T)
# df = df.transpose()

# df.to_excel('metadata.xlsx')