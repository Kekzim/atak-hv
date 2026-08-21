@echo off
REM Launcher for atak_provision.py on Windows.
REM Double-click to run an install, or call from cmd with arguments:
REM     atak-provision.bat devices
REM     atak-provision.bat restore --wipe-media

setlocal
set "SCRIPT=%~dp0atak_provision.py"

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY (
    where python >nul 2>&1 && set "PY=python"
)

if not defined PY (
    echo =====================================================
    echo  Python 3.11 or newer is required but was not found.
    echo =====================================================
    echo.
    echo  Install it from https://www.python.org/downloads/
    echo  Tick "Add python.exe to PATH" in the installer.
    echo.
    pause
    exit /b 1
)

if "%~1"=="" (
    %PY% "%SCRIPT%" install
) else (
    %PY% "%SCRIPT%" %*
)

set "RC=%ERRORLEVEL%"
echo.
if not "%RC%"=="0" echo Finished with errors (exit code %RC%). See the logs folder.
pause
exit /b %RC%
