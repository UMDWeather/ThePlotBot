#!/usr/bin/env python
# PlotBot.py
# C. Martin - 5/2016
# Watches directory to plot graphics in near real time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import subprocess

rootdir = '/home/ldm/data/HRRR/'

class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        # do something, eg. call your function to process the image
        sp = subprocess.Popen('python timeout.py hrrr '+event.src_path,cwd='/home/plotbot/plotbot/childbots',shell=True)

observer = Observer()
event_handler = ExampleHandler() # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path=rootdir)
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
