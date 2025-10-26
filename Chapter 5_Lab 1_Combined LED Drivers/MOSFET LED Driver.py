from machine import Pin
import time

class MosfetDriver:
    def __init__(self, pin=17, active_high=True):
        self.active_high = active_high
        self.out = Pin(pin, Pin.OUT, value=0 if active_high else 1)
        self.off()

    def on(self):
        self.out.value(1 if self.active_high else 0)

    def off(self):
        self.out.value(0 if self.active_high else 1)

    def pulse_ms(self, on_ms=100, off_ms=0):
        self.on()
        time.sleep_ms(on_ms)
        self.off()
        if off_ms:
            time.sleep_ms(off_ms)
