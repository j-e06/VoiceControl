
import queue
from collections import deque

import numpy as np
import sounddevice as sd
import torch
from silero_vad import load_silero_vad, VADIterator


class Listener:
    def __init__(self, on_utterance):
        self.on_utterance = on_utterance

        self.sample_rate = 16000
        self.chunk_size = 512
        self.silence_ms = 700
        self.max_seconds = 29

        self.audio_queue = queue.SimpleQueue()
        self.pre_roll = deque(maxlen=16)

        self.recording = False
        self.frames = []

        torch.set_num_threads(1)

        model = load_silero_vad()
        self.vad = VADIterator(
            model,
            sampling_rate=self.sample_rate,
            min_silence_duration_ms=self.silence_ms,
            speech_pad_ms=100,
        )

    def audio_callback(self, indata, frames, time_info, status):
        self.audio_queue.put(indata[:, 0].copy())

    def run(self):
        print("Listening for speech...")

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=self.chunk_size,
                callback=self.audio_callback,
            ):
                while True:
                    chunk = self.audio_queue.get()
                    event = self.vad(torch.from_numpy(chunk))

                    # Speech begins
                    if not self.recording and event and "start" in event:
                        self.recording = True
                        self.frames = list(self.pre_roll) + [chunk]
                        print("Speech started")

                    elif self.recording:
                        self.frames.append(chunk)

                    self.pre_roll.append(chunk)

                    # Speech ends
                    if self.recording and event and "end" in event:
                        audio = np.concatenate(self.frames)

                        self.recording = False
                        self.frames = []

                        print("Speech ended")

                        duration = len(audio) / self.sample_rate

                        if duration <= self.max_seconds:
                            self.on_utterance(audio)
                        else:
                            print("Audio too long, skipping")

                    # max rec length check, 30s by way of cactus instructions
                    if self.recording:
                        length = len(self.frames) * self.chunk_size

                        if length > self.max_seconds * self.sample_rate:
                            self.recording = False
                            self.frames = []
                            self.pre_roll.clear()
                            self.vad.reset_states()
                            print("Recording limit reached")

        except KeyboardInterrupt:
            print("Listener stopped")
