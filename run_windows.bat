@echo off
title PaginaVox
setlocal
cd /d "%~dp0"

if not exist env\Scripts\python.exe (
  echo Environnement Python introuvable.
  echo Lance d'abord :
  echo install_env_windows.bat
  exit /b 1
)

env\Scripts\python.exe -c "import sys" >nul 2>nul
if errorlevel 1 (
  echo Environnement Python casse ou obsolete.
  echo Lance :
  echo install_env_windows.bat
  exit /b 1
)

env\Scripts\python.exe main.py
