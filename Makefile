check-kubectl:
	# check that kubectl is installed
	which kubectl

clean:
	minikube delete

deploy: launch-kube
	pachctl deploy local
	# wait for the pachyderm to come up
	until ./deploy/check-pachyderm.sh app=pachd; do sleep 5; done

help:
	@cat Makefile

launch-kube: check-kubectl
	deploy/start-minikube.sh
