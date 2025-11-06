@echo off
setlocal enabledelayedexpansion

:: Define websites
set site1=https://www.gate.com
set site2=https://ufile.io
set site3=https://filedrop.io
set site4=https://www.twitter.com
set site5=https://www.imdb.com
set site6=https://www.reddit.com
set site7=https://www.linkedin.com
set site8=https://www.netflix.com
set site9=https://www.ebay.com
set site10=https://www.elle.com/
set site11=https://www.viator.com
set site12=https://www.klook.com
set site13=https://xmind.com
set site14=https://hackr.io
set site15=https://poki.com
set site16=https://www.wikipedia.org
set site17=https://crazygames.com
set site18=https://www.cnn.com
set site19=https://www.bbc.com
set site20=https://www.nhk.or.jp
set site21=https://www.pinterest.com
set site22=https://www.quora.com
set site23=https://www.stackoverflow.com
set site24=https://www.dropbox.com
set site25=https://www.spotify.com
set site26=https://www.airbnb.com
set site27=https://www.booking.com
set site28=https://www.medium.com
set site29=https://www.tumblr.com
set site30=https://www.paypal.com


:: Loop through and open each site
for /L %%i in (1,1,30) do (
    call set url=%%site%%i%%
    start msedge !url!
    timeout /t 1 >nul
)

endlocal
exit