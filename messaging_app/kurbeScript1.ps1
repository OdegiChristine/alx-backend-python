# Windows friendly script to start a kubernetes cluster with minikube and check status

Write-host "=== Kubernetes Script Starting ===`n"

# Check if minikube is installed
if (-not (Get-Command minikube -ErrorAction SilentlyContinue)) {
    Write-Host "Minikube is not installed on this system." -ForegroundColor Red
    Write-Host "Please install minikube"
    exit 1
} else {
    Write-Host "Minikube is installed"
}

# Start Minikube
Write-Host "`nStarting Minikube cluster..."
minikube start

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start Minikube cluster" -ForegroundColor Red
    exit 1
}

# Verify cluster is running
Write-Host "`nVerifying Kubernetes cluster"
kubectl cluster-info

if ($LASTEXITCODE -ne 0) {
    Write-Host "Cluster verification failed" -ForegroundColor Red
    exit 1
} else {
    Write-Host "Cluster is running"
}

# Get available pods in all namespaces
Write-Host "`nRetrieving available pods..."
kubectl get pods --all-namespaces

Write-Host "`n=== Script Completed Successfully ==="
