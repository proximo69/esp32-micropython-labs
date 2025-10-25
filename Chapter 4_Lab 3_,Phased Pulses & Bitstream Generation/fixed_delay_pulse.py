from machine import Pin
import time

PIN = 18  # pick a safe GPIO for your board
TARGET_US = 1000  # 1 ms target pulse width
n = 5000          # simulate variable work; adjust freely

pin = Pin(PIN, Pin.OUT, value=0)

while True:
    deadline = time.ticks_add(time.ticks_us(), TARGET_US)
    pin.value(1)
    for _ in range(n):  # variable workload
        pass
    # wait for remainder so total high time ~ TARGET_US
    while time.ticks_diff(deadline, time.ticks_us()) > 0:
        pass
    pin.value(0)
    time.sleep_ms(1)  # spacing between pulses for visibility
