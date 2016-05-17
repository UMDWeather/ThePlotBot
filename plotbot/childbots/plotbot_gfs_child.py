#!/usr/bin/env python
# PlotBot.py
# C. Martin - 5/2016
# Watches directory to plot graphics in near real time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import sys
import subprocess
import os

plotscript = '/home/plotbot/grib2/GFS/gfs.pgrb2.0p25.py'
rootplotdir = '/var/www/html/ncep/gfs0p25/'

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
	# plot GFS grib files
	outputdir = rootplotdir+sys.argv[1][19:]
	if not os.path.exists(outputdir):
    		os.makedirs(outputdir)
	time.sleep(60) # wait a minute to allow the LDM to downlaod the file fully
	sp = subprocess.Popen('python %s %s %s'  % (plotscript,event.src_path,outputdir),cwd='/home/plotbot/grib2/GFS/',shell=True)

observer = Observer()
event_handler = ExampleHandler() # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path=sys.argv[1])
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
