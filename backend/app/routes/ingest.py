import uuid
from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status
from backend.app.models.alert import NetworkFlow, DetectionAlert
from backend.app.services.inference import inference_service
from backend.app.services.socket_manager import socket_manager
from backend.app.routes.telemetry import telemetry_tracker
from backend.app.database import db_manager, memory_store

router = APIRouter(prefix="/ingest", tags=["Flow Ingestion & Live Inference"])

@router.post("/flow", response_model=DetectionAlert)
async def ingest_network_flow(flow: NetworkFlow):
    """
    Ingests live network flow, runs it through the full ML pipeline:
    Data Cleaner -> Feature Encoder -> Feature Selector (15 features) ->
    Base Models (RF + XGB + CatBoost) -> Adaptive Ensemble -> Zero-Day Anomaly Hook.
    """
    try:
        # 1. Run live ML inference
        result = inference_service.predict_flow(flow.model_dump())
        
        # 2. Construct persistent DetectionAlert
        alert = DetectionAlert(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            src_ip=flow.src_ip,
            src_port=flow.src_port,
            dst_ip=flow.dst_ip,
            dst_port=flow.dst_port,
            protocol=flow.protocol,
            attack_type=result["attack_type"],
            severity=result["severity"],
            is_anomaly=result["is_anomaly"],
            confidence=result["confidence"],
            model_predictions=result["model_predictions"],
            ensemble_weights=result["ensemble_weights"],
            inference_time_ms=result["inference_time_ms"]
        )
        
        # 3. Store alert
        alert_dict = alert.model_dump()
        memory_store.insert_alert(alert_dict)
        telemetry_tracker.record_detection(alert)
        
        # 4. Broadcast live detection via WebSocket to connected React clients
        await socket_manager.broadcast({
            "type": "NEW_ALERT",
            "alert": alert_dict,
            "stats": telemetry_tracker.get_stats().model_dump()
        })
        
        return alert
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(e)}"
        )

@router.get("/pipeline_info")
async def get_pipeline_info():
    """Returns active ML pipeline configuration, feature count, and model architectures."""
    return {
        "status": "active",
        "feature_selection_target": inference_service.target_features,
        "selected_features": inference_service.selector.selected_feature_names,
        "base_models": ["RandomForestClassifier", "XGBClassifier", "CatBoostClassifier"],
        "ensemble_type": "AdaptiveEnsemble (Dynamic Entropy & Margin Weighting)",
        "anomaly_detector": "ZeroDayAnomalyDetector (Entropy & Out-of-Distribution Bounds)"
    }
