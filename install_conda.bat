@echo off
title PaginaVox
setlocal
cd /d "%~dp0"

where conda >nul 2>nul
if errorlevel 1 (
  echo Conda est introuvable. Installe Miniconda ou Anaconda avant de continuer.
  echo https://docs.conda.io/en/latest/miniconda.html
  exit /b 1
)

conda env create -f environment.yml
if errorlevel 1 (
  echo.
  echo L'environnement existe peut-etre deja. Mise a jour en cours...
  conda env update -f environment.yml --prune
)

echo.
echo Installation terminee.
echo Lance ensuite :
echo conda activate paginavox-command
echo python main.py
