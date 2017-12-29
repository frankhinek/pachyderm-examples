import re
import numpy as np

def load_X(X_data_path):
    X_data = []
    
    # Open the file for reading
    file = open(X_data_path, 'r')
    
    # Read the dataset from disk
    X_data.append(
        [np.array(series, dtype=np.float32) for series in [
            re.split(" +", row.strip("\n")) for row in file
        ]]
    )
    file.close()

    return np.array(X_data)

dataset_local_path = 'synthetic_control_data.txt'

# Load the time series dataset from file
control_data = load_X(dataset_local_path)

# Save time series dataset to CSV
np.savetxt("synthetic_control_data.csv", control_data[0], fmt="%2.5f", delimiter=",")

# import pandas as pd
# df = pd.DataFrame(control_data[0])
# for idx, row in df.iterrows():
#     import pdb; pdb.set_trace()
# df.to_csv("synthetic_control_data.csv", header=None, index=None)
