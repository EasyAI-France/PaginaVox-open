#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ ! -x env/bin/python ]; then
  echo "Environnement Python introuvable."
  echo "Lance d'abord : bash install_env_linux.sh"
  exit 1
fi

if ! env/bin/python -c "import sys" >/dev/null 2>&1; then
  echo "Environnement Python casse ou obsolete."
  echo "Lance : bash install_env_linux.sh"
  exit 1
fi

env/bin/python main.py
