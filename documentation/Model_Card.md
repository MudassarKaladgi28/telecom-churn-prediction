# Model Card: Telecom Customer Churn Risk Model

## Model details
- **Task:** binary classification, predicting whether a telecom customer churns (Yes/No)
- **Final model:** XGBoost classifier inside a scikit-learn Pipeline (StandardScaler on numeric features, one-hot encoding on categorical features, then XGBoost)
- **Tuned settings:** n_estimators 200, max_depth 5, learning_rate 0.01, subsample 0.7, colsample_bytree 1.0, min_child_weight 1; class imbalance handled with scale_pos_weight 2.77
- **Benchmark:** Logistic Regression (C = 10, L2 penalty, class_weight balanced)
- **Libraries:** scikit-learn 1.9.1, xgboost 3.4.2 (see requirements.txt; saved model files are tied to library versions)
- **Trained:** November 2026
- **Developer:** Mudassar Kaladgi

## Intended use
- Demonstration and portfolio project showing an end-to-end churn workflow.
- Illustrates how a telecom retention team could rank customers by relative churn risk to prioritise outreach.

## Out-of-scope use
- Real customer decisions (offers, pricing, service changes) without validation on the company's own data.
- Reading the score as a probability: class weights shift scores upward, so a score of 0.8 does not mean an 80% chance of churn.
- Any use that treats the model's output as a cause of churn.

## Training data
- Public sample dataset from Kaggle: 7,043 customers, 21 columns, 26.5% churned. [https://www.kaggle.com/datasets/blastchar/telco-customer-churn]
- Training set: 5,634 customers (80% stratified split); test set: 1,409 customers (374 churners).
- Inputs: 18 raw fields (demographics, account details, services, charges) plus 5 engineered features (tenure_group, num_addons, has_internet, auto_pay, has_support). `gender` was removed (no signal: 26.6% vs 26.4% churn) and `customerID` dropped.
- Data cleaning: 11 blank TotalCharges values (new customers, tenure 0) set to 0; "No internet service" and "No phone service" merged into "No".

## Performance
Test set, default 0.5 cutoff (1,409 customers):

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (tuned) | 0.740 | 0.507 | 0.791 | 0.618 | 0.842 |
| XGBoost (tuned, final) | 0.758 | 0.529 | 0.805 | 0.638 | 0.846 |

- XGBoost confusion matrix: 767 true negatives, 268 false positives, 73 false negatives, 301 true positives. It caught 301 of 374 churners and flagged 569 customers, of whom 52.9% were real churn risks.
- 5-fold cross-validation ROC-AUC on the training set: 0.846 ± 0.012 (Logistic Regression), 0.846 ± 0.011 (Random Forest), 0.846 ± 0.011 (XGBoost untuned); tuned XGBoost 0.848. These are statistically tied, and tuning gave no meaningful improvement.
- The cutoff is a business choice. On out-of-fold training predictions, XGBoost at cutoff 0.3 flags 54.3% of customers (precision 0.441, recall 0.902); at 0.7 it flags 23.2% (precision 0.650, recall 0.568).

## Interpretation
Most influential features (SHAP): month-to-month contract (by a wide margin), tenure, fiber optic internet, monthly charges, electronic check payment, one-year contract. Month-to-month contracts, short tenure, fiber optic, electronic check, paperless billing and streaming movies raise predicted risk; support and security add-ons and having no internet service lower it. SHAP describes what the model relies on, not what causes churn.

## Fairness and bias
- Checked on SeniorCitizen only (test set, 0.5 cutoff): non-seniors (n = 1,187) have actual churn 23.3%, flagged 35.6%, recall 0.764, precision 0.500; seniors (n = 222) have actual churn 44.1%, flagged 66.2%, recall 0.918, precision 0.612.
- The model flags both groups at about 1.5 times their actual churn rate, but flags two thirds of senior customers, so outreach volume and customer experience for that group need care.
- Gender was removed because it carried no signal. No other groups were evaluated, and other columns can act as stand-ins for sensitive characteristics, so this is not a general fairness guarantee.

## Limitations
- Public sample data, one snapshot, no time dimension.
- Associations, not causes; SHAP credit is shared between overlapping features.
- All models tie at about 0.84 ROC-AUC, so the limit appears to be the information in the data.
- Retention costs and offer effectiveness are unknown, so the best cutoff cannot be determined here.
- Test figures come from one split and carry sampling noise (374 churners).

## Maintenance
Not monitored or retrained. In a real deployment, performance should be monitored for drift and the model retrained on current data.
