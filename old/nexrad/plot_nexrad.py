#!/usr/bin/env python
# plot_lwx.py
# plot lwx data on map
# C. Martin - 5/2016
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import datetime as dt
from metpy.io.nexrad import Level3File
import pyart


# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'plot_lwx.py <path to nexrad file> <output dir>'
  sys.exit(1)

filename = sys.argv[1]

f = Level3File(filename)
datadict = f.sym_block[0][0]
# Turn into an array, then mask
data = np.ma.array(datadict['data'])
data[data==0] = np.ma.masked

# Grab azimuths and calculate a range based on number of gates
az = np.array(datadict['start_az'] + [datadict['end_az'][-1]])
rng = np.linspace(0, f.max_range, data.shape[-1] + 1)

# Convert az,range to x,y
xlocs = rng * np.sin(np.deg2rad(az[:, np.newaxis]))
ylocs = rng * np.cos(np.deg2rad(az[:, np.newaxis]))

# Plot the data
#norm, cmap = ctables.registry.get_with_steps(ctable, 16, 16)

# create the plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.pcolormesh(xlocs, ylocs, data)
plt.savefig('out.png')
