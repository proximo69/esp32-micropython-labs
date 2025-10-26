from machine import Pin
import time

PIN = 18
TARGET_US = 1000
n = 5000

pin = Pin(PIN, Pin.OUT, value=0)

while True:
    start = time.ticks_us()
    pin.value(1)
    
    for _ in range(n):  # variable workload
        pass
    
    # Calculate remaining time
    elapsed = time.ticks_diff(time.ticks_us(), start)
    remaining = TARGET_US - elapsed
    
    # Only wait if we haven't exceeded the target
    if remaining > 0:
        deadline = time.ticks_add(time.ticks_us(), remaining)
        while time.ticks_diff(deadline, time.ticks_us()) > 0:
            pass
    
    pin.value(0)
    time.sleep_ms(1)
