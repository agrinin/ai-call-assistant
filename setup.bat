@echo off
setlocal enabledelayedexpansion
echo ========================================
echo AI Call Assistant - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Building executable...
python build_exe.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo [3/4] Checking Windows Phone Link installation...
powershell -Command "$app = Get-AppxPackage -Name Microsoft.YourPhone; if ($app) { Write-Output 'INSTALLED' } else { Write-Output 'NOT_INSTALLED' }" > temp_check.txt
findstr /C:"INSTALLED" temp_check.txt >nul 2>&1
if errorlevel 1 (
    echo WARNING: Windows Phone Link (Your Phone) is not installed
    echo.
    echo Would you like to open Microsoft Store to install it? (Y/N)
    set /p install_choice=
    if /i "!install_choice!"=="Y" (
        echo Opening Microsoft Store...
        start ms-windows-store://pdp/?ProductId=9NMPJ99TJBHZ
        echo.
        echo Please install Phone Link from the Microsoft Store, then run this application.
    )
    del temp_check.txt
) else (
    echo Phone Link is already installed.
    del temp_check.txt
)

echo.
echo [4/4] Setup complete!
echo.
echo Executable created: dist\AI-Call-Assistant.exe
echo.
echo You can now run the application from the dist folder.
echo.
pause

