#!/usr/bin/env bash

set -Ee

# Parse flags
VERSION=v1.8.0
while getopts ":v:" opt; do
  case "${opt}" in
    v)
      VERSION="v${OPTARG}"
      ;;
    \?)
      echo "Invalid argument: ${opt}"
      exit 1
      ;;
  esac
done

if [ "$(uname)" == "Darwin" ]; then
    # Mac OS X platform
    minikube start --vm-driver=hyperkit --kubernetes-version="${VERSION}"

elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # GNU/Linux platform
    minikube start --vm-driver=virtualbox --kubernetes-version="${VERSION}"

elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    # 32-bit Windows NT platform
    echo "32-bit Windows not supported"
    exit 1
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    # 64-bit Windows NT platform
    echo "64-bit Windows currently not supported"
    exit 1
else
    echo "Unable to detected operating system"
    exit 1
fi

until kubectl version 2>/dev/null >/dev/null; do sleep 5; done
