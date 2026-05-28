import pytest
import pandas as pd
import pandera as pa
from pathlib import Path

from src.data.load import load_raw

DATA_PATH = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")


@pytest.fixture(scope="module")
def df():
    return load_raw(DATA_PATH)


def test_row_count(df):
    # 공백 TotalCharges 11건 제거 후 7032행이어야 함
    assert len(df) == 7032


def test_column_count(df):
    assert len(df.columns) == 21


def test_churn_column_exists(df):
    assert "Churn" in df.columns


def test_total_charges_is_float(df):
    # load_raw 내부에서 object → float 변환이 됐는지 확인
    assert df["TotalCharges"].dtype == float


def test_no_missing_values(df):
    assert df.isnull().sum().sum() == 0


def test_churn_values_are_valid(df):
    assert set(df["Churn"].unique()) == {"Yes", "No"}


def test_schema_rejects_bad_data():
    # 허용되지 않는 gender 값이 들어오면 pandera가 에러를 내야 한다
    bad_df = pd.DataFrame({
        "customerID": ["fake-001"],
        "gender": ["Unknown"],   # "Male" / "Female" 외의 값
        "SeniorCitizen": [0], "Partner": ["No"], "Dependents": ["No"],
        "tenure": [1], "PhoneService": ["Yes"], "MultipleLines": ["No"],
        "InternetService": ["DSL"], "OnlineSecurity": ["No"],
        "OnlineBackup": ["No"], "DeviceProtection": ["No"],
        "TechSupport": ["No"], "StreamingTV": ["No"], "StreamingMovies": ["No"],
        "Contract": ["Month-to-month"], "PaperlessBilling": ["Yes"],
        "PaymentMethod": ["Electronic check"],
        "MonthlyCharges": [50.0], "TotalCharges": [50.0], "Churn": ["No"],
    })
    with pytest.raises(pa.errors.SchemaError):
        from src.data.load import CHURN_SCHEMA
        CHURN_SCHEMA.validate(bad_df)