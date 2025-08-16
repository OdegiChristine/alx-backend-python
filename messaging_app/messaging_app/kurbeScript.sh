#!/bin/bash
# Script to start a Kubernetes cluster with minikube and check status

echo "=== Kubernetes Script Starting ==="

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
  echo "Minikube is not installed."
  echo "Please install minikube"
  exit 1
else
  echo "Minikube is installed."
fi

# Start Minikube
echo ""
echo "Starting minikube cluster..."
minikube start
if [ $? -ne 0 ]; then
  echo "Failed to start Minikube cluster."
  exit 1
fi

# Verify cluster is running
echo ""
echo "Verifying Kubernetes cluster..."
kubectl cluster-info
if [ $? -ne 0 ]; then
  echo "Cluster verification failed."
  exit 1
else
  echo "Cluster is running."
fi

# Get available pods in all namespaces
echo ""
echo "Retrieving available pods..."
kubectl get pods --all-namespaces

echo ""
echo "=== Script Completed Successfully ==="
