import argparse
import os
import glob
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras import utils

def create_model(layer_size=10, n_classes=6, input_shape=(60, 1)):
    model = Sequential()
    model.add(LSTM(layer_size, input_shape=input_shape))
    model.add(Dense(n_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model

def load_training_data(input_dir):
    # Generate a list of all of the CSV files in the input directory
    input_paths = glob.glob(os.path.join(input_dir, "*.csv"))

    # Verify there is a data file in the input directory
    if len(input_paths) == 0:
        raise Exception("input_dir contains no data files")
    
    # This code assumes that only a single CSV file is present
    elif len(input_paths) > 1:
        raise Exception("input_dir contains more than one data file")
    
    # The data file is the single CSV file in the input directory
    data_file = input_paths[0]

    # Use NumPy's genfromtxt method read in the data file and store as an array
    control_data = np.genfromtxt(data_file, delimiter=',',dtype=np.float32)

    # Reshape the NumPy array to use for batch processing
    control_data = control_data.reshape(600, 60, 1)

    # Generate labels for the time series.  The first 100 rows are category 1, the second 100 are category 2, and so on.
    # We'll use labels 0 - 5 to represent categories 1 - 6 (i.e., 0-based indexing)
    labels = np.array([(i // 100) for i in range(600)], ndmin=2).T

    return control_data, labels

def normalize_data(dataset):
    # Normalize the dataset with a mean of 0 and standard deviation of 1
    series_mean = dataset.mean(axis=1, keepdims=True)
    series_std = dataset.std(axis=1, keepdims=True)

    return (dataset - series_mean) / series_std

def verify_directories(dirs):
    # Verify each directory exists
    for directory in dirs:
        if dirs[directory] is None or not os.path.exists(dirs[directory]):
            raise Exception("{0} does not exist".format(directory))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True, help="path to folder containing sensor data")
    parser.add_argument("--output_dir", required=True, help="where to store trained model")
    parser.add_argument("--max_epochs", type=int, default=75, help="number of training epochs")
    a = parser.parse_args()

    verify_directories({"input_dir": a.input_dir,
                        "output_dir": a.output_dir})
    
    # Load the time series dataset from file
    control_data, labels = load_training_data(a.input_dir)

    # Normalize the dataset with a mean of 0 and standard deviation of 1
    control_data_norm = normalize_data(control_data)

    # Split data and create train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        control_data, labels, test_size=0.25, random_state=37)

    # Converts train and test set labels to a binary class matrix
    y_train = utils.to_categorical(y_train)
    y_test = utils.to_categorical(y_test)
    
    # Create LSTM classification model
    model = create_model()

    # Trains the model for the specified number of epochs
    model.fit(X_train, y_train, batch_size=10, epochs=a.max_epochs, verbose=0)
    
    # Save the trained model
    save_path = os.path.join(a.output_dir, "model.h5")
    model.save(save_path)

main()
