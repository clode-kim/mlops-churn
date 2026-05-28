import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check
from pathlib import Path
from typing import Union


# 데이터 계약(data contract): 컬럼 타입과 허용 범위를 명시한다.
# 프로덕션에서 스키마 위반 시 SchemaError를 발생시켜 파이프라인을 중단시킨다.
CHURN_SCHEMA = DataFrameSchema(
    columns={
        "customerID":       Column(str),
        "gender":           Column(str, Check.isin(["Male", "Female"])),
        "SeniorCitizen":    Column(int, Check.isin([0, 1])),
        "Partner":          Column(str, Check.isin(["Yes", "No"])),
        "Dependents":       Column(str, Check.isin(["Yes", "No"])),
        "tenure":           Column(int, Check(lambda x: x >= 0)),
        "PhoneService":     Column(str, Check.isin(["Yes", "No"])),
        "MultipleLines":    Column(str),
        "InternetService":  Column(str, Check.isin(["DSL", "Fiber optic", "No"])),
        "OnlineSecurity":   Column(str),
        "OnlineBackup":     Column(str),
        "DeviceProtection": Column(str),
        "TechSupport":      Column(str),
        "StreamingTV":      Column(str),
        "StreamingMovies":  Column(str),
        "Contract":         Column(str, Check.isin(["Month-to-month", "One year", "Two year"])),
        "PaperlessBilling": Column(str, Check.isin(["Yes", "No"])),
        "PaymentMethod":    Column(str),
        "MonthlyCharges":   Column(float, Check(lambda x: x >= 0)),
        "TotalCharges":     Column(float, Check(lambda x: x >= 0)),
        "Churn":            Column(str, Check.isin(["Yes", "No"])),
    }
)


def load_raw(path: Union[str, Path]) -> pd.DataFrame:
    """CSV를 읽고 pandera 스키마를 통과한 DataFrame을 반환한다."""
    df = pd.read_csv(path)

    # TotalCharges: 공백 문자열(" ")이 섞여 있어 object 타입으로 읽힌다.
    # 공백을 NaN으로 바꾼 뒤 float 변환하고, 결측행은 제거한다.
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna(subset=["TotalCharges"]).reset_index(drop=True)

    return CHURN_SCHEMA.validate(df)