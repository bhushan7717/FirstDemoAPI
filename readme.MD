# FirstDemoAPI

This repository contains a simple FastAPI application and includes Docker and Kubernetes configuration for local development and deployment.

## Docker

### Build Image
```powershell
docker build -t fastapi-demo:latest .
```
Creates a Docker image from the `Dockerfile` in the current directory and tags it as `fastapi-demo:latest`.

### Run Container
```powershell
docker run -d -p 8000:8000 --name fastapi-app fastapi-demo:latest
```
Starts a container named `fastapi-app` from the image, mapping port 8000 on the host to port 8000 in the container.

### Stop Container
```powershell
docker stop fastapi-app
```
Stops the running container.

### Remove Container
```powershell
docker rm fastapi-app
```
Deletes the stopped container from the host.

### View Logs
```powershell
docker logs fastapi-app
```
Shows the stdout/stderr output from the container.

### Execute Shell in Container
```powershell
docker exec -it fastapi-app /bin/bash
```
Opens an interactive bash shell inside the running container.

### Remove Image
```powershell
docker rmi fastapi-demo:latest
```
Removes the local Docker image; useful before rebuilding.

### Push to Registry (optional)
```powershell
docker tag fastapi-demo:latest yourusername/fastapi-demo:latest
docker push yourusername/fastapi-demo:latest
```
Tags and uploads the image to Docker Hub or another registry.

## Kubernetes (Local Cluster)

> These commands assume a local cluster (Docker Desktop with Kubernetes or Minikube) and that the image was built locally with `imagePullPolicy: Never` in deployment specs.

### Apply Configuration Files
```powershell
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
kubectl apply -f k8s-ingress.yaml
```
Creates the deployment, service, and ingress resources in the cluster.

### Check Resources
```powershell
kubectl get pods
kubectl get svc
kubectl get deployments
kubectl get ingress
```
Lists pods, services, deployments, and ingress to verify status.

### View Pod Logs
```powershell
kubectl logs -f <pod-name>
```
Tails logs for a specific pod; replace `<pod-name>` with the actual name from `kubectl get pods`.

### Port Forward Service
```powershell
kubectl port-forward svc/fastapi-service 8000:80
```
Forwards port 80 of the service to port 8000 on localhost, allowing access via `http://localhost:8000/`.

### Scale Deployment
```powershell
kubectl scale deployment fastapi-app --replicas=3
```
Changes the number of pod replicas managed by the deployment.

### Update Image
```powershell
kubectl set image deployment/fastapi-app fastapi-app=fastapi-demo:v2
```
Performs a rolling update by changing the container image used by the deployment.

### Rollback Deployment
```powershell
kubectl rollout undo deployment/fastapi-app
```
Reverts the deployment to the previous revision.

### Delete Resources
```powershell
kubectl delete deployment,service,ingress -l app=fastapi-app
```
Removes all objects labeled `app=fastapi-app` (deployment, service, ingress).

## Notes
- When running on Minikube, run `minikube docker-env | Invoke-Expression` before building the image so the cluster can see it.
- Use `kubectl get pods -n <namespace>` if deploying to a different namespace.
- Add a hosts entry for the ingress host if using `fastapi.local`:
  ```text
  127.0.0.1 fastapi.local
  ```

This README can be used as a reference for the next time you need to build or deploy the application.