import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score

# Load data
train_df = pd.read_csv('data/processed/train.csv')
val_df = pd.read_csv('data/processed/val.csv')

X_train = train_df['cleaned_text']
y_train = train_df[['urgency', 'authority', 'fear', 'impersonation']]

X_val = val_df['cleaned_text']
y_val = val_df[['urgency', 'authority', 'fear', 'impersonation']]

# Vectorization (Baseline)
# ngram_range=(1,2) helps capture phrases like "bank account" or "CEO said"
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)

# Multi-label classifier baseline
clf = OneVsRestClassifier(LogisticRegression(solver='liblinear'))
clf.fit(X_train_vec, y_train)

# Evaluation
y_pred = clf.predict(X_val_vec)
report = classification_report(y_val, y_pred, target_names=['urgency', 'authority', 'fear', 'impersonation'])
print("Validation Report:\n", report)

# Save artifacts
os.makedirs('models', exist_ok=True)
joblib.dump(vectorizer, 'models/vectorizer_baseline.joblib')
joblib.dump(clf, 'models/model_baseline.joblib')

print("Baseline model and vectorizer saved to models/")
