from machine import Pin
import machine, time

def gpio_set(value, mask):
    machine.mem32[0x3FF44004] = (machine.mem32[0x3FF44004] & ~mask) | (value & mask)

PIN_A = 18
PIN_B = 19
PHASE_US = 10  # high/low duration per phase

# init pins (direction)
Pin(PIN_A, Pin.OUT, value=0)
Pin(PIN_B, Pin.OUT, value=0)

MASK = (1 << PIN_A) | (1 << PIN_B)

def hold_us(us):
    deadline = time.ticks_add(time.ticks_us(), us)
    while time.ticks_diff(deadline, time.ticks_us()) > 0:
        pass

while True:
    # Phase 1: A=1, B=0
    gpio_set((1 << PIN_A) | (0 << PIN_B), MASK)
    hold_us(PHASE_US)

    # Phase 2: A=0, B=1
    gpio_set((0 << PIN_A) | (1 << PIN_B), MASK)
    hold_us(PHASE_US)
