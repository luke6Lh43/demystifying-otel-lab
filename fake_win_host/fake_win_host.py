import os
import time
import random
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Use environment variables or hardcode for unique hosts
HOSTNAME = os.environ.get("FAKE_WIN_HOST", "WIN-AGENT-01")
MACHINE_ID = os.environ.get("FAKE_MACHINE_ID", "1234-5678-ABCD")
SERVICE_NAME = os.environ.get("OTEL_SERVICE_NAME", "otelcol-win-agent")

# Resource attributes to mimic a real Windows machine/agent
resource = Resource.create({
    "service.name": SERVICE_NAME,
    "host.name": HOSTNAME,
    "os.type": "windows",
    "os.description": "Microsoft Windows Server 2022 Datacenter",
    "os.version": "10.0.20348",
    "machine.id": MACHINE_ID,
    "telemetry.sdk.language": "python"
})

exporter = OTLPMetricExporter(endpoint="collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("otelcol-win-agent")

# Realistic Windows perf counter metric names
def cpu_callback(options):
    return [
        metrics.Observation(random.uniform(0, 100), {"state": "user", "cpu": "0"}),
        metrics.Observation(random.uniform(0, 100), {"state": "system", "cpu": "0"}),
        metrics.Observation(random.uniform(0, 100), {"state": "idle", "cpu": "0"}),
        metrics.Observation(random.uniform(0, 100), {"state": "user", "cpu": "1"}),
        metrics.Observation(random.uniform(0, 100), {"state": "system", "cpu": "1"}),
        metrics.Observation(random.uniform(0, 100), {"state": "idle", "cpu": "1"}),
    ]

def mem_callback(options):
    return [
        metrics.Observation(random.uniform(1e9, 3e9), {"state": "used"}),
        metrics.Observation(random.uniform(1e9, 2e9), {"state": "free"}),
    ]

def proc_callback(options):
    return [
        metrics.Observation(random.randint(80, 180), {"process": "sqlservr.exe"}),
        metrics.Observation(random.randint(10, 40), {"process": "svchost.exe"}),
        metrics.Observation(random.randint(5, 20), {"process": "explorer.exe"}),
    ]

meter.create_observable_gauge(
    name="windows.cpu.time",
    callbacks=[cpu_callback],
    unit="s",
    description="Processor time"
)

meter.create_observable_gauge(
    name="windows.memory.usage",
    callbacks=[mem_callback],
    unit="bytes",
    description="Physical memory usage"
)

meter.create_observable_gauge(
    name="windows.process.count",
    callbacks=[proc_callback],
    unit="1",
    description="Process count"
)

print(f"Windows agent {HOSTNAME} sending metrics to collector. Press Ctrl+C to exit.", flush=True)
while True:
    time.sleep(10)