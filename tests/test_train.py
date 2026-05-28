import pytest
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.training.train import build_pipeline, FEATURE_COLS, CATEGORICAL_COLS


@pytest.fixture(scope="module")
def trained_pipeline():
    """작은 더미 데이터로 Pipeline을 학습시켜 반환한다."""
    from src.data.load import load_raw
    from pathlib import Path

    df = load_raw(Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"))
    df["Churn"] = (df["Churn"] == "Yes").astype(int)

    X = df[FEATURE_COLS].head(200)
    y = df["Churn"].head(200)

    pipeline = build_pipeline(scale_pos_weight=2.76)
    pipeline.fit(X, y)
    return pipeline


def test_pipeline_is_sklearn_pipeline(trained_pipeline):
    assert isinstance(trained_pipeline, Pipeline)


def test_predict_returns_binary(trained_pipeline):
    from src.data.load import load_raw
    from pathlib import Path

    df = load_raw(Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"))
    X_sample = df[FEATURE_COLS].head(10)

    preds = trained_pipeline.predict(X_sample)
    assert set(preds).issubset({0, 1})


def test_predict_proba_sums_to_one(trained_pipeline):
    from src.data.load import load_raw
    from pathlib import Path

    df = load_raw(Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"))
    X_sample = df[FEATURE_COLS].head(10)

    proba = trained_pipeline.predict_proba(X_sample)
    # 각 행의 확률 합이 1이어야 한다
    assert np.allclose(proba.sum(axis=1), 1.0)


def test_pipeline_output_shape(trained_pipeline):
    from src.data.load import load_raw
    from pathlib import Path

    df = load_raw(Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"))
    X_sample = df[FEATURE_COLS].head(10)

    preds = trained_pipeline.predict(X_sample)
    assert len(preds) == 10