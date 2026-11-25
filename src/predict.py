from pathlib import Path
import joblib
import pandas as pd
from src.features import add_features

# models/ folder sits next to src/
MODEL_DIR = Path(__file__).resolve().parent.parent / 'models'

_pipeline = joblib.load(MODEL_DIR / 'churn_xgb_pipeline.joblib')
_columns = joblib.load(MODEL_DIR / 'input_columns.joblib')

def predict_churn(customer: dict) -> float:
    """Return the churn probability (0 to 1) for one customer given raw fields."""
    df = pd.DataFrame([customer])          # one-row table
    df = add_features(df)                  # same features as in training
    df = df[_columns]                      # same column order as in training
    return float(_pipeline.predict_proba(df)[0, 1])
