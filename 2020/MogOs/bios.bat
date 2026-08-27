:start
color 07
echo off
cls
echo MogiOs Test Bios
echo Internal Or External Bootloader?
set /p int=
if %int% equ internal goto int
if %int% equ internel goto int
if %int% equ external goto ext
if %int% equ externel goto ext
if %int% neq internal goto start
:int
bootload
color 47
cls
echo Bootloader Not Found!
pause
bios
:ext
echo Drive Letter? example "a"
set /p drv=
%drv%:
cls
echo directory? example "bootload" or "bootload\mogos
set /p dir=
cd %dir%
bootload
cls
color 47
cls
echo Bootloader Not Found!
pause
bios