#!/usr/bin/env python
""" plot surface obs for specified domains
    from METAR data
    C. Martin - 7/2016
"""
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os
import datetime as dt

# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'Surface from METAR <path to metar files> <output dir>'
  sys.exit(1)

metardir = sys.argv[1]
RootPlotDir = sys.argv[2]

# plot directory
plotDir = RootPlotDir+'/surface'
if not os.path.exists(plotDir):
    os.makedirs(plotDir)

# get timestamp
timestamp = dt.datetime.utcnow()

domains = ['MD','CONUS']

for d in domains:
  if d == 'MD':
    m = Basemap(projection='merc',llcrnrlat=37.75,urcrnrlat=40,\
            llcrnrlon=-79.75,urcrnrlon=-74.75,resolution='h')
  else:
    m= Basemap(width=5200000, height=3600000, rsphere=(6371200.0,6371200.0),
            resolution='l',area_thresh=1000.,projection='lcc',
            lat_1=25,lat_2=25,lat_0=39.5,lon_0=-96)
  fig = plt.figure(figsize=(14,11))
  ax=fig.add_axes([0.03,0.1,0.94,0.8])
  m.drawcoastlines(color='red')
  m.drawcountries(color='red')
  m.drawstates(color='red')
  if d == 'MD':
   m.drawcounties(color='red')
  ax.annotate('Univ. of Maryland - Dept. of Atmos. & Oceanic. Sci.',
              xy=(-0.005,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='right',verticalalignment='bottom',
              color='Black',fontsize=12)
  ax.annotate('Trowal - UMD Weather - http://trowal.weather.umd.edu',
              xy=(1.01,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
              color='Black',fontsize=12)
  ax.annotate('Surface Obs. Generated: '+timestamp.strftime('%Y-%m-%d %H:%M'), xy=(0,1.0), xycoords=('axes fraction'), horizontalalignment='left',
              verticalalignment='bottom', color='black',fontsize=15)
  pos = ax.get_position()
  l, b, w, h = pos.bounds

  plt.savefig(plotDir+'/'+timestamp.strftime('%Y%m%d%H%M')+'_'+d+'.png')
  plt.close('all')
