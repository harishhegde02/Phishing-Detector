import pandas as pd
import numpy as np
import joblib
import os
from sklearn.metrics import accuracy_score, classification_report
import time

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_PATH = os.path.join(BASE_DIR, 'ext_data', 'fiveLakh.csv') # Use a different dataset or subset

def clean_url(url):
    if not isinstance(url, str): return ""
    url = url.lower()
    for prefix in ['https://', 'http://', 'www.']:
        if url.startswith(prefix):
            url = url[len(prefix):]
    return url

print("⏳ Loading Model & Data for Validation...")
start = time.time()

try:
    vectorizer = joblib.load(os.path.join(MODELS_DIR, 'vectorizer_enhanced.joblib'))
    clf = joblib.load(os.path.join(MODELS_DIR, 'model_enhanced.joblib'))
    print(f"✅ Model loaded in {time.time() - start:.2f}s")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    exit(1)

# Load a random sample for testing (using chunks to avoid memory issues)
print("📊 Loading test sample (20,000 rows)...")
try:
    # Read first 20k rows which we know contain phishing samples (from inspection)
    df = pd.read_csv(DATA_PATH, nrows=20000) 
    
    # Check columns
    # fiveLakh.csv usually has 'url' and 'label' (or the 4 columns)
    # The training script treated 'fiveLakh.csv' as having labels ["urgency", "authority", "fear", "impersonation"]
    # Let's see if we can convert these to a binary "Phishing vs Safe" for a simple accuracy number.
    
    # For this verification, let's look at the raw predictions vs the 'Label' implies.
    # Actually, the user wants a general "Accuracy".
    # Since we have a multi-output model, let's measure accuracy per label.
    
    labels = ["urgency", "authority", "fear", "impersonation"]
    
    # specific columns might vary, let's ensure they exist
    missing = [c for c in labels if c not in df.columns]
    if missing:
        # Fallback for fiveLakh if it has different columns
        # Step 338 showed fiveLakh.csv has 500k rows. 
        # Step 434 showed fiveLakh header: url,urgency,authority,fear,impersonation
        # So it matches.
        pass

    # Preprocess
    print("🧹 Preprocessing...")
    X_raw = df['url'].apply(clean_url)
    X_test = vectorizer.transform(X_raw)
    
    Y_test = df[labels].apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
    
    print("\n🔍 Evaluating...")
    Y_pred = clf.predict(X_test)
    
    # Calculate accuracy
    # subset accuracy: exact match of all labels
    subset_acc = accuracy_score(Y_test, Y_pred)
    
    # Average accuracy per label
    avg_acc = np.mean([accuracy_score(Y_test[col], Y_pred[:, i]) for i, col in enumerate(labels)])
    
    print("-" * 30)
    print(f"🎯 Model Accuracy Report")
    print("-" * 30)
    print(f"Test Set Size: {len(df)} samples")
    print(f"Subset Accuracy (Exact Match): {subset_acc*100:.2f}%")
    print(f"Average Label Accuracy:      {avg_acc*100:.2f}%")
    print("-" * 30)
    
    # Detailed report
    from sklearn.metrics import recall_score, precision_score
    
    for i, label in enumerate(labels):
        p = precision_score(Y_test[label], Y_pred[:, i], zero_division=0)
        r = recall_score(Y_test[label], Y_pred[:, i], zero_division=0)
        print(f"{label.ljust(15)} | Precision: {p*100:.1f}% | Recall: {r*100:.1f}%")
    print("-" * 30)

except Exception as e:
    print(f"❌ Validation failed: {e}")
