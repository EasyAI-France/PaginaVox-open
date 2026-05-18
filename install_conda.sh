#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if ! command -v conda >/dev/null 2>&1; then
  echo "Conda est introuvable. Installe Miniconda ou Anaconda avant de continuer."
  echo "https://docs.conda.io/en/latest/miniconda.html"
  exit 1
fi

if conda env list | grep -q "paginavox-command"; then
  conda env update -f environment.yml --prune
else
  conda env create -f environment.yml
fi

echo
echo "Installation terminee."
echo "Lance ensuite :"
echo "conda activate paginavox-command"
echo "python main.py"
