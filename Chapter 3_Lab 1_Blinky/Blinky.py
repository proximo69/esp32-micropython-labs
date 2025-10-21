from machine import Pin
import time

# Define a toggle function
def toggle(pin):
    pin.value(not pin.value())

# Set up pin 2 as an output (on most ESP32 boards, GPIO2 drives the onboard LED)
led = Pin(2, Pin.OUT)

# Blink loop
while True:
    toggle(led) # Flip the LED state
    time.sleep(1) # Wait 1 second
