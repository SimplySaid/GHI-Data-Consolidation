from ddf_utils.factory.ihme import IHMELoader

# get loader and metadata
GBD = IHMELoader()
metadata = GBD.load_metadata()

# choose version: latest
version = metadata['version']['id'].max()

# choose locations: all but 'custom'
locations_md = metadata['location']
locations = locations_md[locations_md['id'] != 'custom']['id'].tolist()

# download risk data
zippath = GBD.bulk_download(
    version = version, # which version of the data to use
    out_dir = "../output/GHDx", # where to save the data
    context = 'cause', # GBD nomenclature for 'diseases'
    age = [2,3,4,5], # early neonatal, late neonatal, postneonatal, 1-4 years
    location = locations, # all locations
    sex = 3, # both male and female
    year = 2011, # year
    metric = 1, # number of cases
    measure = [2,3,4], # daly, yld, yll (no prevalence available)
    cause = [302, 322], # diarrhea, lower respiratory infections
    #rei_id = [136, 137], # non-exclusive breastfeeding, discontinued breastfeeding
    idsOrNames = 'both', # include plain text descriptions of the codes in the results file
)