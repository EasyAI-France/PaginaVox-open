@echo off
setlocal
cd /d "%~dp0\.."

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

call env\Scripts\activate.bat

python -m pip install --upgrade pyinstaller

set PYINSTALLER_WORKPATH=build\pyinstaller
set SPEC_DIR=build\specs
set ICON_PATH=%CD%\build\icons\icon.ico

if exist "%PYINSTALLER_WORKPATH%" rmdir /s /q "%PYINSTALLER_WORKPATH%"
if exist dist\PaginaVox rmdir /s /q dist\PaginaVox

set ICON_ARGS=
if exist "%ICON_PATH%" (
  set ICON_ARGS=--icon="%ICON_PATH%"
)

pyinstaller ^
  --clean ^
  --noconfirm ^
  --onedir ^
  --name PaginaVox ^
  --workpath "%PYINSTALLER_WORKPATH%" ^
  --specpath "%SPEC_DIR%" ^
  %ICON_ARGS% ^
  --collect-all qwen_tts ^
  --collect-all torch ^
  --collect-all torchaudio ^
  --collect-all torchvision ^
  --collect-all transformers ^
  --collect-all accelerate ^
  --collect-all huggingface_hub ^
  --collect-all whisper ^
  --collect-all soundfile ^
  --hidden-import numpy ^
  main.py

if errorlevel 1 (
  echo.
  echo Build echoue.
  exit /b 1
)

mkdir dist\PaginaVox\audio 2>nul
mkdir dist\PaginaVox\txt 2>nul
mkdir dist\PaginaVox\output 2>nul
mkdir dist\PaginaVox\profiles 2>nul

copy README.md dist\PaginaVox\README.md >nul
copy README.fr.md dist\PaginaVox\README.fr.md >nul
copy HELP.md dist\PaginaVox\HELP.md >nul
copy AIDE.md dist\PaginaVox\AIDE.md >nul
copy INSTALLATION.md dist\PaginaVox\INSTALLATION.md >nul

echo.
echo Build termine.
echo Dossier a distribuer :
echo dist\PaginaVox
echo.
echo Les utilisateurs Windows lanceront :
echo PaginaVox.exe
