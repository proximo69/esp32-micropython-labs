from machine import Pin
import time

a = Pin(18, Pin.OUT, value=0)
b = Pin(19, Pin.OUT, value=1)

while True:
    a.value(1); b.value(0)
    time.sleep_us(10)
    a.value(0); b.value(1)
    time.sleep_us(10)
