#!/bin/bash

BLUE_DEPLOY="blue_deployment.yaml"
GREEN_DEPLOY="green_deployment.yaml"
SERVICE="kubeservice.yaml"
NAMESPACE="default"

echo "=== Applying Blue Deployment (current stable) ==="
kubectl apply -f $BLUE_DEPLOY

echo ""
echo "=== Applying Green Deployment (new version) ==="
kubectl apply -f $GREEN_DEPLOY

echo ""
echo "=== Applying Service (currently pointing to Blue) ==="
kubectl apply -f $SERVICE

echo ""
echo "=== Checking Pods ==="
kubectl get pods -n  $NAMESPACE -o wide

echo ""
echo "=== Checking Logs of Green Deployment ==="
GREEN_PODS=$(kubectl get pods -n $NAMESPACE -l app=django,version=green -o jsonpath="{.items[*].metadata.name}")

for pod in $GREEN_PODS; do
  echo "--- Logs for $pod ---"
  kubectl logs $pod -n $NAMESPACE | tail -n 20
done

echo ""
echo "Blue-Green setup complete. Switch traffic by editing kubeservice.yaml selector.version from 'blue' to 'green'."
