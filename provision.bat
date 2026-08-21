@echo off
REM Launcher for provision.py on Windows.
REM Double-click to run an install, or call from cmd with arguments:
REM     provision.bat devices
REM     provision.bat restore --wipe-media

setlocal
set "SCRIPT=%~dp0provision.py"

REM --- find a Python 3.11+ interpreter -------------------------------
set "PY="
for %%C in ("py -3" "python" "python3") do (
    if not defined PY (
        %%~C -c "import sys; sys.exit(0 if sys.version_info>=(3,11) else 1)" >nul 2>&1
        if not errorlevel 1 set "PY=%%~C"
    )
)

if not defined PY (
    echo =====================================================
    echo   Python 3.11 or newer is required, and was not found.
    echo =====================================================
    echo.
    echo   This tool needs Python to run. Install it from:
    echo     https://www.python.org/downloads/
    echo.
    echo   IMPORTANT: tick "Add python.exe to PATH" in the
    echo   installer, then open a new window and try again.
    echo.
    echo   (If Python is already installed it may be an older
    echo    version - this tool needs 3.11 or newer.)
    echo.
    pause
    exit /b 1
)

REM --- run -----------------------------------------------------------
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
