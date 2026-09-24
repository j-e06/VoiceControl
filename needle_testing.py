from time import sleep
import needle_testing
from gpiozero import LED
from pathlib import Path

@needle_testing.tool
def blink_led(pin: int):
    led = LED(pin)
    led.on()
    sleep(1)
    led.off()
    sleep(1)

agent = needle_testing.Needle(tools=[blink_led])
print(agent.run("Blink the led at pin 14.")["results"])