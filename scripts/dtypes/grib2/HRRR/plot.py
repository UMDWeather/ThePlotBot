#!/usr/bin/env python
""" HRRR.py
    C. Martin - 5/2016
    plot HRRR output
    from GRIB2 files from LDM
"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from glob import glob
import sys
import datetime as dt
import importlib
import pygrib
import os
import time

time.sleep(120) # wait two minutes for GRIB2 file to fully populate

# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'HRRR.py <path to grib file> <output dir>'
  sys.exit(1)

filename = sys.argv[1]
rootplotdir = sys.argv[2]
filepath = filename.split('/')
gribfile = filepath[-1]
inittime = filepath[6]
timestep = gribfile[14:-6]

plotDir = rootplotdir+filepath[4]+'/'+filepath[5]+'/'+inittime
if not os.path.exists(plotDir):
    os.makedirs(plotDir)

inittime = dt.datetime.strptime(inittime,"%Y%m%d%H%M")
validtime = inittime + dt.timedelta(hours=float(timestep))

domains = ['CONUS','MidAtl']
pltenv={}

# load in all the plotting plugins
plugins=[]
for p in glob('/home/plotbot/scripts/dtypes/grib2/HRRR/plot_plugins/[a-zA-Z]*py'):
  md='plot_plugins.'+p.split('/')[-1].split('.')[0]
  plugins.append(importlib.import_module(md))

hrrr = pygrib.open(filename)

grb = hrrr.read(1)[0]
lats, lons = grb.latlons()

for d in domains:
  if d == 'MidAtl':
    m= Basemap(width=1200000, height=800000, rsphere=(6378137.00,6356752.3142),
            resolution='h',area_thresh=1000.,projection='lcc',
            lat_1=39,lat_2=39,lat_0=39,lon_0=-77.5)
  else:
    m= Basemap(width=4900000, height=3150000, rsphere=(6378137.00,6356752.3142),
            resolution='l',area_thresh=1000.,projection='lcc',
            lat_1=39.5,lat_2=39.5,lat_0=38.5,lon_0=-97)

  x,y = m(lons,lats)
  pltenv['map'] = m
  pltenv['x'] = x
  pltenv['y'] = y

  for p in plugins:
    fig = plt.figure(figsize=(14,11))
    ax=fig.add_axes([0.03,0.1,0.94,0.8])
    pltenv['ax']=ax
    #annotations, boundaries, etc
    ax.annotate('init:  '+inittime.strftime('%Y-%m-%d %HZ'),xy=(1,1.03),fontsize=9,
              xycoords="axes fraction", horizontalalignment='right')
    ax.annotate('valid: '+validtime.strftime('%Y-%m-%d %HZ'),xy=(1,1.01),fontsize=9,
              xycoords="axes fraction", horizontalalignment='right')
    ax.annotate('University of Maryland Dept. of Atmospheric and Oceanic Science',
              xy=(1.01,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
              color='gray',fontsize=8)
    ax.annotate('High Resolution Rapid Refresh (HRRR)', xy=(0,1.01), xycoords=('axes fraction'), horizontalalignment='left',
              verticalalignment='bottom', color='red')
    # map boundaries
    pltenv['map'].drawcoastlines(color= p.boundaryColor)
    pltenv['map'].drawcountries(color=p.boundaryColor)
    pltenv['map'].drawstates(color=p.boundaryColor)
    
    plt.title(p.title,fontweight='bold')

    p.plot(hrrr, pltenv)
    
    #colorbar
    #TODO, move this to sub routines
    pos = ax.get_position()
    l, b, w, h = pos.bounds
    ch = 0.015
    cw = 0.8
    cax=plt.axes([l + w*(1-cw)/2,b-ch-0.005,w*cw,ch])
    cb = plt.colorbar(cax=cax, orientation='horizontal')
    cb.set_label(p.cbarlabel)

    # save the figures
    plt.savefig(plotDir+'/{0}_F{1}_{2}.png'.format(p.filename,timestep,d))
    plt.close('all')