#!/bin/sh
# run.sh
# navigate to this directory, then execute python script

PATH=/home/pi/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
export DISPLAY=:0.0
cd /home/pi/accord-display
sudo /home/pi/Envs/display/bin/python /home/pi/accord-display/display.py

