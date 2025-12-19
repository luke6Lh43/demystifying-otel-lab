import os
import sys
import json
import time
from datetime import datetime, timezone
from paho.mqtt.client import Client, CallbackAPIVersion

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# --- Force unbuffered output for Docker logs ---
sys.stdout.reconfigure(line_buffering=True)
print("🚀 Starting MQTT Bridge", flush=True)

# --- OTEL Resource definition ---
resource = Resource.create({
    "service.name": "mqtt-bridge",
    "service.version": "1.0"
})

# --- Tracing Setup ---
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)
trace_exporter = OTLPSpanExporter(
    endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://collector:4317"),
    insecure=True
)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
print("✅ Tracing OK", flush=True)

def iso8601_to_ns(isotime: str) -> int:
    """Convert ISO8601 (ms precision) to nanoseconds."""
    if isotime.endswith('Z'):
        isotime = isotime[:-1]
    
    if '.' in isotime:
        parts = isotime.rsplit('.', 1)
        if len(parts[1]) == 3:  # Pad milliseconds to microseconds
            isotime = f"{parts[0]}.{parts[1]}000"
        elif len(parts[1]) > 6:
            parts[1] = parts[1][:6]
            isotime = f"{parts[0]}.{parts[1]}"
    
    dt = datetime.strptime(isotime, '%Y-%m-%dT%H:%M:%S.%f')
    dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1_000_000_000)

# --- MQTT Event Handlers ---
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✅ MQTT CONNECTED (RC: {rc})", flush=True)
    client.subscribe("env/sensors")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        print(f"📨 MQTT: {msg.topic}", flush=True)

        start_ns = iso8601_to_ns(payload["job_start"])
        end_ns = iso8601_to_ns(payload["job_end"])
        
        span = tracer.start_span("mqtt.message.received", start_time=start_ns)
        try:
            span.set_attribute("mqtt.topic", msg.topic)
            span.set_attribute("span.duration_s", round((end_ns - start_ns) / 1_000_000_000, 3))
            for k, v in payload.items():
                span.set_attribute(f"payload.{k}", v)
        finally:
            span.end(end_time=end_ns)
            
    except Exception as e:
        print(f"❌ ERROR: {e}", flush=True)

# --- MQTT Client Setup ---
client = Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id="mqtt-bridge-otel")
client.on_connect = on_connect
client.on_message = on_message

broker = os.environ.get("MQTT_BROKER", "mqtt-broker")

# --- Robust MQTT Connection Loop ---
while True:
    try:
        print(f"🔌 Connecting to {broker}:1883...", flush=True)
        client.connect(broker, 1883, 60)
        print(f"✅ Connected to {broker}:1883", flush=True)
        break
    except Exception as e:
        print(f"❌ MQTT connection failed: {e}", flush=True)
        time.sleep(5)

client.loop_forever()
