from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_telemetry_stats():
    response = client.get("/api/v1/telemetry/stats")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "total_packets_analyzed" in data
    assert "attack_distribution" in data

def test_alerts_endpoint():
    response = client.get("/api/v1/alerts?limit=10")
    assert response.status_code == 200
    alerts = response.json()
    assert isinstance(alerts, list)
    assert len(alerts) > 0
    assert "attack_type" in alerts[0]
    assert "confidence" in alerts[0]

def test_simulate_flow():
    response = client.post("/api/v1/telemetry/simulate_flow")
    assert response.status_code == 200
    new_alert = response.json()
    assert "src_ip" in new_alert
    assert "dst_ip" in new_alert
    assert "confidence" in new_alert
    assert "inference_time_ms" in new_alert
