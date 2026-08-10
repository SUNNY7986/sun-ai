import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier


data = {
    "incident": [
        "Multiple failed login attempts",
        "SQL query with OR 1=1",
        "JavaScript injected into webpage",
        "Malware detected on endpoint",
        "Large number of requests from one IP",
        "Suspicious phishing email received",
        "Repeated SSH login failures",
        "Cross-site scripting payload detected"
    ],
    "severity": [
        "High",
        "Critical",
        "High",
        "Critical",
        "Medium",
        "Medium",
        "High",
        "High"
    ]
}

df = pd.DataFrame(data)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", RandomForestClassifier(random_state=42))
])

model.fit(df["incident"], df["severity"])

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/severity_model.pkl")

print("Model trained successfully.")