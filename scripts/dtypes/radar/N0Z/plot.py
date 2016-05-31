#!/usr/bin/env python
""" N0Z plot
    plot nexrad base reflectivity
    C. Martin - 5/2016
"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import datetime as dt
from metpy.io.nexrad import Level3File
import pyart
import os

# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'plot N0Z <path to nexrad file> <output dir>'
  sys.exit(1)

filename = sys.argv[1]
RootPlotDir = sys.argv[2]
radfile = filename.split('/')
site = radfile[5]
dtype = radfile[6]
nexradf = radfile[7]
filesplit = nexradf.split('_')
today = dt.datetime.utcnow()
yyyymm = today.strftime('%Y%m')
timestamp = filesplit[3]
timestamp = dt.datetime.strptime(yyyymm+timestamp,"%Y%m%d%H%M")

# plot dir
plotDir = RootPlotDir+'/radar/'+site+'/'+timestamp.strftime('%Y%m%d')
if not os.path.exists(plotDir):
    os.makedirs(plotDir)

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

# convert to lat lon (probably not accurate but a good first guess)
lwxlat = 38.976244
lwxlon = -77.487429

xlocs = lwxlon + xlocs/111.
ylocs = lwxlat + ylocs/111.



# Plot the data
#norm, cmap = ctables.registry.get_with_steps(ctable, 16, 16)

# create the plot
fig = plt.figure()
ax = fig.add_subplot(111)

# set up map
m= Basemap(llcrnrlon=-80,llcrnrlat=37,urcrnrlon=-75,urcrnrlat=40, rsphere=(6371200.0,6371200.0),
            resolution='h',area_thresh=1000.,projection='lcc',
            lat_1=25,lat_2=25,lat_0=39.5,lon_0=-95)
xm, ym = m(xlocs,ylocs)
m.pcolormesh(xm, ym, data)
m.drawcoastlines(color='black')
m.drawcountries(color='black')
m.drawcounties(color='black')
m.drawstates(color='black')


plt.savefig(plotDir+'/'+timestamp.strftime('%Y%m%d_%H%M')+'_'+dtype+'.png',bbox_inches='tight',pad_inches=0)
