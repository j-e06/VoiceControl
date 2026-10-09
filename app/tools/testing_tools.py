from gpiozero import LED
from time import sleep
def blink_led(pin: int):
    led = LED(pin)
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    print("LED at pin", pin, "blinked.")
    return {
        "blink": True,
        "blink_time": 1
    }