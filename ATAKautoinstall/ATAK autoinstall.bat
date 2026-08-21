@echo off
setlocal EnableDelayedExpansion

REM =====================================================
REM CONFIGURATION
REM =====================================================
set "ADB=C:\ATAKautoinstall\platform-tools\adb.exe"

REM Apps installed from Google Play by the user (NOT sideloaded):
REM   ATAK  - must be installed BEFORE running this script
REM   OpenVPN, Geocam, Signal, Reolink, FileManager

set "APK1=C:\ATAKautoinstall\Filer\Ramsor.apk"
set "APK2=C:\ATAKautoinstall\Filer\HVreports.apk"
set "APK3=C:\ATAKautoinstall\Filer\Icu.apk"
set "APK4=C:\ATAKautoinstall\Filer\ATAK-Sync.apk"


set "ATAK_BOX=C:\ATAKautoinstall\Filer\ATAK-installation\atak-box.zip"
set "ATAK_INSTALL=C:\ATAKautoinstall\Filer\ATAK-installation"
set "ATAK_FOLDER=C:\ATAKautoinstall\Filer\atak"
set "VPN_FOLDER=C:\ATAKautoinstall\Filer\VPN-clients"

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
echo              MANUAL USB ACCESS REQUIRED
echo	             Make sure all below are set!
echo	    If installation manual is followed all is set!
echo =====================================================
echo 1. INSTALL ATAK FROM GOOGLE PLAY ON ALL DEVICES FIRST
echo    The ATAK-Sync plugin and the pushed config require it
echo    to already be installed. This script does NOT install ATAK.
echo 2. Install OpenVPN and Geocam from Google Play
echo 3. Enable Developer Mode + USB Debugging
echo 4. Connect devices via USB
echo 5. Make sure Screen is unlocked on ALL devices
echo 6. ACCEPT USB debugging if Prompted
echo 7. Select FILE TRANSFER (MTP) if prompted
echo 8. Allow file access if prompted
echo -----------------------------------------------------
echo When above is done Press ANY KEY
Pause
echo =====================================================
echo This takes ~5sek
echo Check yor device again for USB-debugging if promted
echo =====================================================
echo =====================================================


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

REM echo Devices ready: %DEVICES%
REM pause
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
    echo PROCESSING DEVICE %%D
    echo =========================================

    set "LOG=log_%%D.txt"
    echo Start: %date% %time% > "!LOG!"

    REM Keep screen awake
    "%ADB%" -s %%D shell svc power stayon true >nul 2>&1

    REM =====================================================
    REM DISABLE ANDROID & APP UPDATES (MAX LOCKDOWN)
    REM =====================================================
    call :Progress "Disabling Updates" 30

    REM Disable Play auto updates
    "%ADB%" -s %%D shell settings put global auto_update_apps 0 >> "!LOG!"
    "%ADB%" -s %%D shell settings put secure auto_update_apps 0 >> "!LOG!"

    REM Disable OTA flags
    "%ADB%" -s %%D shell settings put global auto_update_system 0 >> "!LOG!"
    "%ADB%" -s %%D shell settings put secure ota_disable_automatic_update 1 >> "!LOG!"
    "%ADB%" -s %%D shell settings put global ota_disable_automatic_update 1 >> "!LOG!"

    REM Disable Google OTA components
    "%ADB%" -s %%D shell pm disable-user --user 0 com.google.android.gms/.update.SystemUpdateActivity >> "!LOG!" 2>&1
    "%ADB%" -s %%D shell pm disable-user --user 0 com.google.android.gms/.update.SystemUpdateService >> "!LOG!" 2>&1

    REM Disable manufacturer OTA (Samsung etc)
    "%ADB%" -s %%D shell pm disable-user --user 0 com.wssyncmldm >> "!LOG!" 2>&1
    "%ADB%" -s %%D shell pm disable-user --user 0 com.sec.android.soagent >> "!LOG!" 2>&1
    "%ADB%" -s %%D shell pm disable-user --user 0 com.miui.updater >> "!LOG!" 2>&1

    REM Disable Play Store (FULL BLOCK)
  REM  "%ADB%" -s %%D shell pm disable-user --user 0 com.android.vending >> "!LOG!" 2>&1

    REM Disable package verifier
    "%ADB%" -s %%D shell settings put global package_verifier_enable 0 >> "!LOG!"
    "%ADB%" -s %%D shell settings put global verifier_verify_adb_installs 0 >> "!LOG!"

    call :Done

    REM =====================================================
    REM CREATE FOLDERS
    REM =====================================================
    call :Progress "Creating folders" 15
    "%ADB%" -s %%D shell mkdir -p %TARGET_ROOT%/atak >> "!LOG!"
    "%ADB%" -s %%D shell mkdir -p %TARGET_ROOT%/ATAK-installation >> "!LOG!"
    "%ADB%" -s %%D shell mkdir -p %TARGET_ROOT%/VPN-clients >> "!LOG!"
    call :Done

    REM =====================================================
    REM INSTALL APKS
    REM =====================================================
    for %%A in ("%APK1%" "%APK2%" "%APK3%" "%APK4%") do (
        call :Progress "Installing %%~nA" 15
        "%ADB%" -s %%D install -r -g %%A >> "!LOG!"
        call :Done
    )

REM =====================================================
REM PUSH FILES
REM =====================================================

REM Push folders (NOT atak-box.zip)
for %%F in ("%ATAK_INSTALL%" "%ATAK_FOLDER%" "%VPN_FOLDER%") do (
    call :Progress "Pushing %%~nF" 15
    "%ADB%" -s %%D push %%F "%TARGET_ROOT%/" >> "!LOG!"
    call :Done
)

REM Push atak-box.zip ONLY to Download folder
call :Progress "Pushing atak-box.zip to Download" 15
"%ADB%" -s %%D push "%ATAK_BOX%" "%TARGET_DOWNLOAD%/" >> "!LOG!"
call :Done


REM =====================================================
REM DELETE OLD ATAK BOX FROM ATAK-INSTALLATION
REM =====================================================
call :Progress "Cleaning old atak-box.zip" 10
"%ADB%" -s %%D shell rm -f %TARGET_ROOT%/ATAK-installation/atak-box.zip >> "!LOG!" 2>&1
call :Done
)

echo =========================================
echo ALL DEVICES COMPLETED SUCCESSFULLY
echo =========================================
pause

"%ADB%" kill-server >nul 2>&1
taskkill /F /IM adb.exe >nul 2>&1
exit /b

REM =====================================================
REM PROGRESS FUNCTIONS
REM =====================================================
REM :Progress
REM echo %~1
REM set /a i=0
REM :loop
REM set /a i+=1
REM <nul set /p=█
REM ping -n 1 localhost >nul
REM if %i% LSS %~2 goto loop
REM echo.
REM exit /b


REM :Done
REM echo [DONE]
REM exit /b


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