
from gpiozero import LED
from time import sleep

def blink_led(pin: int):
    led = LED(pin)

    try:
        led.on()
        sleep(1)
        led.off()

        print(f"LED at GPIO {pin} blinked")

        return {
            "blink": True,
            "pin": pin,
            "blink_time": 1
        }

    finally:
        led.close()
