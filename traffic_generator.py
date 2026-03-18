import time
import requests
import random
from concurrent.futures import ThreadPoolExecutor

# Triton's HTTP endpoint
URL = "http://localhost:8000/v2/models/simple_model/infer"

def send_request(_):
    payload = {
        "inputs": [
            {
                "name": "INPUT0",
                "shape": [3],
                "datatype": "FP32",
                "data": [random.random(), random.random(), random.random()]
            }
        ]
    }
    try:
        requests.post(URL, json=payload, timeout=10)
    except Exception:
        pass

if __name__ == "__main__":
    print("Starting 50-threaded Triton traffic generator...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        while True:
            executor.map(send_request, range(50))
