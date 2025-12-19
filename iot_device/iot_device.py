import os
import json
import time
import random
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

broker = os.environ.get("MQTT_BROKER", "mqtt-broker")
device_id = os.environ.get("DEVICE_ID", "sensor-1")

client = mqtt.Client()
client.connect(broker, 1883, 60)

def iso_now():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

while True:
    job_start = iso_now()
    duration = random.uniform(0.1, 4.5)
    time.sleep(duration)
    job_end = iso_now()

    temperature = round(random.uniform(20, 30), 2)
    humidity = round(random.uniform(30, 70), 2)
    payload = {
        "device_id": device_id,
        "temperature": temperature,
        "humidity": humidity,
        "job_start": job_start,
        "job_end": job_end,
        "job_duration_s": round(duration, 3)
    }
    client.publish("env/sensors", json.dumps(payload))
    print(f"Published: {payload}")
    time.sleep(5)