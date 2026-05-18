@echo off
title PaginaVox install
setlocal
cd /d "%~dp0"

set "PYTHON_CMD="

where py >nul 2>nul
if not errorlevel 1 (
  py -3.12 -c "import sys" >nul 2>nul
  if not errorlevel 1 set "PYTHON_CMD=py -3.12"
)

if "%PYTHON_CMD%"=="" (
  where python >nul 2>nul
  if not errorlevel 1 (
    python -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
  )
)

if "%PYTHON_CMD%"=="" (
  echo Python 3.12 est introuvable. Installe Python 3.12 avant de continuer.
  echo https://www.python.org/downloads/
  exit /b 1
)

if exist env (
  env\Scripts\python.exe -c "import sys" >nul 2>nul
  if errorlevel 1 (
    echo Environnement env casse ou obsolete. Recreation...
    rmdir /s /q env
  )
)

if not exist env (
  %PYTHON_CMD% -m venv env
)

call env\Scripts\activate.bat
python -m pip install --upgrade pip
pip install torch==2.6.0+cu124 torchaudio==2.6.0+cu124 torchvision==0.21.0+cu124 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt

mkdir audio 2>nul
mkdir txt 2>nul
mkdir output 2>nul
mkdir profiles 2>nul

echo.
echo Installation terminee dans command\env.
echo Lance ensuite :
echo env\Scripts\activate
echo python main.py
