#!/bin/bash
# run the GFS/NAM4km grid interpolation
# text product output scripts
# every six hours on a cronjob
# C. Martin - 9/2016

cd /home/plotbot/scripts/text/GridInterp

python GFS.py

