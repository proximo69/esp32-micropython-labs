from machine import Pin
p = Pin(2, Pin.OUT)
while True:
    p.value(1)
    p.value(0)
