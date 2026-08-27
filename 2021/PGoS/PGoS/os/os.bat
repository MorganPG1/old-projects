echo off
set lastprog=PGoS
:os
cls

echo Booting Mogi os
echo Details - Non-Modified
timeout /t 3 /nobreak>nul
:done 
cls
echo Done
echo Type the name of a program (without .bat) to run it
set /p prog=
set lastprog=%prog%
os\apps\%prog%.bat
goto done
