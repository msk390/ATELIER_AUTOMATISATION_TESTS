import statistics
from .tests import ALL_TESTS

def run_all():
    results = []
    for test_fn in ALL_TESTS:
        try:
            result = test_fn()
        except Exception as e:
            result = {"name": test_fn.__name__, "status": "FAIL", "latency_ms": 0, "details": str(e)}
        results.append(result)

    latencies = [r["latency_ms"] for r in results if r["latency_ms"] > 0]
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = len(results) - passed

    summary = {
        "passed": passed,
        "failed": failed,
        "total": len(results),
        "error_rate": round(failed / len(results), 3) if results else 0,
        "latency_ms_avg": int(statistics.mean(latencies)) if latencies else 0,
        "latency_ms_p95": int(sorted(latencies)[int(len(latencies) * 0.95)]) if len(latencies) >= 2 else (latencies[0] if latencies else 0),
    }

    return summary, results
