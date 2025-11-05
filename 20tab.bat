@echo off
setlocal enabledelayedexpansion

:: Define websites
set site1=https://www.amazon.com
set site2=https://www.facebook.com
set site3=https://www.youtube.com
set site4=https://www.twitter.com
set site5=https://www.instagram.com
set site6=https://www.reddit.com
set site7=https://www.linkedin.com
set site8=https://www.netflix.com
set site9=https://www.ebay.com
set site10=https://www.twitch.tv
set site11=https://www.microsoft.com
set site12=https://www.apple.com
set site13=https://www.google.com
set site14=https://www.yahoo.com
set site15=https://www.bing.com
set site16=https://www.wikipedia.org
set site17=https://www.nytimes.com
set site18=https://www.cnn.com
set site19=https://www.bbc.com
set site20=https://www.imdb.com


:: Loop through and open each site
for /L %%i in (1,1,20) do (
    call set url=%%site%%i%%
    start msedge !url!
    timeout /t 1 >nul
)

endlocal
exit