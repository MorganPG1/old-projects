echo off
cls
color 47
echo A critical system error has occoured, this error is not as common but it should be fixed by a reboot.
echo.
echo Last program: %lastprog%
echo.
echo Error code: KERNEL_ERROR
timeout /t 5 /nobreak>nul
load