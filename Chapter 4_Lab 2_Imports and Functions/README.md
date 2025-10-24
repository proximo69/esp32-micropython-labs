# Chapter 4 – Lab 2: Imports and Functions  
**MicroPython & ESP32 – Modular Code Structure**

## 🧩 Extended Description  
An exercise to build an understanding of how to use **imports** in MicroPython to access and execute other program modules.  
This lab demonstrates how to structure MicroPython projects using a **main controller file (`main.py`)** that imports and runs functions from supporting modules (e.g., `speedtest_a_baseline.py`).  
You’ll explore the difference between **top-level code** (which executes on import) and **function-defined code** (which executes only when called), and learn how to use the `if __name__ == "__main__":` pattern for flexible execution.

## 🧪 Objectives  
- Understand how to define and call functions in MicroPython modules.  
- Use the `import` statement to load and invoke functionality from another `.py` file.  
- Structure projects so that `main.py` acts as the central controller while other files serve as reusable modules.  
- Use a logic analyzer to verify program operation at the hardware (GPIO toggle) level.

## 📋 Materials and Tools  
- ESP32 development board with MicroPython firmware installed.  
- USB cable and REPL/IDE connection (e.g., PyCharm with MicroPython support).  
- Logic analyzer (PulseView compatible) and appropriate probes.  
- Onboard LED or external LED connected to GPIO pin 2 (or your preferred pin).  
- Two MicroPython files:  
  - `main.py` — the controller  
  - `speedtest_a_baseline.py` — the module implementing the GPIO toggle test  

## 🔍 Procedure Summary  
1. Create `speedtest_a_baseline.py` with a `run(pin_no=…)` function that toggles the given GPIO pin in a continuous loop.  
2. In `main.py`, `import speedtest_a_baseline` and call `speedtest_a_baseline.run(pin_no=2)`.  
3. Upload both files to the ESP32, reset the board, and observe the LED toggling.  
4. Hook up the logic analyzer, configure a rising-edge trigger, sample at 12 MHz (or higher), capture the waveform, and measure the pulse timing.  
5. Record the measured period (e.g., 8 µs), duty cycle (4 µs high / 4 µs low), and compute the frequency (≈ 125 kHz).

## 📊 Results & Verification  
- The logic analyzer capture shows a **square-wave** pattern on GPIO 2 with ~4 µs high and ~4 µs low, indicating a ~125 kHz toggle frequency.  
- The screenshot (`pulseview_speedtest_baseline.jpg`) is included in this repository for documentation and verification.

## 📁 File Structure
Chapter_4_Lab_2_Imports_and_Functions/
├── README.md
├── main.py
├── speedtest_a_baseline.py
└── pulseview_speedtest_baseline.jpg

## ✅ Outcome  
By completing this lab, you now have a modular MicroPython project: your `main.py` remains lightweight and simply calls external modules, while the modules themselves encapsulate the actual functionality. This sets a solid foundation for your upcoming projects (e.g., BJT/MOSFET LED drivers) where structure, reuse, and clarity will matter.
