# Kubernetes Setup Guide for FastAPI Application

## Prerequisites
- Docker Desktop installed (includes Kubernetes) OR Minikube installed
- kubectl installed and configured

## Option 1: Docker Desktop with Kubernetes (Easiest)

### Step 1: Enable Kubernetes in Docker Desktop
1. Open Docker Desktop
2. Go to **Settings** → **Kubernetes**
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"
5. Wait for Kubernetes to initialize (check system tray)

### Step 2: Verify Kubernetes is Running
```powershell
kubectl cluster-info
kubectl get nodes
```

---

## Option 2: Minikube Setup

### Step 1: Install Minikube
```powershell
# Using Chocolatey
choco install minikube

# Or download from: https://minikube.sigs.k8s.io/docs/
```

### Step 2: Start Minikube
```powershell
minikube start --driver=hyperv
# or use docker driver
minikube start --driver=docker
```

### Step 3: Configure Docker to Use Minikube
```powershell
minikube docker-env | Invoke-Expression
```

---

## Build and Deploy Steps

### Step 1: Build Docker Image Locally
```powershell
# For Docker Desktop
docker build -t fastapi-demo:latest .

# For Minikube
minikube docker-env | Invoke-Expression
docker build -t fastapi-demo:latest .
```

### Step 2: Apply Kubernetes Manifests

#### Option A: Apply Individual Files
```powershell
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
kubectl apply -f k8s-ingress.yaml
```

#### Option B: Apply All Files at Once
```powershell
kubectl apply -f k8s-deployment.yaml,k8s-service.yaml,k8s-ingress.yaml
```

### Step 3: Verify Deployment
```powershell
# Check Pods
kubectl get pods

# Check Services
kubectl get svc

# Check Deployments
kubectl get deployments

# Check Ingress
kubectl get ingress
```

### Step 4: View Pod Logs
```powershell
# Get pod name
kubectl get pods

# View logs
kubectl logs <pod-name>

# View logs in real-time
kubectl logs -f <pod-name>
```

---

## Access Your Application

### Option A: Using Port Forwarding (Easy)
```powershell
kubectl port-forward svc/fastapi-service 8000:80
```
Then visit: `http://localhost:8000/`

### Option B: Using LoadBalancer Service
```powershell
kubectl get svc fastapi-service
```

**For Docker Desktop:** Visit `http://localhost/` (may take a minute to assign IP)

**For Minikube:** Get the external IP
```powershell
minikube service fastapi-service --url
```

### Option C: Using Ingress (If configured)
```powershell
# For Docker Desktop
# Add to your hosts file (C:\Windows\System32\drivers\etc\hosts):
# 127.0.0.1 fastapi.local

# For Minikube
minikube tunnel
# Then visit: http://fastapi.local/
```

---

## Test Your API

### Using curl
```powershell
curl http://localhost:8000/
curl http://localhost:8000/customers/0
curl http://localhost:8000/models/alexnet
curl http://localhost:8000/getFullName/John/Doe
```

### View Interactive Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Useful Kubernetes Commands

### Pod Management
```powershell
# Get all pods
kubectl get pods

# Get pod details
kubectl describe pod <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Delete a pod (triggers restart)
kubectl delete pod <pod-name>
```

### Deployment Management
```powershell
# Get deployment status
kubectl get deployment

# Update image
kubectl set image deployment/fastapi-app fastapi-app=fastapi-demo:v2

# Rollback deployment
kubectl rollout undo deployment/fastapi-app

# Scale replicas
kubectl scale deployment fastapi-app --replicas=3
```

### View Resources
```powershell
# Get all resources
kubectl get all

# Get specific resource type
kubectl get pods,svc,deployment

# Watch resources in real-time
kubectl get pods -w
```

### Debugging
```powershell
# Get detailed resource info
kubectl describe <resource-type> <resource-name>

# View events
kubectl get events

# Get resource YAML
kubectl get deployment fastapi-app -o yaml
```

### Cleanup
```powershell
# Delete entire deployment
kubectl delete -f k8s-deployment.yaml

# Delete service
kubectl delete -f k8s-service.yaml

# Delete everything related to the app
kubectl delete deployment,service,ingress -l app=fastapi-app
```

---

## Configuration Options

### Scaling
Modify `k8s-deployment.yaml` and change `replicas`:
```yaml
replicas: 3  # Change this number
```

Then apply:
```powershell
kubectl apply -f k8s-deployment.yaml
```

### Resource Limits
Edit `k8s-deployment.yaml` to adjust CPU/Memory:
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "200m"
  limits:
    memory: "512Mi"
    cpu: "1000m"
```

### Environment Variables
Add to `k8s-deployment.yaml`:
```yaml
env:
- name: ENV_VARIABLE
  value: "some_value"
```

---

## Minikube Specific Commands

```powershell
# Dashboard
minikube dashboard

# Access service URL
minikube service fastapi-service

# SSH into minikube
minikube ssh

# Stop minikube
minikube stop

# Delete minikube cluster
minikube delete

# Restart minikube
minikube start
```

---

## Troubleshooting

### Pods not starting
```powershell
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Image pull errors
- Make sure image is built with `docker build -t fastapi-demo:latest .`
- Check `imagePullPolicy: Never` in deployment for local images

### Can't access application
- Check if service is running: `kubectl get svc`
- Try port-forward: `kubectl port-forward svc/fastapi-service 8000:80`

### Ingress not working
- May need to enable ingress addon in minikube: `minikube addons enable ingress`

---

## Next Steps

1. **Add ConfigMap** for configuration management
2. **Add Secrets** for sensitive data
3. **Add Persistent Volumes** if you need data persistence
4. **Add HPA** (Horizontal Pod Autoscaling) for automatic scaling
5. **Setup monitoring** with Prometheus/Grafana
