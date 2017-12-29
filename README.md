# Pachyderm Demos

This repository contains examples of deep learning pipelines deployed on
[Pachyderm](http://pachyderm.io/).

A `Makefile` has been included to simplify the process of deploying Pachyderm
locally on Minikube.  First, install [Docker](http://docker.io/),
[Minikube](https://github.com/kubernetes/minikube), and [pachctl](http://docs.pachyderm.io/en/latest/getting_started/local_installation.html#pachctl)
on your macOS or Linux system.  Then run:

    $ make deploy

After a minute or two you should have both Minikube and Pachyderm deployed
locally.  Then run `pachctl port-forward &` before proceeding with the demos.

## Sensor Classification with an LSTM RNN Model

Classification of sensor data using an LSTM recurrent neural network model.

[Sensor Classification](https://github.com/frankhinek/pachyderm-examples/tree/master/sensor-classification)
