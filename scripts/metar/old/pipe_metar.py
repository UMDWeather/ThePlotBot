#!/usr/bin/env python
""" pipe_metar.py
      C. Martin - 7/2016
      Feed METAR information from LDM via UNIX PIPE
      and this program will extract info
      and output to new file
"""
import sys
import datetime as dt
import os

datadir = '/home/ldm/data/text/metar/'
now = dt.datetime.utcnow() # get directory from date
outdir = datadir+now.strftime('%Y%m%d')
if not os.path.exists(outdir):
    os.makedirs(outdir)

metarin = sys.stdin.read() # read in PIPEd input from stdin

#f = open('/home/plotbot/scripts/metar/stations.txt','r')
#fin = f.readlines()
#stations = [fin[a][20:25] for a in range(len(fin))]

records = metarin.split('=') # records end with equals sign
records = [records[a].strip() for a in range(len(records))] # remove extra newline chars

hour = now.strftime('%Y%m%d%H')
f = open(outdir+'/'+hour,'a')

for a in range(len(records)):
  try:
    if records[a][0].isdigit():
       pass
       #records[a] = records[a][30:] # remove all the crap at the beginning
    else: 
      pass
  except:
    pass
for record in records:
  record2 = record.split('\n')
  for re2 in record2:
    if re2[0].isdigit():
      pass
    elif re2 == 'METAR':
      pass
    elif re2[0] == 'S':
      pass
    else:
      print re2
      f.write(re2+'=\n')

f.close()
