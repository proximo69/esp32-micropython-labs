# RMT_test.py
# Chapter 4 – Lab 4: Advanced RMT (ESP32 + MicroPython)
#
# Demos:
#   A) Fixed pulse pair (100 µs high, 100 µs low), repeated N times
#   B) Bitstream generator (maps bits to pulse widths)
#   C) Looping waveform (hardware repeats a pulse train for a set duration)
#
# Usage:
#   - Set MODE = "fixed" | "bitstream" | "loop"
#   - Adjust PIN, CLOCK_DIV, and other CONFIG_* values as needed
#   - Upload to ESP32 and run:  import RMT_test
#
# Notes:
#   - MicroPython RMT API: esp32.RMT(channel, pin=Pin(X), clock_div=Y)
#   - rmt.write_pulses([durations...], start=<0|1>): durations are in "ticks"
#   - tick = (APB clock at 80 MHz) / clock_div  ⇒ with clock_div=80: 1 tick = 1 µs
#   - Always stop/deinit to free the peripheral (handled in finally)
#
# Safe-stop behavior:
#   - Each demo is time/iteration limited to prevent accidental endless output.
#   - Ctrl+C (KeyboardInterrupt) also stops and deinitializes cleanly.

import esp32
from machine import Pin
import time

# ========== USER SETTINGS ==========
MODE = "fixed"       # "fixed", "bitstream", or "loop"
PIN = 14             # GPIO number for output (use a logic-analyzer or LED+resistor)
CLOCK_DIV = 80       # 80 -> 1 µs resolution (80 MHz / 80 = 1 MHz)

# Demo A (fixed pulses)
CONFIG_FIXED = {
    "high_us": 100,         # high duration in µs
    "low_us": 100,          # low duration in µs
    "repetitions": 20,      # how many times to send the pair
    "gap_ms": 5,            # pause between sends (for clear captures)
    "start_level": 1,       # initial level (1=high first)
}

# Demo B (bitstream)
CONFIG_BITSTREAM = {
    # Map bit 1 / 0 to (high_us, low_us) pairs
    "one":  (600, 600),
    "zero": (300, 300),
    # Example payload to transmit:
    "bits": [1,0,1,1,0,  0,1,0,1,1,  1,0,0,1,0],
    "start_level": 1,
}

# Demo C (looping)
CONFIG_LOOP = {
    # The hardware will loop this pulse train continuously:
    "pulse_train": [250, 250],  # 250 µs high, 250 µs low (≈2 kHz square wave)
    "start_level": 1,
    "duration_s": 3.0,          # run the loop for this many seconds, then stop
}

# ==================================


def _us_to_ticks(us, clock_div):
    """Convert microseconds to RMT ticks for the chosen clock_div."""
    # APB = 80 MHz on ESP32; tick = 1 / (80e6 / clock_div) seconds
    # With clock_div=80: 1 tick = 1 µs (so ticks = us)
    return int(us) if clock_div == 80 else int(round(us * (80 // 1_000_000 * 1_000_000) / (80_000_000 / clock_div)))


def _flatten_pairs(pairs):
    """Flatten [(a,b),(c,d),...] -> [a,b,c,d,...]."""
    out = []
    for a, b in pairs:
        out.append(a)
        out.append(b)
    return out


def demo_fixed(rmt, cfg):
    """A) Send a fixed high/low pair repeatedly."""
    high_ticks = cfg["high_us"]
    low_ticks  = cfg["low_us"]
    # With CLOCK_DIV=80, ticks == microseconds, so we can pass µs directly.
    # If you change CLOCK_DIV, convert with _us_to_ticks.
    durations = [high_ticks, low_ticks]

    print("[Fixed] Sending {}× {}us high, {}us low".format(
        cfg["repetitions"], cfg["high_us"], cfg["low_us"]
    ))
    for i in range(cfg["repetitions"]):
        rmt.write_pulses(durations, start=cfg["start_level"])
        rmt.wait_done()
        time.sleep_ms(cfg["gap_ms"])
    print("[Fixed] Done.")


def demo_bitstream(rmt, cfg):
    """B) Build a bitstream where 1/0 map to different pulse widths."""
    one_pair  = cfg["one"]   # (high_us, low_us)
    zero_pair = cfg["zero"]

    pairs = []
    for b in cfg["bits"]:
        pairs.append(one_pair if b else zero_pair)

    durations = _flatten_pairs(pairs)
    print("[Bitstream] Bits ({}): {}".format(len(cfg["bits"]), cfg["bits"]))
    print("[Bitstream] ONE={}us, ZERO={}us".format(one_pair, zero_pair))

    rmt.write_pulses(durations, start=cfg["start_level"])
    rmt.wait_done()
    print("[Bitstream] Done.")


def demo_loop(rmt, cfg):
    """C) Loop a pulse train in hardware for a set duration, then stop."""
    pulse_train = cfg["pulse_train"]
    print("[Loop] Enabling hardware loop for {} s. Pulse train: {}".format(cfg["duration_s"], pulse_train))

    rmt.loop(True)  # enable hardware looping for the next write
    rmt.write_pulses(pulse_train, start=cfg["start_level"])

    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < int(cfg["duration_s"] * 1000):
        time.sleep_ms(50)

    # Stop looping
    rmt.loop(False)
    # After disabling loop, the last write keeps going until we send a short stop pulse or re-write.
    # A common trick is to send a 0-length pulse to terminate; on some ports, a minimal pulse works.
    # We use a tiny pair to force a clean stop:
    rmt.write_pulses([1, 1], start=0)
    rmt.wait_done()
    print("[Loop] Stopped.")


def main():
    # Initialize RMT with chosen resolution
    # With CLOCK_DIV=80, 1 tick = 1 µs (preferred for human-friendly math).
    rmt = esp32.RMT(0, pin=Pin(PIN), clock_div=CLOCK_DIV)
    print("RMT initialized on GPIO{}, clock_div={} (≈ {} µs/tick)".format(
        PIN, CLOCK_DIV, 1 if CLOCK_DIV == 80 else round(CLOCK_DIV / 80.0, 3)
    ))

    try:
        if MODE == "fixed":
            demo_fixed(rmt, CONFIG_FIXED)
        elif MODE == "bitstream":
            demo_bitstream(rmt, CONFIG_BITSTREAM)
        elif MODE == "loop":
            demo_loop(rmt, CONFIG_LOOP)
        else:
            print("Unknown MODE:", MODE)
    except KeyboardInterrupt:
        print("\n[User] Interrupted with Ctrl+C.")
    finally:
        # Always release the peripheral
        try:
            rmt.deinit()
            print("RMT deinitialized.")
        except Exception as e:
            print("RMT deinit error:", e)


# Auto-run when imported as a module on the board.
main()
