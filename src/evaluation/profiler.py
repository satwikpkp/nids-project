import time
import psutil
import numpy as np
from typing import Dict, Any

class ResourceProfiler:
    """Measures CPU usage, RAM consumption, model size, inference latency, and throughput."""
    def __init__(self):
        pass

    @staticmethod
    def profile_inference(model, X: np.ndarray, num_runs: int = 100) -> Dict[str, Any]:
        """Runs repeated benchmark inferences to calculate latency and resource overhead."""
        # Warmup
        _ = model.predict(X[:min(5, len(X))])
        
        # Measure latency
        start_time = time.perf_counter()
        for _ in range(num_runs):
            _ = model.predict(X)
        end_time = time.perf_counter()

        total_elapsed = end_time - start_time
        total_samples = len(X) * num_runs
        avg_latency_ms = (total_elapsed / total_samples) * 1000.0
        pps = int(total_samples / total_elapsed) if total_elapsed > 0 else 0

        # Memory & CPU
        process = psutil.Process()
        ram_mb = process.memory_info().rss / (1024 * 1024)
        cpu_pct = psutil.cpu_percent(interval=None)

        return {
            "avg_latency_per_sample_ms": round(avg_latency_ms, 3),
            "packets_per_sec": pps,
            "total_benchmark_time_sec": round(total_elapsed, 3),
            "process_ram_mb": round(ram_mb, 2),
            "system_cpu_pct": round(cpu_pct, 1)
        }
