:start
date /t >  z:\%computername%_heartbeat.txt
time /t >> z:\%computername%_heartbeat.txt
timeout /t 5 >nul
goto start
