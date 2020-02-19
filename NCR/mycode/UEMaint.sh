#!/bin/bash

NOW=$(date +"%m-%d-%Y")
LOG="/opt/ncrue/logs/UEMaint_$NOW.log"
DATA_DIR="/opt/ncrue/data"
CACHE_DIR="/opt/ncrue/cache/download/data"

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

# clear and recreate data directory
  sudo rm -rf $DATA_DIR
  sudo mkdir $DATA_DIR

# clear and recreate cache/download/data directory
  sudo rm -rf $CACHE_DIR
  sudo mkdir $CACHE_DIR

# check and reset file permissions
  echo "`date`: Cleaning up file permissions" >> $LOG
  sudo /opt/ncrue/installation/perms.sh

  echo "`date`: starting NCRUEIOServer" >> $LOG
  sudo service NCRUEIOServer start
fi

echo "`date`: starting amsbroker" >> $LOG
sudo systemctl start amsbroker

