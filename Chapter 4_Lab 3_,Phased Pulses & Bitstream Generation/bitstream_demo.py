import esp32
from machine import Pin
import machine

PIN = 21
pin = Pin(PIN, Pin.OUT, value=0)

# Configure RMT hardware channel 0 for precise timing
# (Use None for software fallback if RMT channels exhausted)
esp32.RMT.bitstream_channel(0)

# Timing format: (0_high_ns, 0_low_ns, 1_high_ns, 1_low_ns)
# 0-bit: 1µs high + 1µs low (2µs total)
# 1-bit: 2µs high + 1µs low (3µs total)
timing = (1000, 1000, 2000, 1000)

# Test data (sent LSB first):
# 0x55 = 0b01010101 → alternating 0,1,0,1,0,1,0,1
# 0xF0 = 0b11110000 → 0,0,0,0,1,1,1,1
buf = bytearray(b"\x55\xF0")

print(f"Sending {len(buf)} bytes on GPIO {PIN}...")
print("Expected: alternating pattern, then four short + four long pulses")
print("Note: ~400µs gaps between bytes due to Python overhead")

machine.bitstream(pin, 0, timing, buf)
print("Done!")
