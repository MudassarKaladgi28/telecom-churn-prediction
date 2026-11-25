import pandas as pd

# The six add-on service columns
ADDONS = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
          'TechSupport', 'StreamingTV', 'StreamingMovies']

def add_features(data):
    """Create the engineered features from one or more customers' raw columns."""
    data = data.copy()
    data['tenure_group'] = pd.cut(data['tenure'], bins=[-1, 12, 24, 48, 72],
                                  labels=['0-12', '13-24', '25-48', '49-72']).astype(str)
    data['num_addons'] = (data[ADDONS] == 'Yes').sum(axis=1)
    data['has_internet'] = (data['InternetService'] != 'No').astype(int)
    data['auto_pay'] = data['PaymentMethod'].isin(
        ['Bank transfer (automatic)', 'Credit card (automatic)']).astype(int)
    data['has_support'] = ((data['OnlineSecurity'] == 'Yes') |
                           (data['TechSupport'] == 'Yes')).astype(int)
    return data
