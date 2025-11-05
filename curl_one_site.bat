@echo off
if "%~1"=="" (
    set loopcount=2000
) else (
    set loopcount=%~1
)

:loop

curl -v www.flipkart.com
timeout /t 5 /nobreak > NUL
set /a loopcount=loopcount-1
if %loopcount%==0 goto exitloop
goto loop
:exitloop
pause