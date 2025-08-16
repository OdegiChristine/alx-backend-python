#!/bin/bash
# Rolling update with zero downtime check

DEPLOYMENT="blue_deployment.yaml"
SERVICE="django-service"
NAMESPACE="default"
URL="http://localhost:8000"

echo "=== Starting Rolling Update ==="
kubectl apply -f $DEPLOYMENT

echo ""
echo "=== Monitoring Rollout Status ==="
kubectl rollout status deployment/django-messaging-blue -n $NAMESPACE

echo ""
echo "=== Testing for downtime during rollout ==="
for i in {1...30}; do
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)
  if [ "$RESPONSE" -eq 200 ]; then
    echo "[$i] App is responding (HTTP 200)"
  else
    echo "[$i] App might be down! Response code: $RESPONSE"
  fi
  sleep 2
done

echo ""
echo "=== Verifying pods after update ==="
kubectl get pods -l app=django,version=blue -n $NAMESPACE -o wide

echo ""
echo "Rolling update completed successfully!"
