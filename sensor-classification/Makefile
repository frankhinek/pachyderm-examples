DOCKER_BINARY=docker
DOCKER_FILE=Dockerfile
REGISTRY_HOST=docker.io
USERNAME=frankhinek
REPOSITORY=pachydemo
TAG=sensor-rnn
IMAGE=$(REGISTRY_HOST)/$(USERNAME)/$(REPOSITORY)

clean:
	pachctl delete-pipeline sensor_model --delete-jobs --delete-repo
	pachctl delete-pipeline sensor_inference --delete-jobs --delete-repo
	pachctl delete-repo sensor_training_data 
	pachctl delete-repo sensor_measurements 

create-training-pipeline:
	pachctl create-pipeline -f sensor_train_model.json

create-inference-pipeline:
	pachctl create-pipeline -f sensor_inference.json

create-inference-repo:
	pachctl create-repo sensor_measurements

docker-build:
	$(DOCKER_BINARY) build --pull -t $(IMAGE):$(TAG) --no-cache --rm=true -f $(DOCKER_FILE) .

get-data:
	python download_dataset.py
	python convert_to_csv.py

help:
	@cat Makefile

inference: create-inference-repo create-inference-pipeline

load-training-data: get-data
	pachctl create-repo sensor_training_data
	pachctl put-file sensor_training_data master -c -f synthetic_control_data.csv

push:
	$(DOCKER_BINARY) push $(IMAGE):$(TAG)

split-csv:
	python split_csv.py

training: load-training-data create-training-pipeline
