#!/usr/bin/env python
# timeout.py
# C. Martin - 5/2016
# intermediate program to timeout subprocess
# from plotbot
import time
import sys
import subprocess
import os
import glob

# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'timeout.py <datatype> <dir>'
  sys.exit(1)

datatype = sys.argv[1]
datadir = sys.argv[2]

sp = subprocess.Popen('python plotbot_'+datatype+'_child.py '+datadir,cwd='/home/plotbot/plotbot/childbots',shell=True)
if datatype == 'hrrr':
  rootplotdir = '/var/www/html/ncep/hrrr/'
  plotscript = '/home/plotbot/grib2/HRRR/HRRR.py'
  outputdir = rootplotdir+datadir[19:]
  if not os.path.exists(outputdir):
    os.makedirs(outputdir)
  inputfile = glob.glob(datadir+'/*F000*')
  inputfile = inputfile[0]
  time.sleep(90)
  sp0 = subprocess.Popen('python %s %s %s'  % (plotscript,inputfile,outputdir),cwd='/home/plotbot/grib2/HRRR/',shell=True)
  timeout = time.time() + 60*60 # timeout in 60 mins
elif datatype == 'gfs':
  rootplotdir = '/var/www/html/ncep/gfs0p25/'
  plotscript = '/home/plotbot/grib2/GFS/gfs.pgrb2.0p25.py'
  outputdir = rootplotdir+datadir[19:]
  if not os.path.exists(outputdir):
    os.makedirs(outputdir)
  inputfile = glob.glob(datadir+'/*f000')
  inputfile = inputfile[0]
  time.sleep(60)
  sp0 = subprocess.Popen('python %s %s %s'  % (plotscript,inputfile,outputdir),cwd='/home/plotbot/grib2/GFS/',shell=True)
  timeout = time.time() + 60*60*6 # timeout in 6 hours
  
while True:
  if time.time() >= timeout:
    sp.kill()
    sys.exit(1)
