# Docker & Kubernetes Quick Reference Cheat Sheet

## DOCKER QUICK REFERENCE

### Image Operations
```powershell
docker build -t name:tag .              # Build image from Dockerfile
docker images                           # List all images
docker rmi image-name:tag               # Remove image
docker tag source:tag target:tag        # Rename/tag image
docker history image-name:tag           # View image layers
docker inspect image-name:tag           # Get image details
```

### Container Operations
```powershell
docker run -d -p 8000:8000 image:tag    # Run container (detached)
docker run -it image:tag /bin/bash      # Run container (interactive)
docker ps                               # List running containers
docker ps -a                            # List all containers
docker logs container-name              # View logs
docker logs -f container-name           # Follow logs (tail)
docker exec -it container-name cmd      # Execute command in container
docker stop container-name              # Stop container
docker start container-name             # Start stopped container
docker restart container-name           # Restart container
docker rm container-name                # Delete container
docker stats                            # Resource usage
docker top container-name               # View processes
```

### Volume Operations
```powershell
docker volume create volume-name        # Create volume
docker volume ls                        # List volumes
docker volume inspect volume-name       # Volume details
docker volume rm volume-name            # Delete volume
docker volume prune                     # Remove unused volumes
docker run -v volume:/path image:tag    # Mount volume
docker run -v /host:/container image    # Bind mount
```

### Network Operations
```powershell
docker network create network-name      # Create network
docker network ls                       # List networks
docker network inspect network-name     # Network details
docker network rm network-name          # Delete network
docker network connect network container # Connect container to network
docker run --network network-name image # Run on specific network
```

### Registry Operations
```powershell
docker login                            # Login to Docker Hub
docker push username/image:tag          # Upload image
docker pull image:tag                   # Download image
docker logout                           # Logout from Docker Hub
```

### Docker Compose
```powershell
docker-compose up -d                    # Start services
docker-compose down                     # Stop services
docker-compose logs -f                  # Follow service logs
docker-compose ps                       # List services
docker-compose exec service cmd         # Execute command
docker-compose build                    # Build images
docker-compose pull                     # Pull images
```

### Docker System
```powershell
docker version                          # Docker version
docker info                             # System info
docker system prune                     # Remove unused resources
docker system prune -a                  # Remove all unused resources
```

---

## KUBERNETES QUICK REFERENCE

### Cluster Information
```powershell
kubectl cluster-info                    # Cluster details
kubectl get nodes                       # List nodes
kubectl describe node node-name         # Node details
kubectl get namespaces                  # List namespaces
kubectl get events                      # View cluster events
```

### Pod Operations
```powershell
kubectl get pods                        # List pods
kubectl get pods -A                     # All namespaces
kubectl describe pod pod-name           # Pod details
kubectl logs pod-name                   # View logs
kubectl logs -f pod-name                # Follow logs
kubectl logs pod-name -c container      # Specific container logs
kubectl logs pod-name --previous        # Previous pod instance logs
kubectl exec -it pod-name -- /bin/bash  # Execute in pod
kubectl exec pod-name -- cmd arg        # Run command
kubectl delete pod pod-name             # Delete pod
kubectl port-forward pod-name 8000:8000 # Forward pod port
kubectl port-forward svc/service-name 8000:80 # Forward service port
```

### Deployment Operations
```powershell
kubectl get deployments                 # List deployments
kubectl create deployment name --image=image:tag  # Create deployment
kubectl describe deployment name        # Deployment details
kubectl set image deployment/name container=image:tag  # Update image
kubectl scale deployment name --replicas=3  # Scale replicas
kubectl set env deployment/name VAR=value   # Set env variable
kubectl rollout status deployment/name  # Rollout status
kubectl rollout undo deployment/name    # Rollback deployment
kubectl rollout history deployment/name # Rollout history
kubectl delete deployment name          # Delete deployment
```

