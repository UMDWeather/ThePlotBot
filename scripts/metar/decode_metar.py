#!/usr/bin/env python
""" Decode Metar
      C. Martin - 7/2016
      Decode METAR code and output met obs.
"""
import sys

metarin = sys.stdin.read()

if metarin[0:5] == 'METAR':
  metarin = metarin[6:]

# split up message
metarin = metarin.strip('\n')
metarin = metarin.replace('\n','')
code = metarin.split(' ')
code = filter(None,code)

# first part is station name
station = code[0]
# then the timestamp
timestamp = code[1]
day = timestamp[0:2]
time = timestamp[2:6]
# sometimes it specifies if it's auto or corrected
if code[2] == 'AUTO' or 'COR':
  del code[2]
# next is wind
wind = code[2].split('G')
if len(wind) == 1:
  wind = wind[0]
  wind = wind.replace('KT','')
  wspd = wind[0:2]
  wdir = wind[2:]
  gust = 'N/A'
else:
  gust = wind[1]
  wind = wind[0]
  wspd = wind[0:2]
  wdir = wind[2:]
  gust = gust.replace('KT','')
# variable winds?
if 'V' in code[3]:
  wvar = code[3].split('V')
  del code[3]
else:
  wvar = 'N/A'
# visibility
vis = code[3]
# we're 'Muricans for now so we only care about K*** stations
# they report in statute miles
# MEH, for now ignore this var other than repeat it

print code
print station,day,time,wdir,wspd,gust,wvar,vis
