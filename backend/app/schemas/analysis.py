from pydantic import BaseModel, Field
from typing import List, Dict

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)

class FeatureContribution(BaseModel):
    word: str
    weight: float

class LabelAnalysis(BaseModel):
    probability: float
    top_features: List[FeatureContribution] = Field(default_factory=list)

class AnalysisResponse(BaseModel):
    text: str
    max_risk_score: float
    detections: Dict[str, LabelAnalysis]
    model_version: str = "1.0.0"
