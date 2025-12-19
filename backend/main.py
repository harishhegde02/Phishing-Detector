from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os
import sys

# Add parent directory to path to access models if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Social Engineering Detection API")

# Enable CORS for Next.js app (usually on localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load artifacts
try:
    vectorizer = joblib.load('../models/vectorizer_baseline.joblib')
    clf = joblib.load('../models/model_baseline.joblib')
except Exception as e:
    print(f"Error loading models: {e}")
    # Fallback paths for different execution contexts
    vectorizer = joblib.load('models/vectorizer_baseline.joblib')
    clf = joblib.load('models/model_baseline.joblib')

labels = ['urgency', 'authority', 'fear', 'impersonation']
feature_names = vectorizer.get_feature_names_out()

class DetectionRequest(BaseModel):
    text: str

class FeatureImportance(BaseModel):
    word: str
    weight: float

class LabelResult(BaseModel):
    probability: float
    top_features: list[FeatureImportance]

class DetectionResponse(BaseModel):
    text: str
    max_risk_score: float
    labels: dict[str, LabelResult]

@app.post("/detect", response_model=DetectionResponse)
async def detect_attack(request: DetectionRequest):
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    # Vectorize input
    X_vec = vectorizer.transform([text])
    
    # Get probabilities
    probs_array = clf.predict_proba(X_vec)
    probs = probs_array[0]
    
    results_labels = {}
    
    # Identify top contributing words for each positive label
    for i, label in enumerate(labels):
        prob = float(probs[i])
        results_labels[label] = {
            "probability": prob,
            "top_features": []
        }
        
        if prob > 0.1: # Expanded threshold for UI visibility
            coef = clf.estimators_[i].coef_[0]
            feature_indices = X_vec.indices
            
            contrib = []
            for idx in feature_indices:
                contrib.append((feature_names[idx], float(coef[idx])))
            
            contrib.sort(key=lambda x: x[1], reverse=True)
            results_labels[label]["top_features"] = [
                {"word": word, "weight": weight} for word, weight in contrib[:3] if weight > 0
            ]
            
    return {
        "text": text,
        "max_risk_score": float(np.max(probs)),
        "labels": results_labels
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