### Service Operations
```powershell
kubectl get svc                         # List services
kubectl describe svc service-name       # Service details
kubectl expose deployment name --type=LoadBalancer --port=80 --target-port=8000
kubectl delete svc service-name         # Delete service
```

### ConfigMap & Secret Operations
```powershell
kubectl create configmap cm-name --from-literal=KEY=value
kubectl create secret generic secret-name --from-literal=KEY=value
kubectl get configmap                   # List ConfigMaps
kubectl get secrets                     # List Secrets
kubectl describe configmap cm-name      # ConfigMap details
kubectl describe secret secret-name     # Secret details
kubectl delete configmap cm-name        # Delete ConfigMap
kubectl delete secret secret-name       # Delete Secret
```

### Manifest/YAML Operations
```powershell
kubectl apply -f file.yaml              # Apply manifest
kubectl apply -f file1.yaml,file2.yaml  # Apply multiple files
kubectl apply -f folder/                # Apply all in folder
kubectl delete -f file.yaml             # Delete resources
kubectl get resource-type -o yaml       # Get as YAML
kubectl get pod pod-name -o json        # Get as JSON
```

### Resource Management
```powershell
kubectl get all                         # All resources
kubectl get pods,svc,deployment         # Multiple resource types
kubectl top nodes                       # Node resource usage
kubectl top pods                        # Pod resource usage
kubectl describe resource-type name     # Detailed info
```

### Namespace Operations
```powershell
kubectl get namespaces                  # List namespaces
kubectl create namespace ns-name        # Create namespace
kubectl delete namespace ns-name        # Delete namespace
kubectl apply -f file.yaml -n namespace # Apply to namespace
kubectl get pods -n namespace           # Get pods in namespace
kubectl -n namespace get all            # All resources in namespace
```

### Debugging & Troubleshooting
```powershell
kubectl describe pod pod-name           # Pod details & events
kubectl logs pod-name                   # Pod logs
kubectl logs pod-name --all-containers  # All container logs
kubectl get events                      # Cluster events
kubectl get events --sort-by='.lastTimestamp'  # Sorted events
kubectl exec -it pod-name -- /bin/bash  # Shell into pod
kubectl port-forward pod-name 8000:8000 # Test connectivity
kubectl run -it --rm debug --image=busybox -- sh  # Debug pod
```

### Watch Resources
```powershell
kubectl get pods -w                     # Watch pods (live update)
kubectl get pods -w -l app=fastapi      # Watch with label filter
kubectl get events -w                   # Watch events
```

---

## DOCKERFILE QUICK REFERENCE

### Basic Structure
```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s CMD curl http://localhost:8000/

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Common Commands
| Command | Purpose |
|---------|---------|
| `FROM image:tag` | Base image |
| `WORKDIR /path` | Set working directory |
| `COPY src dest` | Copy files |
| `ADD src dest` | Copy files (includes URLs) |
| `RUN command` | Execute command |
| `ENV KEY=value` | Environment variable |
| `EXPOSE port` | Document exposed port |
| `VOLUME /path` | Volume mount point |
| `USER username` | Run as user |
| `ENTRYPOINT` | Main process |
| `CMD` | Default command |
| `HEALTHCHECK` | Health check |

---

## KUBERNETES MANIFEST QUICK REFERENCE

### Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-name
spec:
  containers:
  - name: container-name
    image: image:tag
    ports:
    - containerPort: 8000
```

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment-name
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: container-name
        image: image:tag
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: service-name
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8000
```

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config-name
data:
  KEY1: value1
  KEY2: value2
  config.yaml: |
    key: value
```

### Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-name
type: Opaque
data:
  username: dXNlcm5hbWU=  # base64 encoded
  password: cGFzc3dvcmQ=
```

### PersistentVolumeClaim
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-name
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

---

## Port Mapping Quick Reference

### Docker
```powershell
docker run -p 8000:8000 image:tag
        │     │
        │     └── Container port
        └──────── Host port
