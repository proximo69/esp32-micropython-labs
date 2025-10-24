from machine import Pin

def run(pin_no=2):
    """Continuous GPIO toggle for logic analyzer measurement."""
    p = Pin(pin_no, Pin.OUT)
    while True:
        p.value(1)
        p.value(0)

if __name__ == "__main__":
    run()
