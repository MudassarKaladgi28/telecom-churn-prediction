import sys
from pathlib import Path

# Let the app find the src folder (Streamlit does not add the project root by default)
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.predict import predict_churn

st.set_page_config(page_title="Telecom Churn Risk", page_icon="📉")
st.title("Telecom Customer Churn Risk")
st.write("Enter a customer's details to get the model's churn risk score. "
         "The score ranks customers by risk; it is not an exact probability.")

# ---- Account details ----
st.subheader("Account")
col1, col2 = st.columns(2)
tenure = col1.slider("Tenure (months)", 0, 72, 12)
contract = col2.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
payment = col1.selectbox("Payment method", ["Electronic check", "Mailed check",
                                            "Bank transfer (automatic)", "Credit card (automatic)"])
paperless = col2.selectbox("Paperless billing", ["Yes", "No"])
monthly = col1.number_input("Monthly charges", 18.0, 120.0, 70.0, step=0.5)
total = col2.number_input("Total charges so far", 0.0, 9000.0, float(round(tenure * monthly, 2)), step=10.0)

# ---- Customer details ----
st.subheader("Customer")
col3, col4, col5 = st.columns(3)
senior = col3.selectbox("Senior citizen", ["No", "Yes"])
partner = col4.selectbox("Partner", ["No", "Yes"])
dependents = col5.selectbox("Dependents", ["No", "Yes"])

# ---- Services ----
st.subheader("Services")
phone = st.selectbox("Phone service", ["Yes", "No"])
internet = st.selectbox("Internet service", ["Fiber optic", "DSL", "No"])

# Add-ons only make sense with internet; the model was trained with "No" in that case
addon_names = ["OnlineSecurity", "OnlineBackup", "DeviceProtection",
               "TechSupport", "StreamingTV", "StreamingMovies"]
addons = {}
if internet == "No":
    st.caption("No internet service, so add-on services are set to No.")
    for a in addon_names:
        addons[a] = "No"
else:
    cols = st.columns(3)
    for i, a in enumerate(addon_names):
        addons[a] = cols[i % 3].selectbox(a, ["No", "Yes"], key=a)

if phone == "Yes":
    multiple = st.selectbox("Multiple lines", ["No", "Yes"])
else:
    multiple = "No"      # the model was trained with "No phone service" merged into "No"

# ---- Predict ----
if st.button("Predict churn risk"):
    customer = {
        'SeniorCitizen': 1 if senior == "Yes" else 0,
        'Partner': partner, 'Dependents': dependents, 'tenure': tenure,
        'PhoneService': phone, 'MultipleLines': multiple, 'InternetService': internet,
        **addons,
        'Contract': contract, 'PaperlessBilling': paperless,
        'PaymentMethod': payment, 'MonthlyCharges': monthly, 'TotalCharges': total,
    }
    score = predict_churn(customer)
    st.metric("Churn risk score", f"{score:.3f}")
    st.progress(min(max(score, 0.0), 1.0))
    st.caption("Scores come from a model trained on a public sample dataset and are "
               "for demonstration. They show relative risk, not the chance this customer will leave.")
