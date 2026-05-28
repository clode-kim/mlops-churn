# MLOps Churn Prediction Pipeline

고객 이탈 예측 모델의 학습부터 서빙·모니터링·자동 재학습까지 전체 생애주기를 자동화한 MLOps 포트폴리오 프로젝트.

## Architecture

```
Data → Validation(pandera) → Training(XGBoost) → Registry(MLflow)
                                                        ↓
Monitoring(Evidently) ← Serving(FastAPI/K8s) ← Production Model
     ↓ drift detected
Auto Retrain (GitHub Actions)
```

## Tech Stack

| 영역 | 기술 |
|------|------|
| Infra | Terraform → Azure (AKS, ACR, Blob, PostgreSQL, Key Vault) |
| ML | scikit-learn, XGBoost, MLflow |
| Serving | FastAPI on Kubernetes |
| CI/CD | GitHub Actions (OIDC) |
| Monitoring | Prometheus + Grafana + Evidently |
| Notifications | Microsoft Teams (Power Automate Workflows) |
| Data Validation | pandera |

## Roadmap

- [x] **Phase 0** — 로컬 baseline: 데이터 로드, 모델 학습, MLflow 실험 기록
- [ ] **Phase 1** — Terraform으로 Azure 인프라 프로비저닝
- [ ] **Phase 2** — MLflow on AKS + 모델 레지스트리 등록
- [ ] **Phase 3** — FastAPI 서빙, Production 모델 자동 로드
- [ ] **Phase 4** — GitHub Actions CI/CD (OIDC 인증)
- [ ] **Phase 5** — Prometheus + Grafana + Evidently 드리프트 감지 → 자동 재학습

## Quick Start

```bash
# 1. 가상환경 설치
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt

# 2. 데이터 준비
# Kaggle에서 Telco Customer Churn 데이터셋 다운로드 후
# data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv 에 배치

# 3. 모델 학습
python -m src.training.train

# 4. MLflow UI 확인
mlflow ui --port 5000
# http://localhost:5000

# 5. 테스트 실행
pytest tests/ -v
```

## Dataset

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle)
- 7,043 rows × 21 columns
- Target: `Churn` (Yes/No) — 클래스 불균형 27% : 73%

## Model Performance (Phase 0 Baseline)

| Metric | Score |
|--------|-------|
| ROC-AUC | 0.829 |
| F1 (Churn) | 0.622 |
| Recall (Churn) | 0.790 |