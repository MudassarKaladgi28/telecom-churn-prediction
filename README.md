# Telecom Customer Churn Prediction and Retention Strategy

A machine learning project that predicts which telecom customers are likely to leave, explains what drives churn, and turns the findings into retention recommendations. It includes a Streamlit app that scores one customer at a time.

> Built on a public sample dataset for learning and portfolio purposes. The results demonstrate a method, not outcomes at a real company.

## Business problem
A telecom operator loses customers every month, and winning a new customer costs more than keeping one. Retention offers cannot go to everyone, so the company needs to know which customers are at risk and why they leave.

**Objective:** predict churn, identify its main drivers, and recommend targeted retention actions.

## Dataset
- 7,043 customers, 21 columns, one row per customer. Target: `Churn` (Yes/No); 26.5% of customers churned (1,869).
- Source: [https://www.kaggle.com/datasets/blastchar/telco-customer-churn]
- The dataset is not included in this repository. Download it and save it as `data/Telco-Customer-Churn.csv`.

## Approach
1. **Cleaning:** no duplicate rows or standard missing values. 11 blank `TotalCharges` values (all with tenure 0, i.e. new customers) were set to 0. "No internet service" / "No phone service" were merged into "No". `customerID` was dropped. The IQR method found no outliers in tenure, MonthlyCharges or TotalCharges.
2. **EDA** on the training set only.
3. **Feature engineering:** `tenure_group`, `num_addons`, `has_internet`, `auto_pay`, `has_support`, each computed from a single customer's own row (no leakage). `gender` was dropped: churn was 26.6% (female) vs 26.4% (male), so it carried no signal.
4. **Split and preprocessing:** 80/20 stratified split (5,634 train / 1,409 test). Scaling and one-hot encoding are inside a scikit-learn Pipeline, fitted on training data only.
5. **Models:** dummy baseline, Logistic Regression, Random Forest, XGBoost, with class weights for the imbalance.
6. **Evaluation and tuning:** 5-fold stratified cross-validation on the training set; GridSearchCV (Logistic Regression) and RandomizedSearchCV with 20 candidates (XGBoost), optimizing ROC-AUC. Tuning used the training set only.
7. **Interpretation:** SHAP, plus a fairness check across senior and non-senior customers.

## Key findings from the EDA (training set)
| Finding | Evidence |
|---|---|
| Month-to-month contracts churn most | 42.8% vs 11.1% (one year) vs 2.9% (two year) |
| Churn happens early | 47.3% churn in months 0-12 vs 9.9% after month 48 |
| Fiber optic customers churn more | 42.1% vs 18.7% (DSL) vs 7.2% (no internet) |
| Electronic check payers churn most | 45.7% vs 14.9-19.3% for other methods |
| Security and support add-ons go with lower churn | Online Security 14.4% vs 31.4%; Tech Support 15.2% vs 31.2% |
| Highest-risk segment: fiber + month-to-month | 55.1% churn |

These are associations in the data, not proven causes.

## Model results
**5-fold cross-validation (training set):**

| Model | ROC-AUC | Recall | Precision | F1 |
|---|---|---|---|---|
| Logistic Regression | 0.846 ± 0.012 | 0.794 ± 0.042 | 0.516 ± 0.018 | 0.625 ± 0.024 |
| Random Forest | 0.846 ± 0.011 | 0.767 ± 0.022 | 0.542 ± 0.016 | 0.635 ± 0.016 |
| XGBoost | 0.846 ± 0.011 | 0.797 ± 0.025 | 0.526 ± 0.014 | 0.634 ± 0.016 |

**Test set (1,409 customers, default 0.5 cutoff), tuned models:**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (tuned) | 0.740 | 0.507 | 0.791 | 0.618 | 0.842 |
| XGBoost (tuned) | 0.758 | 0.529 | 0.805 | 0.638 | 0.846 |

Tuned XGBoost caught 301 of 374 churners (80.5%) and missed 73; of the 569 customers it flagged, 301 (52.9%) were real churn risks.

**The three models are statistically tied**, and tuning made no meaningful difference. Tuned XGBoost is the final model (highest tuned CV ROC-AUC, works with SHAP's tree explainer, common industry choice); Logistic Regression is kept as an explainable benchmark.

**Cutoff:** scores are not calibrated probabilities, because class weights shift them upward. Raising the cutoff flags fewer customers with higher precision and lower recall (XGBoost, out-of-fold on the training set: cutoff 0.3 flags 54.3% of customers with precision 0.441 and recall 0.902; cutoff 0.7 flags 23.2% with precision 0.650 and recall 0.568). The right cutoff depends on retention capacity and offer costs, which this dataset does not contain.

## What drives churn (SHAP)
The top features, in order: month-to-month contract (by a wide margin), tenure, fiber optic internet, monthly charges, electronic check payment, one-year contract. Month-to-month contracts, short tenure, fiber optic, electronic check, paperless billing and streaming movies push predicted risk up; support and security add-ons and having no internet service push it down. SHAP shows what the model relies on, not what causes churn.

## Fairness check (SeniorCitizen, test set, 0.5 cutoff)
| Group | Customers | Actual churn | Flagged | Recall | Precision |
|---|---|---|---|---|---|
| Non-senior | 1,187 | 23.3% | 35.6% | 0.764 | 0.500 |
| Senior | 222 | 44.1% | 66.2% | 0.918 | 0.612 |

The model flags both groups at about 1.5 times their actual churn rate. Two thirds of senior customers are flagged at this cutoff, so outreach workload and customer experience should be considered. The senior group is small, so these figures are noisy, and this one check does not prove the model is fair.

## Run the app
```
conda create -n churn_env python=3.11 -y
conda activate churn_env
pip install -r requirements.txt
python -m streamlit run app/app.py
```
See `documentation/Deployment_Guide.md` for test inputs and troubleshooting. Model files are tied to library versions, so use the versions in `requirements.txt`, and only load `.joblib` files you created yourself.

## Project structure
```
app/            Streamlit app (app.py)
data/           place Telco-Customer-Churn.csv here (not included)
documentation/  Deployment_Guide.md
models/         saved pipelines and input column list (.joblib)
notebooks/      01_telecom_churn_analysis.ipynb
src/            features.py, predict.py
requirements.txt
README.md
```
Run the notebook top to bottom to regenerate the model files; the searches take a few minutes.

## Limitations
- Public sample data and a single snapshot with no time dimension.
- Associations, not causes; SHAP credit is shared between overlapping features (tenure, TotalCharges and the contract columns).
- The models tie at about 0.84 ROC-AUC, so the limit appears to be the information in the data, not the algorithm.
- Retention costs and offer effectiveness are unknown.
- Fairness was checked only for SeniorCitizen at one cutoff.
- Test figures come from one split of 1,409 customers (374 churners) and carry sampling noise.

## Author
Mudassar Kaladgi
