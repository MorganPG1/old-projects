:start
color 67
echo off
cls
echo Mogi Os Testing Vm
echo --For Testing Features of mogi os--
echo Enter A App Or Command
echo.
set /p cmd=
if %cmd% equ crash4fun crashscreen
if %cmd% neq crash4fun goto start