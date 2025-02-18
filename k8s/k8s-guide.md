# Kubernetes Setup and Usage Guide

## Initial Setup

Before deploying your application to Kubernetes, ensure you have a running cluster:

```bash
# Start Minikube cluster
minikube start

# Verify cluster is running
kubectl cluster-info
```

## Loading Your Docker Image

Since Minikube runs in its own VM, you need to make your local Docker image available to it:

```bash
# Build your image if you haven't already
docker build -t mnist-classifier:latest .

# Load the image into Minikube
minikube image load mnist-classifier:latest

# Verify the image is available
minikube image ls | grep mnist-classifier
```

## Deploying Your Application

Deploy the components in the following order to ensure dependencies are met:

```bash
# 1. Create persistent storage
kubectl apply -f k8s/persistent-volume.yaml

# 2. Create the deployment
kubectl apply -f k8s/deployment.yaml

# 3. Create the service
kubectl apply -f k8s/service.yaml

# 4. Create the HPA
kubectl apply -f k8s/hpa.yaml

# Alternatively, deploy everything at once
kubectl apply -f k8s/
```

## Understanding Service Types

Kubernetes provides several service types for exposing your application:

### ClusterIP
- Default service type
- Exposes the service on a cluster-internal IP
- Only reachable from within the cluster
- Useful for internal communication between services

### NodePort
- Exposes the service on each node's IP at a static port
- Accessible from outside the cluster using `<NodeIP>:<NodePort>`
- Port range is typically 30000-32767
- Good for development and testing

### LoadBalancer
- Exposes the service externally using a cloud provider's load balancer
- When using Minikube, requires additional steps to access
- Standard way to expose services to the internet in production

## Accessing Your Application

There are several ways to access your service locally:

```bash
# 1. Using Minikube service command (easiest)
minikube service mnist-classifier

# 2. Using port-forwarding
kubectl port-forward service/mnist-classifier 8000:80

# 3. Using Minikube tunnel (runs in background)
minikube tunnel
# Your service will be available at localhost:80
```

## Monitoring Your Deployment

Keep track of your resources:

```bash
# Check pod status
kubectl get pods

# Watch pod status in real-time
kubectl get pods -w

# Check service status
kubectl get services

# Check HPA status
kubectl get hpa

# View pod logs
kubectl logs -l app=mnist-classifier
```

## Teardown Process

When you're done, remove resources in this order:

```bash
# Remove all resources
kubectl delete -f k8s/

# Or remove individually in this order:
kubectl delete -f k8s/hpa.yaml
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/persistent-volume.yaml

# Verify all resources are removed
kubectl get all | grep mnist

# Stop Minikube (optional)
minikube stop

# Delete Minikube cluster (optional)
minikube delete
```

## Troubleshooting

Common issues and their solutions:

1. **Pods stuck in "Pending" state**
   ```bash
   kubectl describe pod <pod-name>
   # Check events section for details
   ```

2. **Service not accessible**
   ```bash
   # Check service endpoints
   kubectl get endpoints mnist-classifier
   
   # Check pod readiness
   kubectl describe pod <pod-name> | grep Ready
   ```

3. **PersistentVolume issues**
   ```bash
   # Check PV/PVC status
   kubectl get pv,pvc
   
   # Check PV/PVC details
   kubectl describe pv <pv-name>
   kubectl describe pvc <pvc-name>
   ```

4. **Force delete stuck resources**
   ```bash
   kubectl delete <resource> <name> --force --grace-period=0
   ```

Remember to check logs frequently during troubleshooting:
```bash
# Container logs
kubectl logs <pod-name> -f

# Previous container logs (if container has restarted)
kubectl logs <pod-name> --previous
```