```

### Kubernetes Service
```yaml
ports:
- port: 80             # External port
  targetPort: 8000     # Pod port
```

### Port Forwarding
```powershell
# Pod
kubectl port-forward pod-name 8000:8000

# Service
kubectl port-forward svc/service-name 8000:80
```

---

## Resource Units Reference

### CPU
```
1000m = 1 CPU
500m = 0.5 CPU
250m = 0.25 CPU
100m = 0.1 CPU
```

### Memory
```
1Gi = 1 Gigabyte = 1024 Mi
1Mi = 1 Megabyte = 1024 Ki
1Ki = 1 Kilobyte = 1024 bytes
```

---

## Label & Selector Patterns

### Labels
```yaml
metadata:
  labels:
    app: my-app
    version: v1
    tier: backend
    environment: production
```

### Selectors
```yaml
# Exact match
selector:
  app: my-app

# Multiple labels (AND)
selector:
  app: my-app
  tier: backend

# Expression (in manifest)
matchLabels:
  app: my-app
```

### kubectl Selector
```powershell
# Label matching
kubectl get pods -l app=my-app
kubectl get pods -l "app=my-app,tier=backend"
kubectl get pods -l "env in (prod,dev)"
kubectl get pods -l "env notin (test)"
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Image not found | Make sure image is built or pulled |
| Port already in use | Use different port or stop other container |
| Can't connect to service | Check service selector labels match pod labels |
| Pod not starting | Check `kubectl describe pod` and logs |
| Out of disk space | `docker system prune -a` or `kubectl delete` unused |
| Slow startup | Increase `initialDelaySeconds` in probe |
| Too many containers crashing | Check `kubectl logs` for errors |
| Can't access externally | Use NodePort or LoadBalancer service type |

---

## Environment Variables in Kubernetes

### From ConfigMap
```yaml
env:
- name: VAR_NAME
  valueFrom:
    configMapKeyRef:
      name: config-map-name
      key: key-name
```

### From Secret
```yaml
env:
- name: VAR_NAME
  valueFrom:
    secretKeyRef:
      name: secret-name
      key: key-name
```

### From Pod fields
```yaml
env:
- name: POD_NAME
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
```

### Load all from ConfigMap
```yaml
envFrom:
- configMapRef:
    name: config-map-name
```

---

## Useful Kubectl Aliases

```powershell
# Add to PowerShell profile
function k { kubectl @args }
function kg { kubectl get @args }
function kd { kubectl describe @args }
function kl { kubectl logs @args }
function ke { kubectl exec @args }

# Usage
k get pods
kg pods
kd pod pod-name
kl pod-name
ke -it pod-name -- /bin/bash
```

---

## Kubectl Context & Config

```powershell
kubectl config get-contexts              # List contexts
kubectl config current-context           # Current context
kubectl config use-context context-name  # Switch context
kubectl config view                      # View config
kubectl config set-context --current --namespace=ns  # Set default namespace
```

---

## Multi-Container Pod Pattern

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container-pod
spec:
  containers:
  - name: app
    image: app:tag
    ports:
    - containerPort: 8000
  - name: sidecar
    image: sidecar:tag
    ports:
    - containerPort: 9000
  # Containers share:
  # - Network namespace (same IP)
  # - Storage (via shared volumes)
```

---

## Health Check Probe Examples

### HTTP
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
```

### TCP
```yaml
livenessProbe:
  tcpSocket:
    port: 8000
```

### Command Exec
```yaml
livenessProbe:
  exec:
    command:
    - /bin/sh
    - -c
    - wget --quiet --tries=1 --spider http://localhost:8000/health
```

### Common Parameters
```yaml
initialDelaySeconds: 10    # Wait before first check
periodSeconds: 10          # Check every N seconds
timeoutSeconds: 5          # Wait N seconds for response
successThreshold: 1        # Success after N passes
failureThreshold: 3        # Fail after N failures
```

---

This cheat sheet is your quick reference! Bookmark it and come back when you need quick command syntax.
