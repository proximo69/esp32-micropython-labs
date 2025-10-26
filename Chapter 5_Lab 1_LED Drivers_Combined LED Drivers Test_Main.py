# Chapter 5 – Lab 1: Combined LED Driver Test (one-shot with arming delay)
# - Arming delay to get PulseView ready
# - Fixed-duration run; drift-free scheduling
# - Clean exit with outputs off (even on Ctrl-C)

from bjt_driver import BjtDriver
from mosfet_driver import MosfetDriver
import time

bjt = None
mos = None

# ===== User Config =====
START_DELAY_S   = 10    # Arming delay
RUN_TIME_S      = 10    # One-shot window
PERIOD_MS       = 200   # Period of the test pattern
ON_MS_BJT       = 50    # BJT ON time
ON_MS_MOSFET    = 50    # MOSFET ON time
GAP_MS          = 10    # Gap between BJT and MOSFET pulses
BJT_PIN         = 16    # Use non-boot-strap pins
MOSFET_PIN      = 17
# =======================

USE_BJT    = True
USE_MOSFET = True

def countdown(seconds):
    for s in range(seconds, 0, -1):
        print("Arming... starting in", s, "s")
        time.sleep(1)

def run_one_shot():
    global bjt, mos
    bjt = BjtDriver(pin=BJT_PIN, active_high=True)
    mos = MosfetDriver(pin=MOSFET_PIN, active_high=True)

    # Timing sanity check
    min_required = (ON_MS_BJT if USE_BJT else 0) \
                 + (GAP_MS if (USE_BJT and USE_MOSFET) else 0) \
                 + (ON_MS_MOSFET if USE_MOSFET else 0)
    if min_required > PERIOD_MS:
        print("WARNING: PERIOD_MS too small. min_required={}, PERIOD_MS={}"
              .format(min_required, PERIOD_MS))

    # Idle
    bjt.off(); mos.off()

    print("Arming delay started.")
    countdown(START_DELAY_S)
    print("Running one-shot for", RUN_TIME_S, "seconds.")

    start_ms   = time.ticks_ms()
    end_ms     = time.ticks_add(start_ms, RUN_TIME_S * 1000)

    # Drift-free schedule: march next_tick forward by PERIOD_MS each cycle
    next_tick  = start_ms
    cycles     = 0
    missed     = 0
    last_ts    = start_ms  # for measuring actual average period

    while time.ticks_diff(end_ms, time.ticks_ms()) > 0:
        cycles += 1
        cycle_start = time.ticks_ms()

        # Workload
        if USE_BJT:
            bjt.pulse_ms(ON_MS_BJT)
        if USE_BJT and USE_MOSFET and GAP_MS > 0:
            time.sleep_ms(GAP_MS)
        if USE_MOSFET:
            mos.pulse_ms(ON_MS_MOSFET)

        # Advance schedule and wait until that exact tick (if possible)
        next_tick = time.ticks_add(next_tick, PERIOD_MS)
        wait_ms = time.ticks_diff(next_tick, time.ticks_ms())
        if wait_ms > 0:
            time.sleep_ms(wait_ms)
        else:
            missed += 1  # we overran; no sleep, catch next tick

        last_ts = cycle_start

    # Cleanup
    bjt.off(); mos.off()

    total_ms = time.ticks_diff(time.ticks_ms(), start_ms)
    avg_period = (total_ms / cycles) if cycles else 0

    if missed:
        print("Done with {} overrun cycle(s).".format(missed))
    else:
        print("Done. No overruns detected.")
    print("Cycles: {}, Elapsed: {} ms, Avg period: {:.2f} ms"
          .format(cycles, total_ms, avg_period))
    print("Outputs off. Back at REPL.")

try:
    run_one_shot()
except KeyboardInterrupt:
    print("\nAborted by user (Ctrl-C).")
finally:
    try:
        if bjt: bjt.off()
        if mos: mos.off()
    except Exception:
        pass
    print("Outputs off.")
