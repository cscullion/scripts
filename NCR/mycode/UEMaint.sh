#!/bin/bash

NOW=$(date +"%m-%d-%Y")
LOG="/opt/ncrue/logs/UEMaint_$NOW.log"

echo "`date`: stopping amsbroker" >> $LOG
sudo systemctl stop amsbroker
echo "`date`: stopping NCRUEIOServer" >> $LOG
sudo service NCRUEIOServer stop

pgrep UEIOServer && echo Running
result=$?

echo "exit code: ${result}"

if [ "${result}" -eq "0" ] ; then
  echo "`date`: NCRUEIOServer is still running - no cleanup performed" >> $LOG
else
  echo "`date`: NCRUEIOServer is not running, cleaning up data and attempting restart" >> $LOG
  echo "`date`: Cleaning data and cache directories" >> $LOG
  rm -rf /opt/ncrue/data/*
  rm -rf /opt/ncrue/cache/download/data/*
  echo "`date`: starting NCRUEIOServer" >> $LOG
  sudo service NCRUEIOServer start
fi

echo "`date`: starting amsbroker" >> $LOG
sudo systemctl start amsbroker

