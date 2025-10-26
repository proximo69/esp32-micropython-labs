# 🧠 Lab Report

## Title
**Chapter X – Lab X: [Lab Title Here]**

**Course:** Programming the ESP32 with MicroPython  
**Author:** Michael Bradford  
**Date Performed:** [Date]  
**Date Submitted:** [Date]  

---

## Abstract
Provide a concise summary (≈150–250 words) describing what you did, how you did it, and what you found.  
Example:  
> This lab investigated pulse generation and timing accuracy on the ESP32 using MicroPython. PulseView was used to capture GPIO waveforms and compare them against theoretical expectations.

---

## Objective
State the purpose of the lab clearly.  
> The goal of this experiment was to analyze the switching behavior of GPIO outputs and compare timing performance between interpreted and hardware-level execution.

---

## Background / Theory
Summarize the scientific or technical principles underlying the lab.  
Include any relevant formulas, definitions, or diagrams.  
Example topics:
- Duty cycle and pulse width
- Transistor switching (BJT vs. MOSFET)
- MicroPython timing overhead
- RMT peripheral functionality

---

## Materials and Equipment
| Item | Description | Notes |
|------|--------------|-------|
| ESP32-WROOM Dev Board | MicroPython v1.xx firmware | Primary MCU |
| Logic Analyzer | DSLogic Plus (24 MHz) | Used with PulseView |
| Breadboard & Jumpers | Standard kit | For circuit prototyping |
| Transistors | PN2222 (BJT), IRLZ44N (MOSFET) | For LED driver circuits |
| LEDs & Resistors | Various | For load and biasing |

---

## Procedure
Describe what you did in step-by-step fashion:
1. Assembled the test circuit on the breadboard.  
2. Uploaded `BJT_LEDDriver.py` and `MOSFET_LEDDriver.py` to the ESP32.  
3. Connected the logic analyzer probes to the output pins.  
4. Captured pulse data using PulseView at 24 MHz sample rate.  
5. Recorded timing values and compared them to expected theoretical results.

---

## Results
Present your observations, measurements, and screenshots.

| Measurement | Expected | Observed | Difference |
|--------------|-----------|-----------|-------------|
| Pulse Width (µs) | 100 | 112 | +12% |
| Duty Cycle (%) | 50 | 47 | –3% |

**Figure 1.** Square-wave pulse captured on GPIO14 using PulseView.

> ![PulseView waveform](./images/pulseview_capture.png)

---

## Analysis / Discussion
Interpret what your results mean:
- Explain discrepancies between measured and expected values.  
- Discuss possible sources of error (timing jitter, code delays, hardware variation).  
- Reflect on what you learned about the ESP32, MicroPython timing, or circuit behavior.  
- Compare BJT vs. MOSFET driver performance if applicable.

---

## Conclusion
Summarize the key outcomes:
> This experiment confirmed that MicroPython introduces measurable latency compared to hardware-driven timing. The MOSFET driver provided faster switching due to lower gate charge and reduced voltage drop. Future work could test RMT hardware timing for improved precision.

---

## References
1. Kolban, N. *Programming the ESP32 with MicroPython*. 2021.  
2. Espressif Systems. *ESP32 Technical Reference Manual*. Rev. 4.3, 2024.  
3. PulseView Logic Analyzer Software, Sigrok.org.

---

## Appendix
Include source code listings, extra measurements, or additional photos.

<details>
<summary>📄 Click to expand code listing</summary>

```python
# Example code snippet
from machine import Pin
import time

led = Pin(14, Pin.OUT)
while True:
    led.value(1)
    time.sleep_us(100)
    led.value(0)
    time.sleep_us(100)
