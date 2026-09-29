# VoiceControl
Voice controller for Metropolia Software Factory robot. Will be able to take in commands via voice, act on them and give responses back.


Techstack looks like the following currently:

VAD(Voice Activity Detector) <b>Silero</b>

Speech To Text <b>Whisper.cpp</b>

Wake word detection <b>openWakeWord</b>

Intent parsing <b>Cactus Needle</b>

Text To Speech <b>Piper TTS</b>

Operating device: <b>Currently, 4GB Raspberry pi 4B</b>

Sequence of events.\
Active microphone input\
SileroVAD waits for speech to be detected\
openWakeWord reacts to Lena to be said\
Whisper turns speech to text and passes to\
Needle turns text into actions\
PiperTTS gives a response to user.


To run whisper on the rasp run the following:
(make sure cmake is installed, if not run the following:)
sudo apt install -y cmake build-essential

git clone https://github.com/ggerganov/whisper.cpp (specifically into /models/)
cd whisper.cpp
cmake -B build
cmake --build build -j4