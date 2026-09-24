#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"
VOICE="en_US-arctic-medium"
VOICE_FILE="${VOICE}.onnx"

echo "==> Voice Control installation"

# make sure python is installed, should always be since running on rasp4 but double check.
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "==> Using Python: $(python3 --version)"

# check if venv already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "==> Virtual environment already exists."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

echo "==> Updating pip..."
python -m pip install --upgrade pip

# install requirements.
if [ -f "requirements.txt" ]; then
    echo "==> Installing Python dependencies..."
    pip install -r requirements.txt
else
  # should not be possible to get here.
    echo "WARNING: requirements.txt not found."
fi


if [ -f "$VOICE_FILE" ]; then
    echo "==> Piper voice already exists: $VOICE_FILE"
else
    echo "==> Downloading Piper voice: $VOICE"
    python -m piper.download_voices "$VOICE"
fi

# --------------------------------------------------
# 6. Finish
# --------------------------------------------------

echo
echo "==> Setup complete!"
echo
echo "To activate the environment manually:"
echo "    source $VENV_DIR/bin/activate"
echo
echo "To start VoiceControl:"
echo "    python main.py"