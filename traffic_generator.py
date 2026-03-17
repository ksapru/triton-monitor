import time
import requests
import json
import random

# Triton's HTTP endpoint
URL = "http://localhost:8000/v2/models/simple_model/infer"

# Define the payload structure
def get_payload():
    return {
        "inputs": [
            {
                "name": "INPUT0",
                "shape": [3],
                "datatype": "FP32",
                "data": [random.random(), random.random(), random.random()]
            }
        ]
    }

def send_request():
    try:
        response = requests.post(URL, data=json.dumps(get_payload()), timeout=5)
        if response.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] Success: {response.json()['outputs'][0]['data']}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    print("Starting Triton traffic generator for 'simple_model'...")
    try:
        while True:
            send_request()
            # Send roughly 10 requests per second
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping traffic generator.")
