# VoiceControl
Voice controller for Metropolia Software Factory robot. Will be able to take in commands via voice, act on them and give responses back.


Techstack looks like the following currently:

Speech To Text <b>Whisper.cpp</b>

Wake word detection <b>openWakeWord</b>

Intent parsing <b>Cactus Needle</b>

Text To Speech <b>Piper TTS</b>

Operating device: <b>Currently, 4GB Raspberry pi 4B</b>

Intended sequence of events is currently:
User talks into the microphone -> oWW reacts to chosen wake word, passes signal to Needle -> Needle deci
des if there is something it can do based on the users instructions -> response passed to Piper TTS to be given as feedback to user.