## Extended Description
*(Based on Chapter 3 – Lab 1 from Programming the ESP32 with MicroPython by Dr. Stephen Smith)*


Chapter 3 – Lab 1: Blinky

📘 Textbook Reference

Programming the ESP32 with MicroPython by Dr. Stephen Smith
Chapter 3: Getting Started with GPIO


🎯 Objective

To create a simple MicroPython program that toggles an LED on and off — demonstrating the fundamental concept of digital output control on the ESP32 microcontroller.
This lab establishes the foundation for later experiments in timing, input handling, and multi-pin control.


🧠 Learning Outcomes

By completing this lab, I will be able to:

Initialize and configure a GPIO pin as a digital output in MicroPython.

Generate periodic on/off signals using loops and timing delays.

Verify correct hardware operation through LED blinking.

Understand how MicroPython interacts with ESP32’s hardware-level registers.


🧰 Materials

Component	Description

ESP32 Dev Board	e.g., ESP32-WROOM-32
LED	Any standard color (e.g., 5 mm red or blue)
Resistor	220 Ω current-limiting resistor
Breadboard & Jumpers	For circuit connection
Thonny or PyCharm IDE	For uploading code and monitoring output


⚡ Circuit Diagram

GPIO Pin: 2 (onboard LED) or external LED on any output-capable pin

Connection:

GPIO → Resistor → LED (anode)

LED cathode → GND



GPIO 2  ----> [220Ω] ----> |>| ----> GND


💻 Code Listing

from machine import Pin
from time import sleep

led = Pin(2, Pin.OUT)  # GPIO2 as output (onboard LED)

while True:
    led.value(1)  # Turn LED on
    sleep(0.5)    # Delay 500 ms
    led.value(0)  # Turn LED off
    sleep(0.5)


🧪 Procedure

1. Wire the LED and resistor to the ESP32 as shown.
2. Upload and run the program.
3. Observe the LED blinking on and off once per second.
4. Experiment by adjusting the sleep() interval for faster or slower blinking.
5. Optionally, capture a short video of the blinking LED for documentation.


📊 Results & Observations

The LED toggled cleanly at the programmed interval.
Reducing the delay to below 0.1 seconds results in perceptible flicker; below 0.02 seconds, the LED appears continuously lit due to human persistence of vision.
This exercise illustrates the practical limits of human-visible frequency and introduces the concept of timing resolution in MicroPython.


🧩 Discussion

The Blinky experiment is a rite of passage for embedded programmers.
It may seem trivial, but it demonstrates three essential principles:

1. Hardware Abstraction:
How high-level MicroPython commands translate into low-level hardware actions.
2. Timing Control:
The role of delay functions in controlling device behavior, and how processor speed and interpreter overhead affect precision.
3. Verification & Debugging:
Using an LED as a simple, visible indicator of program flow — a foundational debugging tool in hardware development.

Future labs build directly on this exercise by replacing manual delays with high-speed logic testing and register-level control, enabling more advanced timing and synchronization experiments.


📸 Media

Blinky_Demo.mp4 — Short video clip showing the LED blinking at 1 Hz.
https://www.youtube.com/shorts/yGk6kcG_ueg

Circuit_Diagram.png — Annotated schematic of the wiring setup.


✍️ Author Notes

This lab marks the starting point of my embedded systems learning path.
Though simple, it provided a tactile sense of control over the ESP32 and established the confidence needed to explore more complex GPIO and timing operations in subsequent labs.
