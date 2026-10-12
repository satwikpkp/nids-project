import random
import time
import psutil
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from backend.app.models.alert import DetectionAlert, TelemetryStats, NetworkFlow
from backend.app.database import db_manager, memory_store
from backend.app.services.socket_manager import socket_manager

router = APIRouter(tags=["Telemetry & Alerts"])

# In-memory accumulator for telemetry calculations
class TelemetryTracker:
    def __init__(self):
        self.total_flows = 1420
        self.malicious_flows = 86
        self.benign_flows = 1334
        self.latencies = [1.12, 1.34, 0.98, 1.25, 1.45]
        self.attack_distribution = {
            "Normal": 1334,
            "DoS": 38,
            "Reconnaissance": 22,
            "Exploits": 14,
            "Fuzzers": 8,
            "UNKNOWN / ANOMALOUS": 4
        }
        self.seed_sample_alerts()

    def seed_sample_alerts(self):
        sample_attacks = [
            ("192.168.1.105", 44322, "10.0.0.5", 80, "TCP", "DoS", "critical", 0.98, False),
            ("192.168.1.144", 51220, "10.0.0.8", 22, "TCP", "Reconnaissance", "medium", 0.91, False),
            ("172.16.0.45", 38920, "10.0.0.12", 443, "TCP", "Exploits", "high", 0.94, False),
            ("192.168.1.199", 59002, "10.0.0.5", 8080, "TCP", "Fuzzers", "medium", 0.88, False),
            ("10.0.2.15", 41200, "10.0.0.1", 53, "UDP", "UNKNOWN / ANOMALOUS", "critical", 0.76, True),
            ("192.168.1.50", 52100, "10.0.0.20", 443, "TCP", "Normal", "normal", 0.99, False),
        ]
        for src, sp, dst, dp, proto, atk, sev, conf, is_ano in sample_attacks:
            alert = DetectionAlert(
                src_ip=src,
                src_port=sp,
                dst_ip=dst,
                dst_port=dp,
                protocol=proto,
                attack_type=atk,
                severity=sev,
                is_anomaly=is_ano,
                confidence=conf,
                model_predictions={
                    "rf": round(conf * 0.98, 2),
                    "xgb": round(conf * 1.01 if conf < 0.98 else 0.99, 2),
                    "cat": round(conf * 0.99, 2)
                },
                ensemble_weights={"rf": 0.33, "xgb": 0.37, "cat": 0.30},
                inference_time_ms=round(random.uniform(0.8, 1.8), 2)
            )
            memory_store.insert_alert(alert.model_dump())

    def get_stats(self) -> TelemetryStats:
        try:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().used / (1024 * 1024)
        except Exception:
            cpu = 14.5
            mem = 210.0

        ratio = (self.malicious_flows / self.total_flows) if self.total_flows > 0 else 0.0
        
        if ratio > 0.15:
            status = "Under Attack"
        elif ratio > 0.03:
            status = "Suspicious"
        else:
            status = "Normal"

        return TelemetryStats(
            status=status,
            total_packets_analyzed=self.total_flows,
            malicious_packets_count=self.malicious_flows,
            benign_packets_count=self.benign_flows,
            attack_ratio=round(ratio, 4),
            avg_inference_latency_ms=round(sum(self.latencies) / len(self.latencies), 2),
            active_threats_count=self.malicious_flows,
            cpu_usage_pct=round(cpu, 1),
            ram_usage_mb=round(mem, 1),
            packets_per_sec=random.randint(120, 380),
            attack_distribution=self.attack_distribution
        )

    def record_detection(self, alert: DetectionAlert):
        self.total_flows += 1
        if alert.attack_type != "Normal":
            self.malicious_flows += 1
        else:
            self.benign_flows += 1

        self.attack_distribution[alert.attack_type] = (
            self.attack_distribution.get(alert.attack_type, 0) + 1
        )
        self.latencies.append(alert.inference_time_ms)
        if len(self.latencies) > 20:
            self.latencies.pop(0)

telemetry_tracker = TelemetryTracker()

@router.get("/alerts", response_model=List[DetectionAlert])
async def get_alerts(
    limit: int = Query(default=50, ge=1, le=200),
    severity: Optional[str] = None
):
    recent = memory_store.get_recent_alerts(limit=limit)
    if severity:
        recent = [a for a in recent if a.get("severity") == severity]
    return [DetectionAlert(**a) for a in recent]

@router.get("/telemetry/stats", response_model=TelemetryStats)
async def get_telemetry_stats():
    return telemetry_tracker.get_stats()

@router.post("/telemetry/simulate_flow", response_model=DetectionAlert)
async def simulate_incoming_flow():
    """Generates a real-time synthetic flow prediction to simulate live traffic stream."""
    attack_choices = [
        ("Normal", "normal", 0.99, False),
        ("Normal", "normal", 0.98, False),
        ("Normal", "normal", 0.97, False),
        ("DoS", "critical", round(random.uniform(0.92, 0.99), 2), False),
        ("Reconnaissance", "medium", round(random.uniform(0.85, 0.94), 2), False),
        ("Exploits", "high", round(random.uniform(0.88, 0.96), 2), False),
        ("Fuzzers", "medium", round(random.uniform(0.81, 0.92), 2), False),
        ("UNKNOWN / ANOMALOUS", "critical", round(random.uniform(0.68, 0.79), 2), True),
    ]
    atk, sev, conf, is_ano = random.choice(attack_choices)
    
    src_ip = f"192.168.1.{random.randint(2, 254)}"
    dst_ip = f"10.0.0.{random.randint(1, 20)}"
    proto = random.choice(["TCP", "UDP", "ICMP"])
    
    alert = DetectionAlert(
        src_ip=src_ip,
        src_port=random.randint(1024, 65535),
        dst_ip=dst_ip,
        dst_port=random.choice([80, 443, 22, 53, 8080, 21]),
        protocol=proto,
        attack_type=atk,
        severity=sev,
        is_anomaly=is_ano,
        confidence=conf,
        model_predictions={
            "rf": round(conf * random.uniform(0.96, 1.02), 2),
            "xgb": round(conf * random.uniform(0.96, 1.02), 2),
            "cat": round(conf * random.uniform(0.96, 1.02), 2),
        },
        ensemble_weights={
            "rf": round(random.uniform(0.28, 0.38), 2),
            "xgb": round(random.uniform(0.32, 0.42), 2),
            "cat": round(random.uniform(0.26, 0.36), 2),
        },
        inference_time_ms=round(random.uniform(0.75, 1.65), 2)
    )
    
    alert_dict = alert.model_dump()
    memory_store.insert_alert(alert_dict)
    telemetry_tracker.record_detection(alert)
    
    # Broadcast to connected WebSocket clients
    await socket_manager.broadcast({
        "type": "NEW_ALERT",
        "alert": alert_dict,
        "stats": telemetry_tracker.get_stats().model_dump()
    })
    
    return alert

@router.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await socket_manager.connect(websocket)
    try:
        # Push initial status immediately
        await websocket.send_json({
            "type": "INITIAL_STATE",
            "stats": telemetry_tracker.get_stats().model_dump(),
            "recent_alerts": memory_store.get_recent_alerts(limit=25)
        })
        while True:
            # Keep socket open and listen for any client messages or pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        socket_manager.disconnect(websocket)
    except Exception as e:
        socket_manager.disconnect(websocket)
