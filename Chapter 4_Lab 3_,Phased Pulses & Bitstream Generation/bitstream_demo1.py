import esp32
from machine import Pin
import machine
import time

PIN = 21
pin = Pin(PIN, Pin.OUT, value=0)

# Configure RMT hardware channel 0 for precise timing
esp32.RMT.bitstream_channel(0)

# Timing format: (0_high_ns, 0_low_ns, 1_high_ns, 1_low_ns)
# 0-bit: 1 µs high + 1 µs low (2 µs total)
# 1-bit: 2 µs high + 1 µs low (3 µs total)
timing = (1000, 1000, 2000, 1000)

# Test data (sent LSB first)
# 0x55 = 01010101  → alternating 0,1,0,1,...
# 0xF0 = 11110000  → four 0s then four 1s
buf = bytearray(b"\x55\xF0")

print(f"Sending continuous bursts on GPIO {PIN}...")
print("Arming logic analyzer...  (2-second delay)")
time.sleep(2)

while True:
    machine.bitstream(pin, 0, timing, buf)
    # short idle gap so the analyzer can show separation between bursts
    time.sleep_ms(10)
