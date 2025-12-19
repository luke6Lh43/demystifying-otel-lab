import time, random

LOG_FILE = "/logs/legacy.log"
EVENTS = [
    "MACHINE_START: Line1",
    "PRODUCT_COMPLETED: Line1, Count=1",
    "FAULT_DETECTED: Line1, Fault=Overheat",
    "OPERATOR_INTERVENTION: Line1, OperatorID=007",
    "SENSOR_READING: Line1, Temp=78.4"
]

while True:
    with open(LOG_FILE, "a") as f:
        event = random.choice(EVENTS)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | {event}\n")
    time.sleep(random.randint(1, 5))