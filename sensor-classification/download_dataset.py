from urllib.request import urlretrieve
from os.path import isfile

# The URL of the dataset and the local path it will be downloaded to
url = "http://archive.ics.uci.edu/ml/databases/synthetic_control/synthetic_control.data"
dataset_local_path = 'synthetic_control_data.txt'

# Only download the dataset if it is missing
if not isfile(dataset_local_path):
    urlretrieve(url, dataset_local_path)
    print("Download complete.")

else:
    print("Local copy of dataset found.")
