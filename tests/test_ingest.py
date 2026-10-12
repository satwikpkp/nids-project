from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_pipeline_info():
    response = client.get("/api/v1/ingest/pipeline_info")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert data["feature_selection_target"] == 15
    assert len(data["selected_features"]) == 15
    assert "AdaptiveEnsemble" in data["ensemble_type"]
    assert "ZeroDayAnomalyDetector" in data["anomaly_detector"]

def test_live_flow_inference():
    flow_payload = {
        "src_ip": "192.168.1.105",
        "src_port": 50123,
        "dst_ip": "10.0.0.1",
        "dst_port": 80,
        "protocol": "TCP",
        "service": "http",
        "flow_duration": 1.25,
        "total_fwd_packets": 20,
        "total_bwd_packets": 15,
        "total_fwd_bytes": 1400,
        "total_bwd_bytes": 850,
        "features": {
            "dur": 1.25,
            "rate": 28.0,
            "sload": 9500.0,
            "dload": 6200.0,
            "sttl": 64,
            "dttl": 64
        }
    }
    response = client.post("/api/v1/ingest/flow", json=flow_payload)
    assert response.status_code == 200
    alert = response.json()
    assert alert["src_ip"] == "192.168.1.105"
    assert alert["dst_ip"] == "10.0.0.1"
    assert "attack_type" in alert
    assert "confidence" in alert
    assert "model_predictions" in alert
    assert "ensemble_weights" in alert
    assert "rf" in alert["ensemble_weights"]
    assert "xgb" in alert["ensemble_weights"]
    assert "cat" in alert["ensemble_weights"]
    assert alert["inference_time_ms"] > 0
