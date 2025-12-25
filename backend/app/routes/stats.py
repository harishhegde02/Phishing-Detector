from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import ScanResult
from app import models
from typing import Dict, Any, List
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1", tags=["stats"])

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. KPI: Total Scans
    total_scans = db.query(ScanResult).count()

    # 2. KPI: Threats Blocked (High Risk + Suspicious)
    # Assuming anything >= 0.4 is "actionable"
    blocked_count = db.query(ScanResult).filter(
        ScanResult.risk_score >= 0.4
    ).count()

    critical_count = db.query(ScanResult).filter(
        ScanResult.risk_level == "HIGH_RISK"
    ).count()

    # 3. Recent Interventions (Recent Browsing History - All Scans)
    recent_risks = db.query(ScanResult).order_by(ScanResult.timestamp.desc()).limit(10).all()

    recent_data = [
        {
            "domain": r.domain,
            "timestamp": r.timestamp.isoformat() + "Z", # Force UTC interpretation
            "type": "Phishing" if "Impersonation" in (r.explanation or "") else ("Social Eng." if r.risk_score >= 0.4 else "Browsing"),
            "risk": r.risk_level.replace("_", " ") if r.risk_score >= 0.4 else "SAFE",
            "score": r.risk_score
        }
        for r in recent_risks
    ]

    # 4. Activity Trend (Last 7 days mock or real aggregated)
    # Real aggregation:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    
    daily_stats = db.query(
        func.date(ScanResult.timestamp).label('date'),
        func.count(ScanResult.id).label('count')
    ).filter(
        ScanResult.timestamp >= start_date
    ).group_by(
        func.date(ScanResult.timestamp)
    ).all()

    # Convert to dictionary for easy lookup
    stats_map = {str(d.date): d.count for d in daily_stats}
    
    # Fill gaps with 0
    trend_data = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        trend_data.append({
            "date": day.strftime("%a"), # Mon, Tue...
            "count": stats_map.get(day_str, 0)
        })

    return {
        "kpi": {
            "total_scans": total_scans,
            "threats_blocked": blocked_count,
            "critical_blocked": critical_count,
            "safety_score": max(0, 100 - (critical_count * 5)) # Clamped heuristic logic
        },
        "recent_interventions": recent_data,
        "activity_trend": trend_data
    }

@router.get("/activity", response_model=List[Dict[str, Any]])
async def get_activity_log(
    limit: int = 50, 
    offset: int = 0, 
    db: Session = Depends(get_db)
):
    scans = db.query(ScanResult).order_by(
        ScanResult.timestamp.desc()
    ).offset(offset).limit(limit).all()

    # Get all blocked domains for efficient checking
    blocked_domains = {b.domain for b in db.query(models.BlockedDomain).all()}

    activity_log = []
    for s in scans:
        # Check against blocklist
        is_blocked = False
        if s.domain:
            for blocked in blocked_domains:
                if s.domain == blocked or s.domain.endswith("." + blocked):
                    is_blocked = True
                    break

        # Infer category from explanation or risk
        category = "General"
        explanation = (s.explanation or "").lower()
        
        status = s.risk_level
        if is_blocked:
            status = "BLOCKED"
        elif s.risk_score > 0.8:
            status = "BLOCKED"
        elif s.risk_score > 0.5:
             status = "WARNED"
        else:
             status = "SAFE"

        if "impersonation" in explanation or "typosquatting" in explanation or "homoglyph" in explanation:
            category = "Phishing"
        elif "urgency" in explanation or "social engineering" in explanation:
            category = "Social Eng."
        elif s.risk_score > 0.7:
            category = "Critical"
        elif s.risk_score < 0.1:
            category = "Safe"
        
        # Override risk score for display if blocked
        display_score = 1.0 if is_blocked else s.risk_score
        display_level = "HIGH_RISK" if is_blocked else s.risk_level

        activity_log.append({
            "id": s.id,
            "domain": s.domain,
            "timestamp": f"{s.timestamp.isoformat()}Z" if s.timestamp else datetime.utcnow().isoformat() + "Z",
            "risk_score": display_score,
            "risk_level": display_level,
            "status": status,
            "category": category,
            "explanation": s.explanation,
            "is_blocked": is_blocked
        })
    
    return activity_log


@router.get("/cognitive-status")
async def get_cognitive_status(db: Session = Depends(get_db)):
    """
    Calculates current 'Cognitive Load' based on interaction density.
    Real-time metric: Scans/decisions requested in the last 60 seconds.
    """
    now = datetime.utcnow()
    one_minute_ago = now - timedelta(minutes=1)
    
    # Count recent interactions
    recent_count = db.query(ScanResult).filter(
        ScanResult.timestamp >= one_minute_ago
    ).count()

    # Determine state limits (Heuristic calibration)
    # > 5/min = Elevated
    # > 10/min = High
    
    triggers = []
    level = 0.1 # Baseline load
    status = "Normal"

    if recent_count > 0:
        level += min(recent_count * 0.1, 0.9) # Cap at 1.0ish
        triggers.append("Active Evaluation")

    if recent_count > 5:
        status = "Elevated"
        triggers.append("High Volume")
    
    if recent_count > 10:
        status = "Maximal"
        triggers.append("Rapid Decisions")

    # Add some mock variation if strictly 0 to show it's "alive" in demo
    # In prod, strictly 0 is fine.
    if recent_count == 0:
        level = 0.05
        status = "Optimal"
        triggers.append("System Idle")

    return {
        "level": round(level, 2),
        "status": status,
        "triggers": triggers[:3], # Max 3 signals
        "density_metric": recent_count
    }

@router.delete("/reset")
async def reset_data(db: Session = Depends(get_db)):
    try:
        db.query(ScanResult).delete()
        db.commit()
        return {"status": "success", "message": "All telemetry data purged."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
