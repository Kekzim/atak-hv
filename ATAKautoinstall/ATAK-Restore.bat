@echo off
setlocal EnableDelayedExpansion

REM =====================================================
REM CONFIGURATION
REM =====================================================
set "ADB=C:\ATAKautoinstall\platform-tools\adb.exe"

set "TARGET_ROOT=/sdcard"
set "TARGET_DOWNLOAD=/sdcard/Download"

REM =====================================================
REM CHECK ADB
REM =====================================================
if not exist "%ADB%" (
    echo ERROR: adb.exe not found
    pause
    exit /b 1
)

cls
echo =====================================================
echo              DEVICE RESTORE TOOL
echo =====================================================
echo This will:
echo - Remove installed ATAK related apps
echo - Delete pushed folders/files
echo - Re-enable Android updates
echo -----------------------------------------------------
echo Make sure:
echo 1. Developer Mode enabled
echo 2. USB debugging enabled
echo 3. Devices unlocked
echo -----------------------------------------------------
pause

REM =====================================================
REM START ADB
REM =====================================================
"%ADB%" kill-server >nul 2>&1
"%ADB%" start-server >nul 2>&1

cls
echo Waiting for authorized devices...

:WAIT_FOR_AUTH
set "DEVICES="
set "BAD=0"

for /f "skip=1 tokens=1,2" %%A in ('"%ADB%" devices') do (
    if "%%B"=="device" (
        set DEVICES=!DEVICES! %%A
    ) else if not "%%A"=="" (
        set BAD=1
    )
)

if not defined DEVICES (
    timeout /t 5 >nul
    goto WAIT_FOR_AUTH
)

if "%BAD%"=="1" (
    echo Accept USB debugging on all devices.
    timeout /t 5 >nul
    goto WAIT_FOR_AUTH
)

echo ==============================
echo       DEVICES DETECTED
echo ==============================

set /a num=0
for %%D in (%DEVICES%) do (
    set /a num+=1
    echo !num!. %%D
)

echo ==============================
pause

REM =====================================================
REM PROCESS DEVICES
REM =====================================================
for %%D in (%DEVICES%) do (

    echo =========================================
    echo RESTORING DEVICE %%D
    echo =========================================

    set "LOG=restore_log_%%D.txt"
    echo Start: %date% %time% > "!LOG!"

REM =====================================================
REM UNINSTALL APPS (AUTO DETECT PACKAGE NAMES)
REM =====================================================
call :Progress "Removing installed apps" 20

REM --- ATAK ---
for /f "tokens=2 delims=:" %%P in ('"%ADB%" -s %%D shell pm list packages ^| findstr /i atak') do (
    "%ADB%" -s %%D uninstall %%P >> "!LOG!" 2>&1
)

REM --- ICU ---
for /f "tokens=2 delims=:" %%P in ('"%ADB%" -s %%D shell pm list packages ^| findstr /i icu') do (
    "%ADB%" -s %%D uninstall %%P >> "!LOG!" 2>&1
)

REM --- GEOCAM ---
for /f "tokens=2 delims=:" %%P in ('"%ADB%" -s %%D shell pm list packages ^| findstr /i geocam') do (
    "%ADB%" -s %%D uninstall %%P >> "!LOG!" 2>&1
)

REM --- REOLINK ---
for /f "tokens=2 delims=:" %%P in ('"%ADB%" -s %%D shell pm list packages ^| findstr /i reolink') do (
    "%ADB%" -s %%D uninstall %%P >> "!LOG!" 2>&1
)

REM --- SIGNAL ---
for /f "tokens=2 delims=:" %%P in ('"%ADB%" -s %%D shell pm list packages ^| findstr /i signal') do (
    "%ADB%" -s %%D uninstall %%P >> "!LOG!" 2>&1
)

REM --- OPENVPN ---
for /f "tokens=2 delims=:" %%P in ('"%ADB%" -s %%D shell pm list packages ^| findstr /i openvpn') do (
    "%ADB%" -s %%D uninstall %%P >> "!LOG!" 2>&1
)

call :Done

call :Done

REM =====================================================
REM DELETE PUSHED FILES
REM =====================================================
call :Progress "Deleting ATAK folders/files" 20

"%ADB%" -s %%D shell rm -rf %TARGET_ROOT%/atak >> "!LOG!" 2>&1
"%ADB%" -s %%D shell rm -rf %TARGET_ROOT%/ATAK-installation >> "!LOG!" 2>&1
"%ADB%" -s %%D shell rm -rf %TARGET_ROOT%/VPN-clients >> "!LOG!" 2>&1

"%ADB%" -s %%D shell rm -f %TARGET_DOWNLOAD%/atak-box.zip >> "!LOG!" 2>&1

call :Done

REM =====================================================
REM RE-ENABLE ANDROID UPDATES
REM =====================================================
call :Progress "Re-enabling Android updates" 20

"%ADB%" -s %%D shell settings put global auto_update_apps 1 >> "!LOG!"
"%ADB%" -s %%D shell settings put secure auto_update_apps 1 >> "!LOG!"

"%ADB%" -s %%D shell settings put global auto_update_system 1 >> "!LOG!"
"%ADB%" -s %%D shell settings put secure ota_disable_automatic_update 0 >> "!LOG!"
"%ADB%" -s %%D shell settings put global ota_disable_automatic_update 0 >> "!LOG!"

"%ADB%" -s %%D shell pm enable com.google.android.gms/.update.SystemUpdateActivity >> "!LOG!" 2>&1
"%ADB%" -s %%D shell pm enable com.google.android.gms/.update.SystemUpdateService >> "!LOG!" 2>&1

"%ADB%" -s %%D shell pm enable com.wssyncmldm >> "!LOG!" 2>&1
"%ADB%" -s %%D shell pm enable com.sec.android.soagent >> "!LOG!" 2>&1
"%ADB%" -s %%D shell pm enable com.miui.updater >> "!LOG!" 2>&1

"%ADB%" -s %%D shell settings put global package_verifier_enable 1 >> "!LOG!"
"%ADB%" -s %%D shell settings put global verifier_verify_adb_installs 1 >> "!LOG!"

call :Done

)

echo =========================================
echo ALL DEVICES RESTORED
echo =========================================
pause

"%ADB%" kill-server >nul 2>&1
taskkill /F /IM adb.exe >nul 2>&1
exit /b

REM =====================================================
REM PROGRESS FUNCTIONS
REM =====================================================

:progress
set "text=%~1"
set "bar="
set /a count=0
echo %text%
:progress_loop
set /a count+=1
set "bar=!bar!█"
<nul set /p="!bar!"
ping -n 1 localhost >nul
if !count! lss 25 goto progress_loop
echo.
exit /b

:done
echo [DONE]
exit /b