echo off
:Main
color 04
cls

echo  PG Official BIOS Flasher tool
echo.
echo Before you use:
echo.
echo DO NOT Close os while flashing
echo Make sure all files are in the /flash folder in the app folder
echo All files required are. (bios.bat, binfo.bat)
echo.
echo How to use:
echo.
echo Copy all files required to /os/apps/flash or where the os and apps are located
echo Type Y below if you want to flash N if not.
echo.
set /p yn=
if %yn% equ Y goto flash
if %yn% equ N os\os.bat
if %yn% equ y goto flash
if %yn% equ n os/os.bat
if %yn% neq Y goto Main
if %yn% neq N goto Main
if %yn% neq y goto Main
if %yn% neq n goto Main
:flash
echo Flashing files...
timeout /t 3 /nobreak>nul

copy /y bios\bios.bat os\apps\flash\bios.bak>nul
copy /y bios\binfo.bat os\apps\flash\binfo.bak>nul
copy /y os\apps\flash\bios.bat bios\bios.bat > bios/flashlg1.txt
copy /y os\apps\flash\binfo.bat bios\binfo.bat > bios/flashlg2.txt

echo Rebooting...
timeout /t 3 /nobreak>nul
Load