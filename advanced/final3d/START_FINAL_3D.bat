@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python bulunamadi. Python 3.10 veya daha yeni bir surum kurun.
  pause
  exit /b 1
)
echo Istanbul Adaptive Mobility Atlas aciliyor...
python server.py
pause
