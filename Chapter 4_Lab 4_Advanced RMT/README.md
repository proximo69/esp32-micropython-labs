# 💡 Chapter 4 – Lab 4: Advanced RMT (Remote Control Module)

**Textbook Reference:** *Programming the ESP32 with MicroPython* — Chapter 4, RMT Peripheral Section  
**Project Folder:** `Chapter 4 - Lab 4 - Advanced RMT`  
**File:** `RMT_test.py`

---

## 🧠 Overview

This lab explores the **ESP32’s RMT (Remote Control) peripheral**, a hardware module designed for generating or decoding **precisely timed pulse sequences**.

Unlike software-based timing (e.g., using `time.sleep_us()`), RMT operates **independently of the CPU**, providing *deterministic microsecond-level accuracy*.  
It’s ideal for tasks such as:

- Infrared (IR) remote control signals  
- WS2812 / NeoPixel LED data streams  
- Ultrasonic sensor triggers  
- Any application needing strict timing control

---

## 🎯 Learning Objectives

1. Understand the purpose and advantages of the **RMT hardware peripheral**.  
2. Configure an RMT transmitter in MicroPython using the `esp32` module.  
3. Generate custom pulse sequences with precise high/low durations.  
4. Capture and analyze waveforms using a logic analyzer.  
5. Compare hardware-timed signals to software-timed ones from earlier labs.

---

## 🧰 Materials

| Item | Purpose |
|------|----------|
| ESP32 development board | Main microcontroller |
| Logic Analyzer (e.g., DSLogic Plus or HiLetGo 24 MHz) | Timing verification |
| PulseView software | Visualize and measure signals |
| Breadboard & jumper wires | Connections |
| 1 × LED (optional) | Visual output test |
| 1 × 220 Ω resistor | Current limiting for LED |

---

## ⚙️ Circuit Setup

| Pin | Connection |
|-----|-------------|
| GPIO 14 | Output to logic analyzer or LED + 220 Ω resistor |
| GND | Common ground |

> The LED is optional. For accurate measurements, connect your logic analyzer probe to **GPIO 14**.

---

## 🧩 Program Description

The file **`RMT_test.py`** contains three selectable demos.  
Set the `MODE` variable at the top of the file to choose which one runs:

| Mode | Function | Description |
|------|-----------|-------------|
| `"fixed"` | `demo_fixed()` | Sends 100 µs high / 100 µs low pulses repeatedly |
| `"bitstream"` | `demo_bitstream()` | Transmits a binary sequence (1s = 600 µs pulse, 0s = 300 µs) |
| `"loop"` | `demo_loop()` | Generates a continuous hardware-timed waveform for several seconds |

### Example Configuration
```python
MODE = "fixed"       # or "bitstream", or "loop"
PIN = 14
CLOCK_DIV = 80       # 1 µs resolution
