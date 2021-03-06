#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "Usage $0 label=value <optional_namespace>"
  exit 1
fi

namespace=default

if [ -n "$2" ]; then
    namespace=$2
fi

results=`kubectl get pods \
  -l $1 \
  --namespace=$namespace \
  -o jsonpath='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}' \
  2>/dev/null | tr ';' "\n"`

if [ -z "$results" ]; then
  echo "Empty result"
  exit 1
fi

readyPods=`echo $results | tr ' ' "\n" | grep "Ready=True" | wc -l`
allPods=`echo $results | tr ' ' "\n" | grep "Ready=" | wc -l`

if [ "$allPods" -eq 0 ]; then
    echo "No pods found yet"
    exit 1
fi

if [ "$readyPods" -ne "$allPods" ]; then
    echo $readyPods "of" $allPods "ready"
    exit 1
fi

echo "All pods are ready."
exit 0
