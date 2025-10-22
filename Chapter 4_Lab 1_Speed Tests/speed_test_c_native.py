import time
from machine import Pin
import micropython  # needed for the decorator
@micropython.native
def flash():
    p = Pin(2, Pin.OUT)
    t_end = time.ticks_add(time.ticks_ms(), 2000)  # run ~2 seconds
    while time.ticks_diff(t_end, time.ticks_ms()) > 0:
        p.value(1)
        p.value(0)
flash()
