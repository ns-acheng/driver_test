@echo off
setlocal enabledelayedexpansion

rem set "TTD_LOG=C:\tmp\stagentsvc_trace.run"

FOR /L %%i IN (1,1,200) DO (
    echo Iteration %%i of 200 =========
    set "PID="

    echo start client service
    sc start stagentsvc

    echo Sleeping for 30 sec
    timeout /t 30 /nobreak >nul

    rem Step 1: Find PID of stagentsvc
    for /f "tokens=2 delims=," %%a in ('tasklist /svc /fo csv ^| findstr /i "stagentsvc"') do (
        set "PID=%%~a"
    )
    
    if not defined PID (
        echo stagentsvc not found.
        exit /b 1
    )
    
    echo Service PID is: %PID%

    del /F /Q "C:\tmp\*" 
    rem  start "" "TTD.exe" -attach %PID% -out "%TTD_LOG%" -noUI -accepteula

    start 10tab.bat
    echo ping and CURL
    ping www.careweb.nl
    ping www.amazon.com
    curl -v www.tripadvisor.com/Restaurants-g293913-zfp10954-Taipei.html
	curl -v smallpdf.com
    
    rem Calculate range size
	set "max=100"
	set "min=30"
	set /a range=max - min + 1
	set /a rand=%RANDOM% %% range + min
	echo wait for %rand% sec
    timeout /t %rand% /nobreak 

    echo Stopping stagentsvc...
    sc stop stagentsvc
    timeout /t 3 /nobreak 
    taskkill /f /im msedge.exe


    rem  Check for .dmp file
    echo Checking for dump files...
    dir "C:\_dump\stAgentSvc.exe\*.dmp" /b >nul 2>&1
    if not errorlevel 1 (
        echo Dump file found. Exiting loop.
        echo Dump in iteration %%i >> C:\_dump\note.txt
        exit /b 1
    )
    dir "C:\ProgramData\netskope\stagent\logs\*.dmp" /b >nul 2>&1
    if not errorlevel 1 (
        echo Dump file found in logs folder. Exiting loop.
        echo Dump in iteration %%i >> C:\_dump\note.txt
        exit /b 1
    )
	
	echo Iteration %%i ends =====================
)

:done
echo All iterations complete.

ENDLOCAL
pause