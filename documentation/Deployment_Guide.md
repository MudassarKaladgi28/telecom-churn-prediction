# Deployment Guide: Telecom Churn Risk App

## What the app does
Takes one customer's details and returns a churn risk score from the saved XGBoost pipeline. The score ranks customers by relative risk; it is not an exact probability.

## Requirements
- Python 3.11
- Packages listed in `requirements.txt` (the saved model only loads reliably with similar library versions)

## Run locally
1. Create an environment and install the packages:
   ```
   conda create -n churn_env python=3.11 -y
   conda activate churn_env
   pip install -r requirements.txt
   ```
2. From the project root folder, start the app:
   ```
   python -m streamlit run app/app.py
   ```
3. Open the address shown in the terminal (usually http://localhost:8501).

## Project files the app needs
- `app/app.py` (the interface)
- `src/features.py` and `src/predict.py` (feature creation and prediction)
- `models/churn_xgb_pipeline.joblib` and `models/input_columns.joblib`

## Testing
Enter this profile; the expected score is 0.819: tenure 2, Month-to-month, Electronic check, paperless billing Yes, monthly charges 85.0, total charges 170.0, Senior/Partner/Dependents No, Phone service Yes, Fiber optic, all add-ons No, multiple lines No.
A second check: tenure 60, Two year, Credit card (automatic), paperless No, monthly 70.0, total 4200.0, Senior No, Partner Yes, Dependents Yes, Phone Yes, DSL, security/backup/protection/tech support Yes, streaming No, multiple lines No. Expected score: 0.098.

## Troubleshooting
- `No module named streamlit`: the environment is not active or packages are missing; activate it and install `requirements.txt`.
- `ModuleNotFoundError: No module named 'src'`: start the app from the project root.
- Model loading errors mentioning versions: use the library versions in `requirements.txt`, or re-save the model in your environment.
- Only load `.joblib` files you created yourself; they can run code if they come from an untrusted source.

## Limitations
Trained on a public sample dataset for demonstration. Scores are not calibrated probabilities. The model is not suitable for real customer decisions without validation on the company's own data.
