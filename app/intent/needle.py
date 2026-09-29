from time import sleep
import needle
from gpiozero import LED
from poiper import play_sound

@needle.tool
def blink_led(pin: int):
    """Turn an led on for one second, and off."""
    led = LED(pin)
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    return f"LED on pin {pin} blinked."

@needle.tool
def talk_to_user(instruction:str):
    """Talk to the user."""
    print(instruction)
    play_sound(instruction)
    return f"User yapped to."


agent = needle.Needle(tools=[blink_led, talk_to_user])
result = agent.run(
    "Blink the led at pin 14 and say hello to the user"
)

print(result)
