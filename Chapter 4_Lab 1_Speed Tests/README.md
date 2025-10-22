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
### **Test B — Function Code Loop**
**Filename:** `speed_test_a_baseline.py`
```python

from machine import Pin

def flash():
    p = Pin(2, Pin.OUT)
    while True:
        p.value(1)
        p.value(0)

flash()
```
### **Test C — Native Code Loop**
**Filename:** `speed_test_a_baseline.py`
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
