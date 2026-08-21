@echo off
REM --- Configuration Variables ---
SET "ADB_PATH=c:\platform-tools\adb.exe"
REM If adb is not in your system PATH, change the above line to the full path, e.g., "C:\platform-tools\adb.exe"
SET "SOURCE_DIR=%CD%"

REM Target location for the specific files in the "Download" folder
SET "TARGET_DOWNLOAD=/storage/emulated/0/Download"
REM Target location for the "atak" folder at the root of internal storage
SET "TARGET_INTERNAL_ROOT=/storage/emulated/0"
REM -------------------------------

echo Connecting to Android device via ADB...
%ADB_PATH% devices
echo Ensure a device is listed above. Press any key to continue, or close this window to troubleshoot.
pause

REM Create necessary directories on the phone (e.g. the ATAK installation folder within Download)
echo Creating required directories on the phone...
%ADB_PATH% shell mkdir -p "%TARGET_DOWNLOAD%/ATAK-installation"
%ADB_PATH% shell mkdir -p "%TARGET_INTERNAL_ROOT%/atak"

REM Install the 3 applications (using -r for replace if they exist, -g to grant permissions automatically)
echo Installing App 1/3...
%ADB_PATH% install -r -g "C:\Users\wintakadm\Videos\USB-stickan\1.apk"
echo Installing App 2/3...
%ADB_PATH% install -r -g "C:\Users\wintakadm\Videos\USB-stickan\2.apk"
echo Installing App 3/3...
%ADB_PATH% install -r -g "C:\Users\wintakadm\Videos\USB-stickan\3.apk"

REM Push specific files to the "Download" folder location
echo Pushing atak-box.zip to %TARGET_DOWNLOAD%/...
%ADB_PATH% push "C:\Users\wintakadm\Videos\USB-stickan\atak-box.zip" "%TARGET_DOWNLOAD%/"

echo Pushing ATAK-installation folder to %TARGET_DOWNLOAD%/...
%ADB_PATH% push "C:\Users\wintakadm\Videos\USB-stickan\ATAK-installation" "%TARGET_DOWNLOAD%/"

REM Push the 'atak' folder to the internal storage root (/storage/emulated/0/)
echo Pushing 'atak' folder to internal storage root %TARGET_INTERNAL_ROOT%/...
%ADB_PATH% push "C:\Users\wintakadm\Videos\USB-stickan\atak" "%TARGET_INTERNAL_ROOT%/"

echo All installations and file transfers complete.
pause

