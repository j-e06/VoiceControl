
import queue
import re
import threading
import time
import wave
from pathlib import Path

import numpy as np
import needle

from microphone import Listener
from tool_exec import ToolExecutor


class VoiceAssistant:
    def __init__(self):
        self.wake_word = "Lena"
        self.command_timeout = 7
        self.armed_until = 0.0

        self.wav_path = Path(__file__).resolve().parent / "last_utterance.wav"

        self.whistle = needle.Whistle()
        self.tools = ToolExecutor()

        self.utterance_queue = queue.Queue(maxsize=4)

        self.worker = threading.Thread(
            target=self.process_queue,
            daemon=True,
        )
        self.worker.start()

    def queue_utterance(self, audio):
        finished_at = time.monotonic()

        try:
            self.utterance_queue.put_nowait((audio, finished_at))
        except queue.Full:
            print("Processing queue full. Dropping utterance.")

    def process_queue(self):
        while True:
            audio, finished_at = self.utterance_queue.get()

            try:
                self.process_utterance(audio, finished_at)
            except Exception as error:
                print("Processing error:", error)
            finally:
                self.utterance_queue.task_done()

    def save_wav(self, audio):
        pcm = (
            np.clip(audio, -1, 1) * 32767
        ).astype(np.int16)

        with wave.open(str(self.wav_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(16000)
            wav.writeframes(pcm.tobytes())

    def process_utterance(self, audio, finished_at):
        self.save_wav(audio)

        result = self.whistle.transcribe(
            str(self.wav_path),
            language="en",
            keywords=[self.wake_word, "LED", "GPIO", "blink led", "pin 14"],
        )

        text = result.get("text", "").strip()

        if not text:
            return

        print("Whistle:", text)

        wake_match = re.match(
            r"^\s*lena\b[\s,.:;!?-]*",
            text,
            flags=re.IGNORECASE,
        )

        if wake_match:
            command = text[wake_match.end():].strip()

            # some goof only said keyword, not anything after
            if not command:
                self.armed_until = (
                    time.monotonic() + self.command_timeout
                )
                print("Activated. Waiting for command...")
                return

        elif finished_at <= self.armed_until:
            # activated by a previous utterance.
            command = text

        else:
            # nowake word ignore yap
            return

        if not command:
            return

        # deactivete before exec
        self.armed_until = 0.0

        print("Executing:", command)

        # needle to tool
        results = self.tools.run_command(command)
        print("Results:", results)

    def run(self):
        listener = Listener(
            on_utterance=self.queue_utterance
        )

        listener.run()


if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()