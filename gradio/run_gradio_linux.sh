#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

if [ ! -x env/bin/python ]; then
  echo "Environnement Python introuvable."
  echo "Lance d'abord : bash install_env_linux.sh"
  exit 1
fi

if ! env/bin/python -c "import gradio" >/dev/null 2>&1; then
  echo "Gradio est introuvable. Installation des dependances..."
  env/bin/pip install -r requirements.txt
fi

env/bin/python gradio/app.py
