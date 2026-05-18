#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-python3.12}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "$PYTHON_BIN est introuvable. Installe Python 3.12 ou lance avec PYTHON_BIN=python3."
  exit 1
fi

if [ ! -d env ]; then
  "$PYTHON_BIN" -m venv env
fi

source env/bin/activate
python -m pip install --upgrade pip
pip install torch==2.6.0+cu124 torchaudio==2.6.0+cu124 torchvision==0.21.0+cu124 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
mkdir -p audio txt output profiles
echo
echo "Installation terminee dans command/env."
echo "Lance ensuite :"
echo "source env/bin/activate"
echo "python main.py"
