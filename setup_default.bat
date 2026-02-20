@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

title ThreadPilot Default Setup

set "INSTALL_ONLY=0"
if /I "%~1"=="--install-only" set "INSTALL_ONLY=1"

echo =====================================================
echo ThreadPilot Default Setup
echo =====================================================
echo This script installs everything needed by default:
echo - Python venv (.venv)
echo - pip upgrade
echo - app dependencies (requirements.txt)
echo - PyInstaller
echo - EXE build (dist\threadpilot.exe)
echo.

set "PYTHON_CMD="
where py >nul 2>nul
if %ERRORLEVEL%==0 set "PYTHON_CMD=py"
if not defined PYTHON_CMD (
  where python >nul 2>nul
  if %ERRORLEVEL%==0 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  echo [ERROR] Python is not installed or not in PATH.
  echo Install Python 3.10+ first.
  pause
  exit /b 1
)

echo [1/7] Creating virtual environment...
if not exist ".venv\Scripts\python.exe" (
  %PYTHON_CMD% -m venv .venv
  if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] Failed to activate virtual environment.
  pause
  exit /b 1
)

echo [2/7] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
  echo [ERROR] pip upgrade failed.
  pause
  exit /b 1
)

echo [3/7] Installing app dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] requirements install failed.
  pause
  exit /b 1
)

echo [4/7] Installing pyinstaller...
python -m pip install pyinstaller
if errorlevel 1 (
  echo [ERROR] pyinstaller install failed.
  pause
  exit /b 1
)

echo [5/7] Preparing build output...
if exist "dist\threadpilot.exe" (
  taskkill /F /IM threadpilot.exe >nul 2>nul
  timeout /t 1 >nul
  del /F /Q "dist\threadpilot.exe" >nul 2>nul
)

echo [6/7] Building EXE...
pyinstaller --noconfirm --clean --onefile --name threadpilot --add-data "threadpilot/src/ui/main.html;threadpilot/src/ui" threadpilot/main.py
if errorlevel 1 (
  echo [ERROR] EXE build failed.
  pause
  exit /b 1
)

echo [7/7] Setup complete.
echo EXE path: dist\threadpilot.exe

if "%INSTALL_ONLY%"=="1" (
  echo Install-only mode complete.
  exit /b 0
)

echo Launching UI with EXE...
"dist\threadpilot.exe" ui
