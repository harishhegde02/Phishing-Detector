from fastapi import APIRouter, Depends, HTTPException
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.inference import get_inference_service, InferenceService

router = APIRouter(prefix="/api/v1", tags=["analysis"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_message(
    request: AnalysisRequest, 
    service: InferenceService = Depends(get_inference_service)
):
    try:
        results = service.analyze_text(request.text)
        return {
            "text": request.text,
            "max_risk_score": results["max_risk_score"],
            "detections": results["detections"],
            "model_version": "1.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
