import queue
import sys
import wave

import numpy as np
import sounddevice as sd
import torch
from silero_vad import load_silero_vad


SAMPLE_RATE = 16000
CHUNK_SIZE = 512

audio_queue = queue.Queue()

model = load_silero_vad()


def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    # sounddevice gives us float32 audio. make a copy because the input buffer is reused.
    audio_queue.put(indata[:, 0].copy())


print("Loading Silero VAD...")
print("Listening...")
print("Press Ctrl+C to stop.\n")


speech_active = False
audio_buffer = []

try:
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=CHUNK_SIZE,
        callback=audio_callback,
    ):
        while True:
            audio = audio_queue.get()

            # numpy to pytorch
            audio_tensor = torch.from_numpy(audio)

            speech_probability = model(audio_tensor, SAMPLE_RATE).item()

            currently_speaking = speech_probability >= 0.8

            if currently_speaking and not speech_active:
                print("🗣️ SPEECH START")

                # collecting audio
                audio_buffer.append(audio)

            elif currently_speaking and speech_active:
                # continuecollecting audio
                audio_buffer.append(audio)

            elif not currently_speaking and speech_active:
                print("🔇 SPEECH END")

                if len(audio_buffer) > 0:
                    # Combine all of the chunks into one continuous array
                    full_audio = np.concatenate(audio_buffer)

                    print(
                        f"Captured {len(full_audio) / SAMPLE_RATE:.2f} seconds"
                    )

                    # Convert float32 into 16bit pcm
                    audio_int16 = (full_audio * 32767).astype(np.int16)

                    with wave.open("test.wav", "wb") as wav:
                        wav.setsampwidth(2)
                        wav.setnchannels(1)
                        wav.setframerate(SAMPLE_RATE)
                        wav.writeframes(audio_int16.tobytes())

                    print("Saved test.wav")

                # clear for next time somebody yaps
                audio_buffer.clear()

            speech_active = currently_speaking

except KeyboardInterrupt:
    print("\nStopped.")

except Exception as e:
    print(f"\nError: {e}")
