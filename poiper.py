import wave
from piper import PiperVoice, SynthesisConfig
syn_config = SynthesisConfig(
        volume = 3,
        noise_scale = 1.0,
        noise_w_scale=1.0
        )

voice = PiperVoice.load("en_US-arctic-medium.onnx")
with wave.open("test.wav", "wb") as wav_file:
    voice.synthesize_wav("hello my fellow kids, how are we doing today", wav_file, syn_config=syn_config)
