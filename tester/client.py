import requests
import time

DEFAULT_TIMEOUT = 5

def get(url, timeout=DEFAULT_TIMEOUT, retries=1):
    last_error = None
    for attempt in range(retries + 1):
        try:
            start = time.time()
            response = requests.get(url, timeout=timeout)
            latency_ms = int((time.time() - start) * 1000)
            return response, latency_ms
        except requests.exceptions.Timeout:
            last_error = "timeout"
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            time.sleep(1)
    return None, last_error
