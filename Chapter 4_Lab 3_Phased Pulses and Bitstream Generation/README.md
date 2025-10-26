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
- Bitstream: 0/1 cell timing matches tuple; note ~400 µs gaps between calls

## Notes
- Choose safe GPIOs for your board (e.g., 18, 19, 21). Avoid strapping pins.
- For arbitrary start/stop bit shapes, consider `esp32.RMT(...).write_pulses(...)` next lab.
