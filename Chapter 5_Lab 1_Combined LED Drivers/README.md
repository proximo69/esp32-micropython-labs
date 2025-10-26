# Chapter 5 – Lab 1: Combined LED Driver Test  
*Programming the ESP32 with MicroPython – Section 1 Final Lab*

---

## 🎯 Objective

This lab combines two independent LED driver circuits — one using a **BJT transistor** and the other using a **MOSFET** — into a single coordinated test program.

It demonstrates **modular programming**, **timing control**, and **safe execution** using MicroPython’s `time` and `machine` modules.  
By running both drivers in sequence, the ESP32 produces visible and measurable pulse streams that can be verified on a logic analyzer.

---

## 🧠 Concepts Reinforced

| Concept | Description |
|----------|-------------|
| **Modular Design** | Separate Python files (`bjt_driver.py`, `mosfet_driver.py`, `main.py`) form a clean, reusable structure. |
| **Class-Based Hardware Control** | Each driver encapsulates pin configuration and on/off logic. |
| **Timing & Scheduling** | Uses `time.sleep_ms()` and `time.ticks_ms()` for precise control of pulse intervals. |
| **Exception Handling** | `try / except / finally` ensures outputs always return to a safe OFF state. |
| **Testing & Verification** | Output signals are captured in **PulseView** using a logic analyzer for waveform analysis. |

---

## ⚙️ Materials

- **ESP32 Development Board** (WROOM or similar)  
- **Breadboard and jumpers**  
- **NPN BJT transistor** (e.g., PN2222, 2N3904)  
- **Logic-level N-MOSFET** (e.g., IRLZ44N or IRL540N)  
- **Two LEDs** (different colors)  
- **Current-limiting resistors** (220–330 Ω typical)  
- **Two pushbuttons** *(optional for future lab extensions)*  
- **Logic Analyzer + PulseView software**

---

## 🧩 File Overview

| File | Purpose |
|------|----------|
| **bjt_driver.py** | Defines the `BjtDriver` class to control a low-side NPN transistor LED circuit. |
| **mosfet_driver.py** | Defines the `MosfetDriver` class to control a logic-level MOSFET LED circuit. |
| **main.py** | Coordinates both drivers, applying precise timing, an arming delay, and safe cleanup. |

---

## 🔍 Program Behavior

1. **Imports drivers and time module.**  
2. Defines an **arming delay** (10 s) to allow the user to prepare PulseView.  
3. Executes a **one-shot window** (10 s total) where:  
   - The BJT LED driver pulses first.  
   - A short **phase gap** separates the two signals.  
   - The MOSFET LED driver pulses second.  
4. Each cycle repeats at a defined **period** (200 ms default).  
5. On completion or manual interruption (Ctrl-C), all outputs return to the OFF state.

---

## 🧮 Timing Diagram (Conceptual)
|<--------- PERIOD_MS = 200 ms --------->| [BJT ON 50 ms] [GAP 10 ms] [MOSFET ON 50 ms] [REMAIN 90 ms idle]

Measured on PulseView, this produces distinct, non-overlapping square waves at the chosen cycle period.

---

## 🛠️ Configuration Parameters

Defined at the top of `main.py`:

| Variable | Default | Description |
|-----------|----------|-------------|
| `START_DELAY_S` | 10 | Seconds to wait before pulses begin (arming time). |
| `RUN_TIME_S` | 10 | Total run duration in seconds. |
| `PERIOD_MS` | 200 | Period between starts of each test cycle. |
| `ON_MS_BJT` | 50 | Duration of the BJT ON pulse. |
| `ON_MS_MOSFET` | 50 | Duration of the MOSFET ON pulse. |
| `GAP_MS` | 10 | Delay between the two pulses each cycle. |
| `BJT_PIN` | 16 | GPIO output for the BJT circuit. |
| `MOSFET_PIN` | 17 | GPIO output for the MOSFET circuit. |

---

## 🧰 Usage Instructions

1. **Upload all three files** to the ESP32:
   - `bjt_driver.py`  
   - `mosfet_driver.py`  
   - `main.py`
2. **Connect the circuits** as shown in your breadboard layout.  
3. **Start PulseView** and arm the logic analyzer on the BJT and MOSFET input pins.  
4. **Run the program**:
   ```python
   >>> import main
5. Observe the countdown messages in REPL during arming delay.


6. Capture and analyze pulses in PulseView.


7. After completion, verify that both LEDs are off.

## Circuit Diagrams

### 🧲 BJT LED Driver (NPN, e.g., PN2222)

3.3V ──[220Ω]──▶│──┐
                     │
                     │ LED (red)
                     │
                 Collector
                    │
  ESP32 GPIO16 ─┬──B   NPN BJT
                │      (PN2222)
                └───[1kΩ]───┤
                            │
                          Emitter
                            │
                           GND

**Operation:**  
When GPIO16 outputs HIGH, base current flows through the 1 kΩ resistor into the BJT base, turning it ON and allowing current to flow through the LED → resistor → collector → emitter → GND.  
When GPIO16 goes LOW, the transistor switches OFF and the LED turns off.

---

### ⚙️ MOSFET LED Driver (N-channel, logic-level)

3.3V ──[220Ω]──▶│──┐
                     │
                     │ LED (green)
                     │
                 Drain
                    │
  ESP32 GPIO17 ────Gate
                    │
               Source → GND

**Operation:**  
When GPIO17 outputs HIGH (~3.3 V), the MOSFET gate voltage rises enough to switch it ON, allowing current to flow through the LED.  
When GPIO17 goes LOW, the MOSFET switches OFF and current stops.

> 💡 *In practice, a small 100 Ω gate resistor can be added between GPIO17 and the MOSFET gate for noise suppression, though not strictly required in low-speed tests like this.*

---

🔒 Safety and Recovery

If interrupted (Ctrl-C), the finally block ensures all GPIOs are set LOW (OFF).

The main.py file prevents infinite loops — it is always safe to upload and re-run.

Using non-boot-strap pins (GPIO 16, 17) prevents ESP32 startup issues.



---

📈 Example Observations

Test	Measured High	Measured Low	Notes

BJT Driver	~50 ms	~150 ms	Matches expected duty cycle.
MOSFET Driver	~50 ms	~150 ms	Similar timing, phase shifted by 10 ms.


Captured with 1 ms/div time base in PulseView.


---

🧭 Key Takeaways

Practiced modular program design using multiple .py files.

Implemented class-based abstraction to control hardware cleanly.

Understood MicroPython timing functions and the importance of delay precision.

Reinforced safe execution and cleanup through try–except–finally.

Verified output behavior with a logic analyzer, bridging software and hardware.



---

🧑‍🔬 Next Steps

Introduce input pushbuttons to select which driver test to run.

Add frequency sweep or PWM control using machine.PWM.

Use ADC input to monitor voltage response for driver characterization.



---

Author: Michael Bradford
Project: Programming the ESP32 with MicroPython
Lab: Chapter 5 – Lab 1 • Combined LED Driver Test
Date: October 2025
