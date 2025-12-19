This repository contains the lab environment used for the OpenTelemetry blog post: 

**Demystifying OpenTelemetry: Why You Shouldn’t Fear Observability in Traditional Environments (not yet published, still WIP)** 

Here you’ll find a complete, reproducible setup showing how to bring modern observability to traditional environments with OpenTelemetry Collector:

* Legacy production logs (unstructured files)
* IoT sensor data (via MQTT and bridge apps)
* SQL Server performance metrics
* Windows system metrics (via Windows Performance Counters)

Whether you’re a site reliability engineer, developer, or architect, this lab lets you get full-stack visibility - even from systems not designed with observability in mind.

## Features

* File-based log ingestion: Parse and extract metrics from legacy app logs with zero code changes.
* MQTT-to-OpenTelemetry bridge: Forward IoT device telemetry and create meaningful traces and metrics.
* SQL Server monitoring: Collect and export performance metrics from multiple SQL Server instances. 
* Windows host monitoring: Gather CPU and memory stats from Windows machines using native performance counters. (simulated)
* Multi-pipeline OpenTelemetry Collector config: Mix and match data sources, processors, and exporters.
* Prometheus and Jaeger integration: Visualize metrics and traces in popular open-source backends.

## Architecture

![Alt text for the image](fictional-organization-architecture.png)

## Getting Started

**Prerequisties:**

* Docker and Docker Compose
* Prometheus, Jaeger for metrics and traces

**Quick start:**

1. Clone this repository

```console
git clone https://github.com/luke6Lh43/demystifying-otel-lab.git
cd otel-legacy-lab
```

2. Build and start the lab

```console
docker compose up --build
```

3. Access the services

```
Prometheus: http://localhost:9090
Jaeger UI: http://localhost:16686
OpenTelemetry Collector Prometheus endpoint: http://localhost:8889/metrics
```

## Security Notice: Passwords and Sensitive Information

This lab includes example configuration files that use default or hardcoded credentials (for example, oteluser/YourStrong!Passw0rd) for demonstration and local testing purposes only.

**Do not use these passwords in production!**


For real-world deployments:

* Always use strong, unique passwords for all services.
* Store credentials securely using environment variables, Docker secrets, or a dedicated secrets manager.
* Never commit real passwords, access keys, or other secrets to a public repository.
* Consider adding a .gitignore rule for files containing secrets, or use .env.example/.env files to illustrate variable usage without exposing real values.