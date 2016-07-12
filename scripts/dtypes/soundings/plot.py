#!/usr/bin/env python
""" Soundings
    Read ASCII radiosonde data in WMO format from LDM
    and plot it on a Skew-T
    C. Martin - 7/2016
"""
import sys

# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'Soundings <path to upper air file> <output dir>'
  sys.exit(1)

filename = sys.argv[1]
RootPlotDir = sys.argv[2]


