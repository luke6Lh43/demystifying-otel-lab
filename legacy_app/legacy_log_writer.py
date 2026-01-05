import time, random

LOG_FILE = "/logs/legacy.log"

LINES = ["Line1", "Line2"]
FAULTS = ["Overheat", "Jam", "LowPressure"]

def machine_start(line): return f"MACHINE_START: {line}"
def product_completed(line): return f"PRODUCT_COMPLETED: {line}, Count=1"
def sensor_reading(line):
    temp = round(random.uniform(70.0, 95.0), 1)
    return f"SENSOR_READING: {line}, Temp={temp}"
def operator_intervention(line):
    operator_id = random.choice(["007", "011", "042"])
    return f"OPERATOR_INTERVENTION: {line}, OperatorID={operator_id}"
def fault_detected(line):
    fault = random.choice(FAULTS)
    return f"FAULT_DETECTED: {line}, Fault={fault}"

EVENT_GENERATORS = [
    machine_start,
    product_completed,
    sensor_reading,
    operator_intervention,
    fault_detected,
]

while True:
    line = random.choice(LINES)
    event = random.choice(EVENT_GENERATORS)(line)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} | {event}\n")

    time.sleep(random.randint(1, 5))