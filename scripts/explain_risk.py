import joblib
import pandas as pd
import numpy as np

# Load artifacts
vectorizer = joblib.load('models/vectorizer_baseline.joblib')
clf = joblib.load('models/model_baseline.joblib')

labels = ['urgency', 'authority', 'fear', 'impersonation']
feature_names = vectorizer.get_feature_names_out()

def get_risk_explanation(text):
    # Vectorize input
    X_vec = vectorizer.transform([text])
    
    # Get probabilities
    # For OneVsRestClassifier, predict_proba returns (n_samples, n_classes)
    probs_array = clf.predict_proba(X_vec)
    probs = probs_array[0] # First (and only) sample
    
    explanation = {
        "text": text,
        "max_risk_score": float(np.max(probs)),
        "labels": {}
    }
    
    # Identify top contributing words for each positive label
    for i, label in enumerate(labels):
        prob = probs[i]
        explanation["labels"][label] = {
            "probability": float(prob),
            "top_features": []
        }
        
        if prob > 0.3: # Only explain if there's some signal
            # Get coefficients for this specific estimator
            coef = clf.estimators_[i].coef_[0]
            
            # Find feature indices present in the current text
            feature_indices = X_vec.indices
            
            # Map indices to names and coefficients
            contrib = []
            for idx in feature_indices:
                contrib.append((feature_names[idx], coef[idx]))
            
            # Sort by coefficient value (magnitude of contribution)
            contrib.sort(key=lambda x: x[1], reverse=True)
            explanation["labels"][label]["top_features"] = [
                {"word": word, "weight": float(weight)} for word, weight in contrib[:3] if weight > 0
            ]
            
    return explanation

# Test
if __name__ == "__main__":
    test_texts = [
        "URGENT: Your account will be locked in 1 hour!",
        "Hi mom, I lost my phone. Send money please.",
        "The project meeting is at 5 PM today.",
        "This is the CEO. I need the payroll file immediately."
    ]
    
    for t in test_texts:
        res = get_risk_explanation(t)
        print(f"\nText: {t}")
        print(f"Risk Score: {res['max_risk_score']:.2f}")
        for lbl, info in res['labels'].items():
            if info['probability'] > 0.5:
                print(f"  - Detected: {lbl} ({info['probability']:.2f})")
                if info['top_features']:
                    words = ", ".join([f"{f['word']}" for f in info['top_features']])
                    print(f"    Reason: Keywords [{words}] triggered the risk.")
