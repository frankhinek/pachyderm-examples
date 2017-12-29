# Sensor Classification with an LSTM RNN Model

Classification of sensor data using an LSTM recurrent neural network model.

A `Makefile` has been included to simply the process of deploying and testing
the Pachyderm workflow associated with this demo.

To create the repositories and pipelines for training the LSTM RNN model and
load the training data run:

    $ make training

To create the repositories and pipelines for performing inference using the
trained model run:

    $ make inference

In order to test inference you can use `pachctl` to upload individual sensor
observations to the `sensor_measurements` repository.  The `sensor_inference`
pipeline will automatically create a job to use the trained model to infer
whether the measurements indicate a normal, warning, or critical state.

To make this simple to test run `make split-csv` and then upload one of the
CSV files using the following command:

    $ pachctl put-file sensor_measurements master -c -f 100.csv

After a few seconds the job should complete and there should be a corresponding
`100.csv` in the `sensor_inference` repository that contains the inferred
class.  You can view the output with the following command:

    $ pachctl get-file sensor_inference master 100.csv
