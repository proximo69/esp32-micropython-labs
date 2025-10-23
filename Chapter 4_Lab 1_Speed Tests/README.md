# 🧪 Chapter 4 – Lab 1: Speed Tests  
**Programming the ESP32 with MicroPython**

Determine how fast the ESP32 can toggle a GPIO pin under different MicroPython execution conditions.  
This lab explores interpreter overhead, function call latency, and the performance gains from native code compilation.

**Textbook Reference:**  
*Programming the ESP32 with MicroPython* — Chapter 4, “How Fast?”

---

## 🎯 Learning Objectives

- Compare GPIO toggle speed between baseline, function-based, and native-compiled code  
- Capture and measure digital pulse widths using a logic analyzer  
- Quantify MicroPython’s instruction overhead  
- Discuss the role of just-in-time compilation and hardware timers in improving performance  

---

## 🧰 Materials

| Component | Description |
|------------|-------------|
| **ESP32 Dev Board** | e.g., ESP32-WROOM-32 |
| **Logic Analyzer** | DSLogic Plus, HiLetGo 24 MHz, or similar |
| **Software** | PulseView (Sigrok) |
| **Breadboard & Jumper Wires** | For clean signal connection |

---

## 🧪 Lab Tasks

### **Test A — Baseline Loop**
**Filename:** `speed_test_a_baseline.py`
```python
from machine import Pin
p = Pin(2, Pin.OUT)
while True:
    p.value(1)
    p
```

Direct loop toggling the GPIO pin.
Provides the pure interpreter baseline for speed measurement.

### **Test B — Function Code Loop**
**Filename:** `speed_test_b_function.py`
```python

from machine import Pin

def flash():
    p = Pin(2, Pin.OUT)
    while True:
        p.value(1)
        p.value(0)

flash()
```

The same toggle loop wrapped inside a function.
Demonstrates how MicroPython’s function-call structure introduces additional overhead.

### **Test C — Native Code Loop**
**Filename:** `speed_test_c_native.py`
```python


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
```

Uses the @micropython.native decorator to compile the function to native machine code.
Measures performance improvement over pure interpreted code.


## Logic Analyzer Setup
Connection	                             Description
Channel 0 → GPIO 2	               Capture toggle signal
Ground → ESP32 GND	   Common ground reference
Sample Rate: ≥ 10 MHz            recommended (minimum 5 MHz).

Observation: Square wave output with measurable high/low periods.

## 📈 Measurements and Expected Results

| Test | Description        | Typical Period (µs) | Approx. Frequency (kHz) |
|------|--------------------|--------------------:|------------------------:|
| **A** | Baseline           | ≈ 11–12 µs          | 83–90 kHz               |
| **B** | Function call      | Slightly slower     | ~75–80 kHz              |
| **C** | Native decorator   | Noticeably faster   | ~130–150 kHz            |

*Results may vary depending on board and firmware version.*

Results will vary by board and firmware version.

Interpretation
Baseline vs. Function: The function wrapper adds minor call overhead per loop iteration.
Native Compilation: Reduces interpreter overhead, nearly doubling GPIO speed.
Pulse Asymmetry: High and low durations differ slightly (~0.4 µs) due to instruction scheduling and timing granularity.
Hardware Potential: The ESP32’s C-level GPIO toggling can exceed 10 MHz, showing how much performance MicroPython trades for convenience.

## 🧩 Discussion Questions

1. Why do the high and low durations differ slightly?

2. How does function encapsulation affect timing consistency?

3. How does the @micropython.native decorator reduce overhead?

4. What further gains might @micropython.viper or machine.Signal provide?

5. In which types of projects would such speed differences matter most?


## 📓 Summary

This experiment illustrates how MicroPython’s interpreter introduces significant timing overhead compared to compiled execution.
By progressively optimizing the same loop — from direct inline code to function-based, then native-compiled — you can visualize how code structure and decorators affect GPIO performance.

Key Takeaway:
For applications demanding microsecond-level timing (PWM generation, serial protocols, or pulse



## ⚠️ Notes on Trigger Timing and Analyzer Limitations

During testing of the `@micropython.native` version of the **Flash Speed Test** (20-second pulse loop), I encountered timing issues when attempting to capture the waveform using the **HiLetgo 24 MHz USB Logic Analyzer** with **PulseView**.

### Observed Behavior
- When using a **rising-edge trigger**, PulseView would **timeout before the pulse occurred**, stopping the capture before any data was recorded.  
- Increasing the pulse duration from 2 s to 20 s caused the ESP32 to **lock up** (remain “busy”) due to the `@micropython.native` decorator executing the tight loop without interpreter interrupts.  
- Lowering the analyzer’s **sample rate** from 24 MHz to 12 MHz effectively **doubled the real-time capture window**, allowing slightly more time to arm the analyzer and start the MicroPython script before timeout.

### Technical Explanation
- The HiLetgo analyzer is a **Saleae Logic clone** based on the **Cypress FX2LP (CY7C68013A)** chip. It streams samples directly over USB and lacks onboard memory or a true hardware trigger engine.  
- PulseView’s “trigger” for this device is **software-simulated** — it buffers streamed data and discards it until the condition is met, but times out if no trigger occurs within a short period (typically a few seconds).  
- Because of this limitation, it is **not possible to disable auto-trigger** or to **wait indefinitely** for a rising-edge event.  
- Lowering the sample rate extends the real-time duration of the capture (e.g., at 12 MHz, a 1 M-sample capture covers roughly twice the real time of a 24 MHz capture).

### Takeaway
- This analyzer performs well for **short, repetitive, or periodic signals**, but not for **long-delay, single-shot events**.  
- For extended trigger waits or precise pre/post-trigger control, consider upgrading to a logic analyzer with a true hardware trigger engine — such as a **Kingst LA2016**, **DSLogic Plus**, or genuine **Saleae Logic**.

---
