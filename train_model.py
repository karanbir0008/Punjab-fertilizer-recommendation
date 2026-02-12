import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report

# to load dataset
df = pd.read_csv("final_dataset.csv")

# we will shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

#handling of NaN
# -1 means "not applicable" (rice)
if "irrigation_count" in df.columns:
    df["irrigation_count"] = df["irrigation_count"].fillna(-1)

# labels and features
target_cols = ["N_class", "P_class", "K_class"]
X = df.drop(columns=target_cols)
y = df[target_cols]


label_encoders = {}

for col in X.columns:
    if X[col].dtype == "object":
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

# Encode targets
target_encoders = {}
for col in y.columns:
    le = LabelEncoder()
    y[col] = le.fit_transform(y[col])
    target_encoders[col] = le

#train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# model
base_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model = MultiOutputClassifier(base_model)


model.fit(X_train, y_train)

#evaluation
y_pred = model.predict(X_test)

print("\n=== NITROGEN (N) ===")
print(classification_report(y_test.iloc[:, 0], y_pred[:, 0]))

print("\n=== PHOSPHORUS (P) ===")
print(classification_report(y_test.iloc[:, 1], y_pred[:, 1]))

print("\n=== POTASSIUM (K) ===")
print(classification_report(y_test.iloc[:, 2], y_pred[:, 2]))



# Saveing trained model
joblib.dump(model, "model.joblib")

# Save feature encoders
joblib.dump(label_encoders, "feature_encoders.joblib")

# Save target encoders
joblib.dump(target_encoders, "target_encoders.joblib")

print("Model and encoders saved successfully")
