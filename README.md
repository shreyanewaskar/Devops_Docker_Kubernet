# CloudCart – Containerization & Kubernetes Deployment

**Name:** Shreya Sachin Newaskar
**Department:** Computer Science
**PRN:** 202301040240
**Division:** B

## Submission links

Everything for this challenge is in two places: a Google Drive folder and a GitHub repository.

| Item | Link |
|------|------|
| PDF report and execution evidence (Drive folder) | Open Drive folder |
| Recorded online demonstration video (Drive folder) | Open Drive folder |
| GitHub repository (Dockerfile, Kubernetes YAML, source code) | https://github.com/shreyanewaskar/Devops_Docker_Kubernet |

## Project overview

**CloudCart** is a small cloud-native e-commerce demo built with Python and Flask. It is packaged into a Docker image and run on Kubernetes using a Deployment (2 replicas) and a NodePort Service, covering the full path from source code to a running, reachable pod.

**The application**
- A storefront page with a hero banner, featured products, category filters (All, Electronics, Fashion, Lifestyle), live product search and a cart counter.
- The footer shows **Container Host**: the hostname of the pod serving the request. With 2 replicas, refreshing the page shows Kubernetes load-balancing between pods.
- A `/health` endpoint returns JSON (`status`, `application`, `hostname`), useful for checking the pod is up.

**The deployment**
- **Docker:** the Dockerfile uses `python:3.12-slim`, installs Flask, copies `app.py` and exposes port 5000.
- **Kubernetes:** `deployment.yaml` runs 2 replicas of `cloudcart:1.0`; `service.yaml` exposes them on NodePort 30007 so the app opens in a browser.
- **Evidence:** screenshots of the build, the running pods and the service are in the PDF report.

## Repository contents

| File | Purpose |
|------|---------|
| `app.py` | CloudCart Flask app (storefront at `/`, health check at `/health`), listens on port 5000 |
| `requirements.txt` | Python dependency (Flask 3.1.2) |
| `Dockerfile` | Builds the `cloudcart:1.0` image |
| `deployment.yaml` | Deployment `cloudcart-deployment`: 2 replicas, container port 5000 |
| `service.yaml` | Service `cloudcart-service`: NodePort 30007 → port 5000 |
| `README.md` | Setup and run instructions |

## Execution steps

These are the commands shown in the demo video.

1. Build the image: `docker build -t cloudcart:1.0 .`
2. Run it in a container: `docker run -p 8080:5000 cloudcart:1.0` and open http://localhost:8080
3. Apply the Deployment: `kubectl apply -f deployment.yaml`
4. Apply the Service: `kubectl apply -f service.yaml`
5. Show the running pods: `kubectl get pods`
6. Show the service and its access port: `kubectl get svc`
7. Open the app in the browser through the service URL: http://localhost:30007 (Docker Desktop Kubernetes) or `minikube service cloudcart-service` (Minikube).

Health check: `curl http://localhost:30007/health`

If you use Minikube, load the local image first with `minikube image load cloudcart:1.0` (the Deployment uses `imagePullPolicy: IfNotPresent`).

## Cloud-native concepts

The demo video explains these ideas alongside the deployment.

- **Containerization:** CloudCart and Flask are packed into one image that runs the same on any machine.
- **Pod:** the smallest unit Kubernetes runs; each CloudCart pod wraps one container.
- **Deployment:** keeps 2 CloudCart replicas running and restarts failed ones.
- **Service:** gives the pods one stable address and load-balances traffic across them (visible via the Container Host name changing).
- **Scalability and self-healing:** `kubectl scale deployment cloudcart-deployment --replicas=4` scales the app, and deleting a pod (`kubectl delete pod <name>`) shows Kubernetes replacing it automatically.
