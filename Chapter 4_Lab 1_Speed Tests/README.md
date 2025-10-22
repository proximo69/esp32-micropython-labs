
LAB to Accompany Programming the ESP32 in MicroPython by Harry Fairchild
Chapter 4 – Lab 1: How Fast? (Expanded Speed Tests)
Goal
Determine how fast the ESP32 can toggle a GPIO pin under different MicroPython execution conditions.
This lab explores interpreter overhead, function call latency, and the performance gains from native code compilation.

Textbook Reference:
Programming the ESP32 with MicroPython — Chapter 4, “How Fast?”

🎯 Learning Objectives
Compare GPIO toggle speed between baseline, function-based, and native-compiled code.
Capture and measure digital pulse widths using a logic analyzer
Quantify MicroPython’s instruction overhead.
Discuss the role of just-in-time compilation and hardware timers in improving performance.

🧰 Materials
Component                  	              Description
ESP32 Dev Board       	            e.g., ESP32-WROOM-32
Logic Analyzer	                        DSLogic Plus, HiLetGo 24 MHz, or similar
Software	                                   PulseView (Sigrok)
Breadboard & Jumper Wires   	For clean signal connection

🧪 Lab Tasks
Test A — Baseline Loop
Filename: speed_test_a_baseline.py

from machine import Pin
p = Pin(2, Pin.OUT)
while True:
    p.value(1)
    p.value(0)

Direct loop toggling the GPIO pin.

Provides the pure interpreter baseline for speed measurement.
Test B — Function Encapsulation
Filename: speed_test_b_function.py

from machine import Pin

def flash():
    p = Pin(2, Pin.OUT)
    while True:
        p.value(1)
        p.value(0)

flash()

The same toggle loop wrapped inside a function.

Demonstrates how MicroPython’s function-call structure introduces additional overhead.

Test C — Native Decorator Optimization
Filename: speed_test_c_native.py

import time
from machine import Pin
import micropython  # needed for the decorator

@micropython.native
def flash():
    p = Pin(2, Pin.OUT)
    t_end = time.ticks_add(time.ticks_ms(), 2000)  # run ~2 seconds
    while time.ticks_diff(t_end, time.ticks_ms()) > 0:
        p.value(1)
        p.value(0)

flash()

Uses the @micropython.native decorator to compile the function to native machine code.

Measures performance improvement over pure interpreted code.

Logic Analyzer Setup
Connection	                             Description
Channel 0 → GPIO 2	               Capture toggle signal
Ground → ESP32 GND	   Common ground reference
Sample Rate: ≥ 10 MHz            recommended (minimum 5 MHz).

Observation: Square wave output with measurable high/low periods.

Measurements and Expected Results
Test	Description	Typical Period (µs)	Approx. Frequency (kHz)

A	Baseline	≈ 11–12 µs	83–90 kHz
B	Function call	Slightly slower	~75–80 kHz
C	Native decorator	Noticeably faster	~130–150 kHz


Results will vary by board and firmware version.

Interpretation
Baseline vs. Function: The function wrapper adds minor call overhead per loop iteration.
Native Compilation: Reduces interpreter overhead, nearly doubling GPIO speed.
Pulse Asymmetry: High and low durations differ slightly (~0.4 µs) due to instruction scheduling and timing granularity.
Hardware Potential: The ESP32’s C-level GPIO toggling can exceed 10 MHz, showing how much performance MicroPython trades for convenience.

🧩 Discussion Questions

1. Why do the high and low durations differ slightly?

2. How does function encapsulation affect timing consistency?

3. How does the @micropython.native decorator reduce overhead?

4. What further gains might @micropython.viper or machine.Signal provide?

5. In which types of projects would such speed differences matter most?


📓 Summary

This experiment illustrates how MicroPython’s interpreter introduces significant timing overhead compared to compiled execution.
By progressively optimizing the same loop — from direct inline code to function-based, then native-compiled — you can visualize how code structure and decorators affect GPIO performance.

Key Takeaway:
For applications demanding microsecond-level timing (PWM generation, serial protocols, or pulse sensing), use native/Viper decorators or hardware peripherals rather than pure Python loops.
