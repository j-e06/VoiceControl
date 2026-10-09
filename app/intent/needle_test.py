from time import sleep
import needle
from gpiozero import LED
import wave
from piper import PiperVoice, SynthesisConfig
import subprocess

voice = PiperVoice.load("models/piper/en_US-arctic-medium.onnx")

syn_config = SynthesisConfig(
    volume=3,
    noise_scale=1.0,
    noise_w_scale=1.0
)

def play_sound(instruction: str):
    with wave.open("test.wav", "wb") as wav_file:
        voice.synthesize_wav(instruction, wav_file, syn_config=syn_config)
    subprocess.run(["aplay", "test.wav"], check=True)
    #subprocess.Popen(["rm", "test.wav"]) # remove file after playing.
    print("Done.")
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

print(needle.transcribe("test.wav")["text"])
