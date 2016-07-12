#!/usr/bin/env python
"""
   MOSparse.py
   Orig: C. Martin - 6/2016
   Parse MOS file for echo to shell/file/PHP page
"""
import sys
import numpy as np

# command line arguments
if len(sys.argv) != 3:
  print "Ah ah ah, you didn't say the magic word...:"
  print "MOSparse.py <path to file> <Station ID>" 
  sys.exit(1)

filename = sys.argv[1]
station = sys.argv[2]

f = open(filename,'r')

MOS = f.read()

MOS = MOS.split('                                                                               ')
MOS = np.array(MOS)
stations = []
for m in MOS:
  stations.append(m[2:6])
#stations = MOS[2][2:6]
stations = np.array(stations)
arr_index = np.where(stations == station)

mymos = MOS[arr_index]
mymos = mymos.tolist()
print mymos
