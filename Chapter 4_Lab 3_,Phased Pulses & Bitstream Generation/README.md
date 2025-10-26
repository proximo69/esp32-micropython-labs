# Chapter 4 — Lab 3: Phased Pulses & Bitstream Generation

**Goal:** Produce precisely timed pulses under variable workload, generate out-of-phase dual outputs with atomic edges, and emit a simple bitstream using ESP32 RMT.

## Key Concepts
- Fixed-time pulses using `ticks_us()` + `ticks_add()`/`ticks_diff()`
- Atomic multi-GPIO updates via `gpio_set(value, mask)` to remove skew
- `machine.bitstream(...)` (RMT-backed) for fast, accurate bit cells

## Files
- `fixed_delay_pulse.py` — 1 ms pulses with variable “work”, constant width
- `phased_pulses_atomic.py` — true A/B out-of-phase pulses (simultaneous edges)
- `bitstream_demo.py` — encode bytes into timed cells via RMT

## What to Measure
- Fixed delay: HIGH width ≈ target independent of loop workload
- Phased: edge alignment (naïve vs atomic)

### Exercise 1: Naive Phased Pulses
Run `phased_pulses_naive.py` and capture both GPIO 18 and 19 on your oscilloscope.

**What to observe:**
- Use oscilloscope **persistence mode**
- Trigger on Channel A rising edge
- Zoom in on the falling edge of Channel B
- You should see ~100-500 ns delay between the two transitions

### Exercise 2: Atomic Phased Pulses  
Run `phased_pulses_atomic.py` with the same oscilloscope settings.

**What to observe:**
- Both edges now align perfectly (<50 ns skew)
- Persistence mode shows a single sharp line instead of "thickness"
- This is the difference atomic GPIO operations make!

## Bitstream Measurements

**Timing verification:**
1. Measure 0-bit cell width: should be ~2 µs (1µs high + 1µs low)
2. Measure 1-bit cell width: should be ~3 µs (2µs high + 1µs low)
3. Observe ~400 µs gaps between the two bytes

**Pattern verification:**
- First byte (0x55): Alternating short/long pulses
- Second byte (0xF0): Four short pulses, then four long pulses
- Remember: LSB is transmitted first!

**Try modifying:**
- Change `buf` to `b"\xFF\x00"` to see all-long then all-short
- Change `buf` to `b"\xAA"` (0b10101010) to invert the pattern
- Increase timing values to slow down for easier observation


## Notes
- Choose safe GPIOs for your board (e.g., 18, 19, 21). Avoid strapping pins.
- For arbitrary start/stop bit shapes, consider `esp32.RMT(...).write_pulses(...)` next lab.

