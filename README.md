# Triton Inference Observability & Load Testing Platform

A load testing and monitoring setup for [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server).

## Project Overview

This project provides tools to simulate traffic against a Triton Inference Server and visualize its performance metrics using Grafana and Prometheus.

### Components

- **`models/`**
  A Triton model repository that includes pre-configured models (`simple_model` and `simple_model_gpu`) ready to be served by Triton.
- **`traffic_generator.py`**
  A multi-threaded Python script designed to generate robust synthetic inference traffic. It sends concurrent POST requests with randomized payload data to the `http://localhost:8000/v2/models/simple_model/infer` endpoint, simulating real-world usage.
- **`triton-dashboard.json`**
  A comprehensive Grafana dashboard configuration exported as JSON ("Dashboard for PyTorch Simple Model"). It helps visualize Prometheus metrics scraped from Triton and provides insights on:
  - GPU Utilization
  - GPU Power Usage and Energy Consumption
  - GPU Memory Used
  - Total Inference Count
  - Inference Request Status (Success, Pending, Failure)
- **`traffic.log`**
  Log outputs from the traffic generator executions.

## Usage Guide

1. **Deploy Triton Server**
   Start your Triton Inference Server pointing to the local `models` repository, and ensure the metrics port (default `8002`) is exposed:
   ```bash
   tritonserver --model-repository=/path/to/triton-monitor/models
   ```

2. **Setup Monitoring Infrastructure**
   - Run a Prometheus instance configured to scrape metrics from Triton (`localhost:8002/metrics`).<img width="1440" height="900" alt="Screenshot 2026-03-20 at 1 48 32 PM" src="https://github.com/user-attachments/assets/8c83fbde-5379-470a-818c-1ecfb56b0682" />

   - Import the `triton-dashboard.json` file into your Grafana instance and select your Prometheus data source to start visualizing the metrics.

3. **Generate Synthetic Traffic**
   To simulate load and observe the metrics in action, run the traffic generator script:
   ```bash
   pip install requests
   python traffic_generator.py
   ```
   The script starts 50 concurrent threads to heavily hit the inference server.
