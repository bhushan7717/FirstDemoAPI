# Docker & Kubernetes Complete Learning Guide

## Table of Contents
1. [Docker Fundamentals](#docker-fundamentals)
2. [Kubernetes Fundamentals](#kubernetes-fundamentals)
3. [Concepts We Used](#concepts-we-used)
4. [Learning Resources](#learning-resources)
5. [Hands-On Exercises](#hands-on-exercises)
6. [Best Practices](#best-practices)

---

# DOCKER FUNDAMENTALS

## What is Docker?

Docker is a containerization platform that packages your application and all its dependencies into a standardized unit called a **container**.

### Key Problem Docker Solves
- **"It works on my machine"** problem
- Consistency across development, testing, and production environments
- Easy deployment and scaling

### Docker Architecture

```
┌─────────────────────────────────────────┐
│            Host OS (Windows)            │
├─────────────────────────────────────────┤
│          Docker Daemon (Engine)         │
├──────────┬──────────┬──────────────────┤
│Container │Container │  Container       │
│ App + OS │ App + OS │  App + OS        │
│Libraries │Libraries │  Libraries       │
└──────────┴──────────┴──────────────────┘
```

### Core Concepts

#### 1. **Image**
- Blueprint for creating containers (like a class in OOP)
- Read-only template containing your application code, runtime, and dependencies
- Stored in layers for efficiency
- Example: `fastapi-demo:latest`

#### 2. **Container**
- Running instance of an image (like an object in OOP)
- Lightweight, isolated environment
- Can be started, stopped, deleted
- Each has its own filesystem, network interfaces, processes

#### 3. **Dockerfile**
- Text file with instructions to build an image
- Contains commands to build layers step by step

```dockerfile
FROM python:3.11-slim           # Base image (layer 1)
WORKDIR /app                    # Working directory (layer 2)
COPY requirements.txt .         # Copy files (layer 3)
RUN pip install -r requirements.txt  # Install dependencies (layer 4)
COPY main.py .                  # Copy app code (layer 5)
EXPOSE 8000                     # Document exposed port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]  # Default command
```

#### 4. **Docker Registry**
- Repository for storing and sharing images
- Public: Docker Hub (hub.docker.com)
- Private: Amazon ECR, Google Container Registry, etc.

### Docker Lifecycle

```
1. CREATE IMAGE
   docker build -t fastapi-demo:latest .
           ↓
2. STORE (optional)
   docker push fastapi-demo:latest
           ↓
3. CREATE CONTAINER
   docker run -d -p 8000:8000 --name fastapi-app fastapi-demo:latest
           ↓
4. MANAGE
   docker ps, docker logs, docker exec, etc.
           ↓
5. CLEANUP
   docker stop, docker rm, docker rmi
```

### Docker Commands Explained

```powershell
# BUILD - Create image from Dockerfile
docker build -t fastapi-demo:latest .
  -t = tag (name:version)
  . = build context (current directory)

# RUN - Create and start container from image
docker run -d -p 8000:8000 --name fastapi-app fastapi-demo:latest
  -d = detached (background)
  -p = port mapping (host:container)
  --name = container name

# PS - List running containers
docker ps
docker ps -a  # All containers (including stopped)

# LOGS - View container output
docker logs fastapi-app
docker logs -f fastapi-app  # Follow/tail logs

# EXEC - Run command in running container
docker exec -it fastapi-app /bin/bash  # Interactive terminal

# STOP - Stop container gracefully
docker stop fastapi-app

# START - Start stopped container
docker start fastapi-app

# RM - Delete container
docker rm fastapi-app  # Must stop first

# RMI - Delete image
docker rmi fastapi-demo:latest

# PUSH - Upload image to registry
docker push yourusername/fastapi-demo:latest

# PULL - Download image from registry
docker pull yourusername/fastapi-demo:latest
```

### Layers in Docker Images

Each command in Dockerfile creates a new layer:

```dockerfile
FROM python:3.11-slim      # Layer 1: ~130MB (base image)
WORKDIR /app               # Layer 2: tiny (metadata)
COPY requirements.txt .    # Layer 3: small (text file)
RUN pip install ...        # Layer 4: ~200MB (packages)
COPY main.py .             # Layer 5: tiny (app code)
```

**Benefits:**
- Caching: If layer 3 doesn't change, layers 1-3 are reused
- Efficiency: Smaller build times
- Storage: Only unique parts are stored

---

## Docker Networking

### Port Mapping
```powershell
docker run -p 8000:8000 fastapi-demo:latest

8000:8000
│     │
│     └── Container port (inside Docker)
└──────── Host port (your machine)
```

You access via `http://localhost:8000/`

### Network Types

1. **Bridge Network** (default)
   - Containers can talk to each other
   - Isolated from host except via port mapping

2. **Host Network**
   - Container uses host's network directly
   - `docker run --network host`

3. **Custom Networks**
   - Create your own for better isolation
   ```powershell
   docker network create myapp-network
   docker run --network myapp-network ...
   ```

---

## Docker Volumes & Storage

### Problem: Container Data Loss
```
Container is deleted → All data inside is lost
```

### Solution: Volumes

```powershell
# Named volume
docker run -v my-volume:/app/data fastapi-demo:latest

# Bind mount (local directory)
docker run -v C:\data:/app/data fastapi-demo:latest

# Anonymous volume
docker run -v /app/data fastapi-demo:latest
```

---

## Docker Compose (Multiple Containers)

If you want database + app together:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

```powershell
docker-compose up -d      # Start services
docker-compose down       # Stop services
docker-compose logs -f    # View logs
```

---

# KUBERNETES FUNDAMENTALS

## What is Kubernetes?

Kubernetes (K8s) is an orchestration platform that automates deployment, scaling, and management of containerized applications across a cluster of machines.

### Key Problems Kubernetes Solves
- Managing multiple containers across multiple machines
- Automatic scaling based on demand
- Self-healing when containers fail
- Load balancing and service discovery
- Rolling updates and rollbacks

### Kubernetes Architecture

```
┌─────────────────────────────────────────────┐
│          CONTROL PLANE (Master)             │
│  ┌──────────────────────────────────────┐  │
│  │ API Server - All requests go here    │  │
│  │ Scheduler - Decides where to run pod │  │
│  │ Controller - Maintains desired state  │  │
│  │ etcd - Cluster database              │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
           │         │         │
    ┌──────┴─────┬───┴─────┬───┴──────┐
    │            │         │          │
┌───▼──┐     ┌──▼──┐   ┌──▼──┐   ┌──▼──┐
│Worker│     │Worker│   │Worker│   │Worker│
│Node 1│     │Node 2│   │Node 3│   │Node 4│
└──────┘     └──────┘   └──────┘   └──────┘
(Pods run here)
```

### Core Kubernetes Objects

#### 1. **Pod** (Smallest unit)
- Wrapper around one or more containers
- Containers in a pod share network namespace
- Usually one container per pod
- Ephemeral (can be deleted anytime)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fastapi-pod
spec:
  containers:
  - name: fastapi
    image: fastapi-demo:latest
    ports:
    - containerPort: 8000
```

#### 2. **Deployment** (Manages Pods)
- Manages creation and updates of pods
- Ensures desired number of replicas are running
- Supports rolling updates and rollbacks
- Self-healing: restarts failed pods

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3  # Desired number of pods
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-app
        image: fastapi-demo:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

**Key Features:**
```
Deploys 3 pods
     ↓
If 1 pod crashes → Auto restart
If 1 pod is slow → Load balancer distributes traffic
Update image → Rolling update (no downtime)
Rollback if needed → Revert to previous version
```

#### 3. **Service** (Network Access)
- Stable IP and DNS for pods
- Load balancing across pods
- Types: ClusterIP, NodePort, LoadBalancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  selector:
    app: fastapi-app  # Routes to pods with this label
  ports:
  - port: 80          # External port
    targetPort: 8000  # Pod port
```

**How Service Routing Works:**
```
Client Request
     ↓
Service (fastapi-service:80)
     ↓
Load Balancer
    / | \
   /  |  \
Pod1 Pod2 Pod3 (8000)
```

#### 4. **Ingress** (HTTP/HTTPS Routing)
- External HTTP(S) access
- hostname-based routing
- SSL/TLS termination

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-ingress
spec:
  rules:
  - host: fastapi.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fastapi-service
            port:
              number: 80
```

**How Ingress Works:**
```
User visits: fastapi.local
     ↓
Ingress Controller (nginx)
     ↓
Routes to fastapi-service
     ↓
Service routes to Pod
```

#### 5. **ConfigMap** (Configuration)
- Store non-sensitive configuration
- Key-value pairs
- Mount as files or environment variables

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgresql://..."
  LOG_LEVEL: "debug"
  API_VERSION: "v1"
```

Usage in Deployment:
```yaml
containers:
- name: fastapi-app
  image: fastapi-demo:latest
  envFrom:
  - configMapRef:
      name: app-config
```

#### 6. **Secret** (Sensitive Data)
- Store passwords, API keys, tokens
- Base64 encoded (not encrypted by default)
- Similar interface to ConfigMap

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: cGFzc3dvcmQxMjM=  # base64 encoded
  API_KEY: YWJjZGVmZ2hpamtsbW5vcA==
```

#### 7. **PersistentVolume (PV) & PersistentVolumeClaim (PVC)**
- Persistent storage across pod restarts
- Like external hard drive for containers

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-storage
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  template:
    spec:
      containers:
      - name: fastapi-app
        volumeMounts:
        - name: data
          mountPath: /app/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: app-storage
```

#### 8. **Namespace**
- Virtual cluster within a cluster
- Helps organize and isolate resources
- Default namespaces: default, kube-system, kube-public

```powershell
kubectl get pods -n default
kubectl get pods -n kube-system
kubectl create namespace my-app
kubectl apply -f deployment.yaml -n my-app
```

---

# CONCEPTS WE USED IN YOUR SETUP

## 1. **Deployment with Replicas**
```yaml
replicas: 2  # Two identical copies of your pod
```

**Why?**
- High Availability: If one fails, one still runs
- Load Distribution: Traffic spreads across replicas
- Updates: Can update one while others serve traffic

**Manual Scaling:**
```powershell
kubectl scale deployment fastapi-app --replicas=5
```

## 2. **Health Checks (Probes)**

### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
```

**What it does:**
- Every 10 seconds, checks if pod is alive
- Makes HTTP GET request to `/`
- If fails 3 times → Kubernetes restarts pod

**Analogy:** Checking if your app is breathing

### Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

**What it does:**
- Checks if pod is ready to receive traffic
- Different from liveness (may be alive but initializing)
- If fails → Removes pod from service load balancer

**Analogy:** Checking if your app is ready to take requests

## 3. **Resource Management**
```yaml
resources:
  requests:          # Minimum guaranteed
    memory: "128Mi"
    cpu: "100m"
  limits:           # Maximum allowed
    memory: "256Mi"
    cpu: "500m"
```

**Impact:**
- **requests**: Kubernetes uses this to decide where to schedule pod
- **limits**: Pod is killed if exceeds this
- **No requests**: Pod can be evicted if node is full
- **No limits**: Pod can consume all resources → starve others

**CPU Units:**
```
1000m = 1 CPU
500m = 0.5 CPU
100m = 0.1 CPU
```

**Memory Units:**
```
1Gi = 1 Gigabyte
1Mi = 1 Megabyte
1Ki = 1 Kilobyte
```

## 4. **ImagePullPolicy**
```yaml
imagePullPolicy: Never  # Use local image only
```

**Options:**
- `IfNotPresent` (default): Use local if exists, else pull
- `Always`: Always pull latest from registry
- `Never`: Only use local image

## 5. **Service LoadBalancing**
```yaml
type: LoadBalancer
selector:
  app: fastapi-app
```

**How traffic is distributed:**

```
Client 1 ──┐
Client 2 ──┤
Client 3 ──┼─→ Service ─┬─→ Pod1 (fastapi-app)
Client 4 ──┤           ├─→ Pod2 (fastapi-app)
Client 5 ──┘           └─→ Pod3 (fastapi-app)
           Load Balancing (Round-robin by default)
```

## 6. **Port Mapping in Kubernetes**

```yaml
ports:
- containerPort: 8000      # Pod's internal port
```

Service Configuration:
```yaml
ports:
- port: 80                 # External port
  targetPort: 8000         # Pod port (can be name or number)
```

**Flow:**
```
Client: localhost:80
       ↓
Service virtual IP + Port 80
       ↓
Routes to targetPort 8000 of selected pods
```

## 7. **Labels and Selectors**

**Label (on Pod):**
```yaml
metadata:
  labels:
    app: fastapi-app
```

**Selector (in Service/Deployment):**
```yaml
selector:
  app: fastapi-app  # Only pods with this label
```

**Multiple Labels Example:**
```yaml
labels:
  app: fastapi-app
  version: v1
  team: backend
---
selector:
  app: fastapi-app
  version: v1
  # Selects pods matching ALL labels
```

---

# LEARNING RESOURCES

## Official Documentation (Bookmark These!)

### Docker
- **Docker Docs**: https://docs.docker.com/
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **Dockerfile Reference**: https://docs.docker.com/engine/reference/builder/

### Kubernetes
- **Kubernetes Official Docs**: https://kubernetes.io/docs/
- **Kubernetes API Reference**: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.28/
- **kubectl Cheat Sheet**: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

## Free Online Courses

### Docker
1. **Docker Official Tutorial** (Free)
   - https://docker-curriculum.com/
   - Very beginner-friendly

2. **YouTube - NetworkChuck**
   - Docker in 100 seconds
   - Docker full course (several hours)

3. **Udemy** (Often $10 sales)
   - "The Complete Docker Course"
   - "Docker and Kubernetes: The Complete Guide"

### Kubernetes
1. **Interactive Playground**
   - https://www.katacoda.com/courses/kubernetes
   - Practice K8s without installing

2. **YouTube - TechWorld with Nana**
   - "Kubernetes Tutorial for Beginners"
   - Very popular and well-explained

3. **Linux Academy / A Cloud Guru**
   - Kubernetes basics course
   - Hands-on labs

## Books

1. **The Docker Book** - James Turnbull
2. **Kubernetes in Action** - Marko Lukša
3. **The Kubernetes Book** - Nigel Poulton

## Interactive Practice

### Play with Docker (PWD)
- https://labs.play-with-docker.com/
- Run Docker commands online (no installation)
- Limited 4 hours

### Play with Kubernetes (PWK)
- https://labs.play-with-k8s.com/
- Run Kubernetes online
- Fully functional cluster

### Minikube
- Local Kubernetes cluster for practice
- Perfect for learning without production impact

---

# HANDS-ON EXERCISES

## Exercise 1: Docker Basics

### Build and Run Container
```powershell
# 1. Build image
docker build -t my-app:v1 .

# 2. Run container
docker run -d -p 8000:8000 --name my-container my-app:v1

# 3. Check logs
docker logs my-container

# 4. Execute command in running container
docker exec -it my-container /bin/bash

# 5. Stop container
docker stop my-container

# 6. Remove container
docker rm my-container

# 7. Remove image
docker rmi my-app:v1
```

### What you'll learn:
- Image building
- Container lifecycle
- Port mapping
- Container interaction

## Exercise 2: Docker Networking

```powershell
# 1. Create network
docker network create my-network

# 2. Run container on network
docker run -d --name app1 --network my-network my-app:v1
docker run -d --name app2 --network my-network my-app:v1

# 3. Containers can ping each other by name
docker exec app1 ping app2

# 4. Clean up
docker network rm my-network
```

## Exercise 3: Volume Persistence

```powershell
# 1. Create volume
docker volume create my-data

# 2. Run with volume
docker run -d -v my-data:/app/data my-app:v1

# 3. Check volume
docker volume inspect my-data

# 4. Clean up
docker volume rm my-data
```

## Exercise 4: Kubernetes Basic Deployment

```powershell
# 1. Create deployment
kubectl create deployment fastapi --image=fastapi-demo:latest

# 2. Check deployment
kubectl get deployment
kubectl get pods
kubectl describe deployment fastapi

# 3. Scale deployment
kubectl scale deployment fastapi --replicas=3

# 4. View logs
kubectl logs deployment/fastapi
kubectl logs -f pod-name

# 5. Update image
kubectl set image deployment/fastapi fastapi=fastapi-demo:v2

# 6. Rollback if needed
kubectl rollout undo deployment/fastapi

# 7. Delete deployment
kubectl delete deployment fastapi
```

## Exercise 5: Kubernetes Service Exposure

```powershell
# 1. Create service
kubectl expose deployment fastapi --type=LoadBalancer --port=80 --target-port=8000

# 2. Get service IP
kubectl get svc

# 3. Port forward (for testing)
kubectl port-forward svc/fastapi 8000:80

# 4. Access service
curl localhost:8000

# 5. Delete service
kubectl delete svc fastapi
```

## Exercise 6: ConfigMap and Environment Variables

```powershell
# 1. Create ConfigMap
kubectl create configmap app-config --from-literal=DEBUG=true --from-literal=LOG_LEVEL=info

# 2. Check ConfigMap
kubectl get configmap
kubectl describe configmap app-config

# 3. Create deployment that uses ConfigMap
kubectl apply -f configmap-deployment.yaml

# 4. Verify environment variables in pod
kubectl exec pod-name -- env | grep DEBUG

# 5. Delete ConfigMap
kubectl delete configmap app-config
```

## Exercise 7: Debugging and Troubleshooting

```powershell
# 1. Get detailed pod info
kubectl describe pod pod-name

# 2. View logs
kubectl logs pod-name
kubectl logs pod-name -c container-name  # Specific container
kubectl logs pod-name --previous         # Previous instance

# 3. Get into pod
kubectl exec -it pod-name -- /bin/bash

# 4. Check resource usage
kubectl top nodes
kubectl top pods

# 5. View events
kubectl get events

# 6. Get resource YAML
kubectl get pod pod-name -o yaml
kubectl get deployment deployment-name -o yaml

# 7. Port forward to debug
kubectl port-forward pod-name 8000:8000
```

---

# BEST PRACTICES

## Docker Best Practices

### 1. Use Specific Base Image Versions
```dockerfile
# ❌ Bad: Latest might break your build
FROM python:latest

# ✅ Good: Specific version
FROM python:3.11-slim
```

### 2. Minimize Layers and Size
```dockerfile
# ❌ Bad: Creates separate layers, larger image
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2

# ✅ Good: Combines into one layer
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Use .dockerignore
```
__pycache__
*.pyc
.git
.env
node_modules
```

### 4. Security: Don't Run as Root
```dockerfile
RUN useradd -m appuser
USER appuser
```

### 5. Health Checks in Dockerfile
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"
```

### 6. Multi-Stage Builds (For smaller images)
```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY main.py .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app"]
```

### 7. Logging
```dockerfile
# Ensure logs go to stdout/stderr for container logging
# Don't write to files inside container
```

## Kubernetes Best Practices

### 1. Always Set Resource Requests and Limits
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"
```

### 2. Use Health Checks
```yaml
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

### 3. Use Labels and Selectors Properly
```yaml
labels:
  app: fastapi-app
  version: v1
  environment: production
```

### 4. Never Run Root in Containers
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

### 5. Use ConfigMaps for Configuration
```yaml
envFrom:
- configMapRef:
    name: app-config
```

### 6. Use Secrets for Sensitive Data
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: db-password
```

### 7. Implement Proper Update Strategy
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### 8. Use NetworkPolicy for Security
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: restrict-traffic
spec:
  podSelector:
    matchLabels:
      app: fastapi-app
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
```

### 9. Monitor and Alert
```yaml
- Set up Prometheus/Grafana
- Configure AlertManager
- Monitor resource usage
- Track application metrics
```

### 10. Backup Critical Data
```yaml
- Use PersistentVolumes with backup policies
- Regular snapshot backups
- Test restore procedures
```

---

# GLOSSARY

| Term | Definition |
|------|-----------|
| **Image** | Blueprint for containers |
| **Container** | Running instance of an image |
| **Dockerfile** | Instructions to build image |
| **Registry** | Repository for images (Docker Hub) |
| **Pod** | Smallest K8s unit, wraps containers |
| **Deployment** | Manages pods (replicas) |
| **Service** | Network access to pods |
| **Ingress** | HTTP(S) routing |
| **ConfigMap** | Configuration key-values |
| **Secret** | Sensitive data storage |
| **Namespace** | Virtual cluster |
| **Node** | Machine in cluster |
| **Cluster** | Group of nodes |
| **Manifest** | YAML file describing K8s resource |
| **Replica** | Copy of pod |
| **Label** | Key-value tag on resources |
| **Selector** | Query to find resources by labels |
| **Volume** | Storage for containers/pods |
| **PVC** | Request for persistent storage |
| **kubectl** | Command-line tool for K8s |

---

# PRACTICE PROJECT IDEAS

## Beginner
1. Run a simple web app in Docker
2. Create 2 containers that communicate
3. Deploy single container to Kubernetes

## Intermediate
1. Multi-container Docker Compose setup
2. Configure ConfigMap and Secrets
3. Implement health checking

## Advanced
1. Multi-replica deployment with load balancing
2. Rolling updates and rollbacks
3. Implement NetworkPolicy
4. Setup autoscaling (HPA)
5. Persistent storage setup

---

# Quick Reference Commands

## Docker
```powershell
docker build -t name:tag .
docker run -d -p 8000:8000 name:tag
docker ps
docker logs container-name
docker exec -it container-name /bin/bash
docker stop container-name
docker rm container-name
docker rmi image-name:tag
```

## Kubernetes
```powershell
kubectl apply -f file.yaml
kubectl get pods/svc/deployment
kubectl describe pod pod-name
kubectl logs pod-name
kubectl exec -it pod-name -- /bin/bash
kubectl port-forward svc/service-name 8000:80
kubectl scale deployment name --replicas=3
kubectl set image deployment/name container=image:tag
kubectl rollout undo deployment/name
kubectl delete pod/svc/deployment name
```

---

## Next Steps

1. **Complete Docker Tutorial** (2-3 hours)
   - Follow docker-curriculum.com

2. **Setup Local Kubernetes** (1 hour)
   - Install Minikube or use Docker Desktop

3. **Deploy Your First App** (1-2 hours)
   - Deploy FastAPI to local K8s

4. **Learn Helm** (2-3 hours)
   - Package manager for K8s
   - Makes deployments easier

5. **Explore Advanced Topics** (Ongoing)
   - StatefulSets for databases
   - DaemonSets for agents
   - Jobs and CronJobs
   - Custom Resources (CRDs)

---

**Remember:** The best way to learn is by doing. Practice with your own projects!
