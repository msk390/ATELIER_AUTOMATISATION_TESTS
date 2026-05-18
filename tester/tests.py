from .client import get

BASE_URL = "https://api.frankfurter.app"

def test_status_200():
    resp, latency = get(f"{BASE_URL}/latest?from=EUR")
    if resp is None:
        return {"name": "status_200", "status": "FAIL", "latency_ms": 0, "details": "pas de réponse"}
    ok = resp.status_code == 200
    return {"name": "status_200", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": f"code reçu: {resp.status_code}"}

def test_content_type_json():
    resp, latency = get(f"{BASE_URL}/latest?from=EUR")
    if resp is None:
        return {"name": "content_type_json", "status": "FAIL", "latency_ms": 0, "details": "pas de réponse"}
    ct = resp.headers.get("Content-Type", "")
    ok = "application/json" in ct
    return {"name": "content_type_json", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": ct}

def test_schema_fields():
    resp, latency = get(f"{BASE_URL}/latest?from=EUR")
    if resp is None:
        return {"name": "schema_fields", "status": "FAIL", "latency_ms": 0, "details": "pas de réponse"}
    data = resp.json()
    required = ["amount", "base", "date", "rates"]
    missing = [f for f in required if f not in data]
    ok = len(missing) == 0
    return {"name": "schema_fields", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": f"champs manquants: {missing}" if missing else "tous les champs présents"}

def test_rates_not_empty():
    resp, latency = get(f"{BASE_URL}/latest?from=EUR")
    if resp is None:
        return {"name": "rates_not_empty", "status": "FAIL", "latency_ms": 0, "details": "pas de réponse"}
    rates = resp.json().get("rates", {})
    ok = isinstance(rates, dict) and len(rates) > 0
    return {"name": "rates_not_empty", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": f"{len(rates)} devises trouvées"}

def test_base_is_eur():
    resp, latency = get(f"{BASE_URL}/latest?from=EUR")
    if resp is None:
        return {"name": "base_is_eur", "status": "FAIL", "latency_ms": 0, "details": "pas de réponse"}
    base = resp.json().get("base")
    ok = base == "EUR"
    return {"name": "base_is_eur", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": f"base={base}"}

def test_invalid_endpoint_returns_error():
    resp, latency = get(f"{BASE_URL}/endpoint_invalide_xyz")
    if resp is None:
        return {"name": "invalid_404", "status": "FAIL", "latency_ms": 0, "details": "pas de réponse"}
    ok = resp.status_code in [400, 404, 422]
    return {"name": "invalid_404", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": f"code reçu: {resp.status_code}"}

def test_latency_under_3s():
    resp, latency = get(f"{BASE_URL}/latest?from=EUR", timeout=3)
    if resp is None:
        return {"name": "latency_under_3s", "status": "FAIL", "latency_ms": 0, "details": "timeout"}
    ok = latency < 3000
    return {"name": "latency_under_3s", "status": "PASS" if ok else "FAIL",
            "latency_ms": latency, "details": f"{latency}ms"}

ALL_TESTS = [
    test_status_200,
    test_content_type_json,
    test_schema_fields,
    test_rates_not_empty,
    test_base_is_eur,
    test_invalid_endpoint_returns_error,
    test_latency_under_3s,
]
