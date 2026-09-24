import wave
from piper import PiperVoice, SynthesisConfig
import subprocess

voice = PiperVoice.load("en_US-arctic-medium.onnx")

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