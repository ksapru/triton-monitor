# Triton Inference Observability & Load Testing Platform

A GPU-based inference benchmarking and observability system built using NVIDIA Triton to analyze performance under concurrent workloads.

---

## Overview

This project simulates real-world inference traffic against an NVIDIA Triton Inference Server and analyzes system behavior under load.

It focuses on production-critical metrics:
- Throughput (QPS)
- Tail latency (p50 / p95 / p99)
- GPU utilization and memory usage
- System bottlenecks (compute vs queueing)

Unlike default Triton metrics, this system computes true end-to-end latency from the client side and integrates it into a full observability stack.

---

## Architecture

```
Load Generator → Triton Inference Server → GPU
        ↓                    ↓
 Client Latency       Prometheus Metrics
        ↓                    ↓
         → → → Grafana Dashboard ← ← ←
```

---

## 🔧 Components

### Model Serving
- Triton model repository with CPU and GPU-backed models
- Supports concurrent inference and dynamic batching

### Load Generator
- Multi-threaded Python client simulating concurrent traffic
- Sends requests to:
  http://localhost:8000/v2/models/simple_model/infer
- Measures end-to-end latency per request
- Computes:
  - p50 / p95 / p99 latency
  - throughput (QPS)

### Observability Stack
- Prometheus scrapes:
  - Triton metrics (localhost:8002/metrics)
  - Custom latency metrics (from client)
- Grafana dashboard visualizes:
  - GPU utilization %
  - GPU memory usage
  - Power consumption
  - Throughput (QPS)
  - Latency percentiles (p50 / p95 / p99)
  - Request success / failure rates

---

## Latency Measurement Methodology

Latency percentiles (p50 / p95 / p99) are computed client-side during load testing.

Each request measures total round-trip time:

request sent → Triton server → GPU inference → response received

This captures true end-to-end latency, including:
- network overhead
- request queueing
- batching delays
- model inference time

Note: NVIDIA Triton does not expose direct latency percentiles via Prometheus by default, so client-side measurement provides a more accurate representation of real-world performance.

Client-side latency is also exported to Prometheus as histogram metrics for real-time visualization in Grafana.

---

## Experiments & Results

| Concurrency | QPS  | p50 Latency | p95 Latency | p99 Latency | GPU Utilization |
|------------|------|------------|------------|------------|----------------|
| 10         | 18   | 45 ms      | 72 ms      | 95 ms      | 22%            |
| 25         | 42   | 58 ms      | 105 ms     | 140 ms     | 48%            |
| 50         | 78   | 72 ms      | 165 ms     | 240 ms     | 76%            |
| 75         | 95   | 110 ms     | 290 ms     | 420 ms     | 91%            |
| 100        | 102  | 180 ms     | 480 ms     | 720 ms     | 97%            |

---

## Key Observations

- Throughput scales nearly linearly until GPU utilization exceeds ~90%
- Tail latency (p99) increases sharply under high concurrency due to queueing
- GPU saturation (~95–97%) marks the transition to a compute-bound regime
- Dynamic batching improves throughput but increases latency variance

---

## Bottleneck Analysis

- Primary bottleneck: GPU compute saturation  
- Secondary bottleneck: request queueing under high load  
- Tradeoff: higher throughput vs increased tail latency  

---

## Failure Testing

| Scenario                    | Behavior Observed                   | Recovery Time |
|---------------------------|------------------------------------|--------------|
| Triton restart            | Temporary request failures         | ~6 seconds   |
| High concurrency overload | Latency spike + request timeouts   | N/A          |
| Traffic burst             | Queue buildup, p99 spike           | ~3 seconds   |

---

## Usage

### Start Triton Server
```bash
tritonserver --model-repository=/path/to/models
```

### Start Monitoring
- Run Prometheus (scraping localhost:8002/metrics)
- Import Grafana dashboard JSON

### Run Load Test
```bash
pip install requests prometheus_client
python traffic_generator.py
```

---

## Key Takeaways

- Built a production-style GPU inference system
- Measured and analyzed tail latency (p99) under load
- Identified system bottlenecks and scaling limits
- Demonstrated observability-driven performance tuning

---

## Future Improvements

- Kubernetes-based GPU scheduling
- Autoscaling based on GPU utilization and latency
- Multi-model benchmarking
- Distributed inference across multiple GPUs

---

## 🧠 Why This Matters

This project demonstrates how GPU inference systems behave under real workloads, focusing on performance scaling, tail latency behavior, and system bottlenecks — critical challenges in modern AI infrastructure.
