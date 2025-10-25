import esp32
from machine import Pin
import machine

PIN = 21
pin = Pin(PIN, Pin.OUT, value=0)

# Optional: choose RMT channel (0..7). Use None for software fallback.
esp32.RMT.bitstream_channel(0)

# Timings are in nanoseconds (ns).
# Example: encode 0 as 300ns high + 300ns low, 1 as 600ns high + 300ns low.
timing = (300, 300, 600, 300)

# Data: 0b01010101, 0b11110000 (alternate then runs)
buf = bytearray(b"\x55\xF0")

machine.bitstream(pin, 0, timing, buf)
