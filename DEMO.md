# Demo Script (≈10 minutes)

Repo: https://github.com/ar-ush/MlOpsProjectHeartDiseasePrediction
Image: https://hub.docker.com/r/arushspam/heart-disease-api

## 0. Before the demo (do 10 minutes early)
1. Open **Docker Desktop**, wait for "Engine running".
2. `minikube start --driver=docker`
3. `kubectl get pods` — wait until all three pods are `Running` (apply with `kubectl apply -f k8s/` if empty).

## 1. ML pipeline + experiment tracking
```powershell
.venv\Scripts\activate
$env:PYTHONUTF8=1
python src/preprocess.py; python src/train.py; python src/evaluate.py
mlflow ui --port 5000        # open http://localhost:5000
```
Show: 3 models compared, champion = Logistic Regression (F1 0.84), quality gate (F1 >= 0.75).

## 2. CI/CD (GitHub Actions)
Open the repo → **Actions** tab → latest "MLOps Pipeline" run.
Jobs: **Train & Evaluate** → **Build & push Docker Image** → **Kubernetes deploy smoke test**.
Then show the image tags on Docker Hub.

## 3. Docker Compose (Streamlit + Prometheus + Grafana)
```powershell
docker compose up -d
```
| What | URL |
|------|-----|
| Streamlit app | http://localhost:8501 |
| Prometheus (Status → Targets = UP) | http://localhost:9090 |
| Grafana (admin / admin) → Dashboards → MLOps → Heart Disease MLOps | http://localhost:3000 |

Make ~10 predictions in Streamlit, then in Prometheus run `streamlit_predictions_total`
and watch the Grafana panels move. `docker compose down` when done (frees ports for step 4).

## 4. Kubernetes (Minikube)
```powershell
kubectl get pods,svc
kubectl port-forward svc/heart-disease-streamlit-service 8501:8501   # terminal 1
kubectl port-forward svc/prometheus 9090:9090                        # terminal 2
kubectl port-forward svc/grafana 3000:3000                           # terminal 3
```
Same URLs as above. Each port-forward blocks its terminal; Ctrl+C to stop.

Optional rolling update: edit a title in `src/streamlit_app.py`, push, wait for CI, then
`kubectl rollout restart deployment/heart-disease-streamlit`.

## 5. Cleanup
```powershell
docker compose down -v
minikube delete --all
```
