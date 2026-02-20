@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

title ThreadPilot Quick Start

set "INSTALL_ONLY=0"
if /I "%~1"=="--install-only" set "INSTALL_ONLY=1"

echo =====================================================
echo ThreadPilot Quick Start
echo =====================================================
echo.

if exist "dist\threadpilot.exe" (
  echo [1/3] EXE detected: dist\threadpilot.exe
  if "%INSTALL_ONLY%"=="1" (
    echo Install-only mode: skip launching UI.
    exit /b 0
  )
  echo [2/3] Starting beginner UI...
  "dist\threadpilot.exe" ui
  goto :eof
)

echo EXE not found. Switching to Python mode.

set "PYTHON_CMD="
where py >nul 2>nul
if %ERRORLEVEL%==0 set "PYTHON_CMD=py"
if not defined PYTHON_CMD (
  where python >nul 2>nul
  if %ERRORLEVEL%==0 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  echo [ERROR] Python is not installed or not in PATH.
  echo Please install Python 3.10+ and re-run this script.
  pause
  exit /b 1
)

echo [1/3] Preparing virtual environment...
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

echo [2/3] Installing default dependencies...
python -m pip install --upgrade pip
if errorlevel 1 (
  echo [ERROR] Failed to upgrade pip.
  pause
  exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Failed to install requirements.
  pause
  exit /b 1
)

if "%INSTALL_ONLY%"=="1" (
  echo [3/3] Install-only mode complete.
  exit /b 0
)

echo [3/3] Launching beginner UI...
python -m threadpilot.main ui
