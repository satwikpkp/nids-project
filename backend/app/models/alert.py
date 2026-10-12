import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class NetworkFlow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    protocol: str = "TCP"  # TCP, UDP, ICMP
    service: str = "http"   # http, dns, ssh, ftp, etc.
    flow_duration: float = 0.0
    total_fwd_packets: int = 1
    total_bwd_packets: int = 0
    total_fwd_bytes: int = 64
    total_bwd_bytes: int = 0
    features: Optional[Dict[str, float]] = None

class DetectionAlert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    protocol: str
    attack_type: str = "Normal"  # Normal, DoS, Reconnaissance, Exploits, Fuzzers, Backdoor, Generic, UNKNOWN / ANOMALOUS
    severity: str = "low"        # normal, low, medium, high, critical
    is_anomaly: bool = False
    confidence: float = Field(..., ge=0.0, le=1.0)
    model_predictions: Dict[str, float] = Field(
        default_factory=lambda: {"rf": 0.0, "xgb": 0.0, "cat": 0.0}
    )
    ensemble_weights: Dict[str, float] = Field(
        default_factory=lambda: {"rf": 0.33, "xgb": 0.34, "cat": 0.33}
    )
    inference_time_ms: float = 1.2

class TelemetryStats(BaseModel):
    status: str = "Normal" # Normal, Suspicious, Under Attack
    total_packets_analyzed: int = 0
    malicious_packets_count: int = 0
    benign_packets_count: int = 0
    attack_ratio: float = 0.0
    avg_inference_latency_ms: float = 0.0
    active_threats_count: int = 0
    cpu_usage_pct: float = 0.0
    ram_usage_mb: float = 0.0
    packets_per_sec: int = 0
    attack_distribution: Dict[str, int] = Field(default_factory=dict)
