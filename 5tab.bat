@echo off
setlocal enabledelayedexpansion

:: Define websites
set site1=https://www.nytimes.com
set site2=https://www.cnn.com
set site3=https://www.bbc.com
set site4=https://www.imdb.com
set site5=https://www.pinterest.com


:: Loop through and open each site
for /L %%i in (1,1,5) do (
    call set url=%%site%%i%%
    start msedge !url!
    timeout /t 1 >nul
)

timeout /t 15 1>nul


endlocal
exit