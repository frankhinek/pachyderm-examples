import argparse
import os
import glob
import numpy as np
from keras.models import load_model

def load_trained_model(model_dir):
    # Generate a list of the files in the model directory
    input_paths = glob.glob(os.path.join(model_dir, "*.h5"))
    
    # Verify there is a model file in the model directory
    if len(input_paths) == 0:
        raise Exception("model_dir contains no model files")
    
    # This code assumes that only a single model file is present
    elif len(input_paths) > 1:
        raise Exception("model_dir contains more than one model file")
    
    # The model file is the single .h5 file in the model directory
    model_file = input_paths[0]

    # Returns a compiled model identical to the previously trained model
    return load_model(model_file)

def load_sensor_data(input_dir):
    # Generate a list of all of the CSV files in the input directory
    input_paths = glob.glob(os.path.join(input_dir, "*.csv"))

    # Verify there is a data file in the input directory
    if len(input_paths) == 0:
        raise Exception("input_dir contains no data files")
    
    # Variable to store the sensor measurement arrays
    sensor_data = {}

    # The data file is the single CSV file in the input directory
    for data_file in input_paths:
        # Read in the data from file and store in a NumPy array
        data = np.genfromtxt(data_file, delimiter=',',dtype=np.float32)
        
        # Get the filename.csv from the path
        filename = os.path.basename(data_file)

        # The data file should contain a single row
        # Reshape for model inference and add to the sensor measurements dict
        if data.ndim == 1:
            sensor_data[filename] = data.reshape(1, data.shape[0], 1)
        
        # If the data file contains multiple rows, reshape for model inference,
        # and append to the list of sensor measurements
        elif data.ndim == 2:
            for idx, row in enumerate(data):
                new_suffix = "-" + str(idx) + "."
                output_file = new_suffix.join(filename.split("."))
                sensor_data[output_file] = row.reshape(1, row.shape[0], 1)

    return sensor_data

def verify_directories(dirs):
    # Verify each directory exists
    for directory in dirs:
        if dirs[directory] is None or not os.path.exists(dirs[directory]):
            raise Exception("{0} does not exist".format(directory))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="path to folder containing sensor measurements")
    parser.add_argument("--model_dir", required=True, help="path to folder containing trained model")
    parser.add_argument("--output_dir", required=True, help="where to store inferences")
    a = parser.parse_args()

    verify_directories({"input_dir": a.input_dir,
                        "model_dir": a.model_dir,
                        "output_dir": a.output_dir})

    # Load the sensor measurements from file
    sensor_data = load_sensor_data(a.input_dir)

    # Load the previously trained model
    model = load_trained_model(a.model_dir)

    # For each sensor measurement series, predict the class, and save it to
    # an output file
    for output_file in sensor_data:
        save_path = os.path.join(a.output_dir, output_file)
        prediction = model.predict_classes(sensor_data[output_file])
        inferred_class = str(prediction[0])
        with open(save_path, 'w') as f:
            f.write(inferred_class)

main()
