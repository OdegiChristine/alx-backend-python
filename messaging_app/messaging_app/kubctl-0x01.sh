#!/bin/bash
# Script to scale Django app in Kubernetes, test load, and monitor resources

DEPLOYMENT_NAME="django-messaging-deployment"
SERVICE_NAME="django-messaging-service"
NAMESPACE="default"
TARGET_REPLICAS=3

echo "=== Scaling Kubernetes Deployment ==="
kubectl scale deployment $DEPLOYMENT_NAME --replicas=$TARGET_REPLICAS --namespace=$NAMESPACE

echo ""
echo "=== Verifying Pods ==="
kubectl get pods --namespace=$NAMESPACE -o wide

echo ""
echo "=== Port-forwarding service for local access ==="
kubectl port-forward service/$SERVICE_NAME 8000:8000 &
PORT_FORWARD_PID=$!
sleep 5

echo ""
echo "=== Running Load Test with wrk ==="
wrk -t4 -c50 -d10s http://localhost:8000/

echo ""
echo "=== Monitoring Resource Usage ==="
kubectl top pods --namespace=$NAMESPACE

# Cleanup port-forward
kill $PORT_FORWARD_PID
