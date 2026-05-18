@echo off
setlocal
cd /d "%~dp0"

docker compose build
if errorlevel 1 (
  echo.
  echo Build Docker echoue.
  exit /b 1
)

echo.
echo Image Docker creee : paginavox:gpu
