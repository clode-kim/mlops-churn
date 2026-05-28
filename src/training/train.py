import os
import mlflow
import mlflow.sklearn
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import roc_auc_score, f1_score, classification_report
from xgboost import XGBClassifier

from src.data.load import load_raw

# 데이터 경로
DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# 학습에 쓸 피처 컬럼 (customerID는 식별자라 제외)
CATEGORICAL_COLS = [
    "gender", "Partner", "Dependents", "PhoneService", "MultipleLines",
    "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies", "Contract",
    "PaperlessBilling", "PaymentMethod",
]
NUMERICAL_COLS = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
FEATURE_COLS = CATEGORICAL_COLS + NUMERICAL_COLS
TARGET_COL = "Churn"


def build_pipeline(scale_pos_weight: float) -> Pipeline:
    """전처리 + XGBoost를 하나의 Pipeline으로 묶는다."""
    preprocessor = ColumnTransformer(
        transformers=[
            # 범주형 컬럼: 문자열 → 정수 (XGBoost가 이해할 수 있는 형태)
            ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CATEGORICAL_COLS),
            # 수치형 컬럼: 그대로 통과 (XGBoost는 스케일링 불필요)
            ("num", "passthrough", NUMERICAL_COLS),
        ]
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        # 클래스 불균형 보정: No(다수):Yes(소수) 비율을 가중치로 준다
        scale_pos_weight=scale_pos_weight,
        eval_metric="logloss",
        random_state=42,
        verbosity=0,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def train():
    df = load_raw(DATA_PATH)

    # 타겟을 0/1로 변환 (Yes → 1, No → 0)
    df[TARGET_COL] = (df[TARGET_COL] == "Yes").astype(int)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    # 클래스 불균형 비율 계산 (No 수 / Yes 수)
    scale_pos_weight = (y == 0).sum() / (y == 1).sum()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://20.200.246.155:5000"))
    mlflow.set_experiment("churn-prediction")

    with mlflow.start_run():
        # autolog: 파라미터·지표·모델을 MLflow가 자동으로 기록
        mlflow.sklearn.autolog(log_model_signatures=True)

        pipeline = build_pipeline(scale_pos_weight)
        pipeline.fit(X_train, y_train)

        # 추가 지표: AUC, F1 (이탈 탐지에서 중요한 지표)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        y_pred = pipeline.predict(X_test)

        auc = roc_auc_score(y_test, y_prob)
        f1 = f1_score(y_test, y_pred)

        mlflow.log_metric("test_roc_auc", auc)
        mlflow.log_metric("test_f1", f1)

        print(f"\n--- 학습 완료 ---")
        print(f"ROC-AUC : {auc:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"\n{classification_report(y_test, y_pred, target_names=['No Churn', 'Churn'])}")


if __name__ == "__main__":
    train()