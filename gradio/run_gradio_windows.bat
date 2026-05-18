@echo off
setlocal
cd /d "%~dp0\.."

if not exist env\Scripts\python.exe (
  echo Environnement Python introuvable.
  echo Lance d'abord :
  echo install_env_windows.bat
  exit /b 1
)

env\Scripts\python.exe -c "import gradio" >nul 2>nul
if errorlevel 1 (
  echo Gradio est introuvable. Installation des dependances...
  call env\Scripts\activate.bat
  pip install -r requirements.txt
)

env\Scripts\python.exe gradio\app.py
