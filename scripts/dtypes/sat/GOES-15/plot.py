#!/usr/bin/env python
""" GOES-15
    C. Martin - 7/2016
    convert satellite data in GINI format to PNG graphic
"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import datetime as dt
from metpy.io.gini import GiniFile
import os

# command line arguments
if len(sys.argv) != 3:
  print 'wrong usage:'
  print 'GOES-15.py <path to gini file> <output dir>'
  sys.exit(1)

filename = sys.argv[1]
RootPlotDir = sys.argv[2]

# filename format
# /home/ldm/data/sat/20160516/20/GOES-13/2045Z_VIS_1km_EAST-CONUS-TIGE01_KNES_70082.satz.2016051620
# get info based off filename
satfile = filename.split('/')
date = satfile[5]
hour = satfile[6]
sat = satfile[7]
ginifile = satfile[8]
filesplit = ginifile.split('_')
timestamp = filesplit[0]
timestamp = dt.datetime.strptime(date+timestamp,"%Y%m%d%H%MZ")
dtype = filesplit[1]
res = filesplit[2]
domain = filesplit[3]
goodlist = ['WEST-CONUS-TIGW01','WEST-CONUS-TIGW05','WEST-CONUS-TIGW02','WEST-CONUS-TIGW04','WEST-CONUS-TIGW06']

if domain not in goodlist:
  sys.exit()

# plot directory
plotDir = RootPlotDir+'/sat/'+sat
if not os.path.exists(plotDir):
    os.makedirs(plotDir)

# read in the satellite data
gini = GiniFile(filename)
gini_ds = gini.to_dataset()

var = {'IR':'IR','VIS':'Visible','WV':'WV','13.3':'IR','3.9':'IR'}
cbarlabels = {'Visible':'Brightness','IR':'IDK','WV':'IDK'}
title = {'IR':'Infrared','VIS':'Visible','WV':'Water Vapor','13.3':'13.3 micron IR','3.9':'3.9 micron IR'}

cbarlabel = cbarlabels[var[dtype]]

x = gini_ds.variables['x'][:]
y = gini_ds.variables['y'][:]
lons = gini_ds.variables['lon'][:]
lats = gini_ds.variables['lat'][:]

data_var = gini_ds.variables[var[dtype]]
proj_var = gini_ds.variables[data_var.grid_mapping]

# get variables from file
stdpar = proj_var.standard_parallel
longcent = proj_var.longitude_of_central_meridian
latcent = proj_var.latitude_of_projection_origin
earthrad = proj_var.earth_radius
latS = lats[0,0]; latN = lats[-1,-1]
lonW = lons[0,0]; lonE = lons[-1,-1]

"""
<class 'metpy.io.cdm.Variable'>: int32 Lambert_Conformal()
	grid_mapping_name: lambert_conformal_conic
	standard_parallel: 25.0
	longitude_of_central_meridian: -95.0
	latitude_of_projection_origin: 25.0
	earth_radius: 6371200.0
"""

# set up the map projection(s)
domains = ['00','01','02']
for d in domains:
  if d == '01': # conus-ish
      m= Basemap(llcrnrlon=-130,llcrnrlat=22,urcrnrlon=-95,urcrnrlat=50, rsphere=(earthrad,earthrad),
            resolution='l',area_thresh=1000.,projection='lcc',
            lat_1=stdpar,lat_2=stdpar,lat_0=latcent,lon_0=longcent)
  elif d == '02': # maryland area
      m= Basemap(llcrnrlon=-84,llcrnrlat=35,urcrnrlon=-69,urcrnrlat=42, rsphere=(earthrad,earthrad),
            resolution='l',area_thresh=1000.,projection='lcc',
            lat_1=stdpar,lat_2=stdpar,lat_0=latcent,lon_0=longcent)
  else: # the full disk of the dataset
      m= Basemap(llcrnrlon=lonW,llcrnrlat=latS,urcrnrlon=lonE,urcrnrlat=latN, rsphere=(earthrad,earthrad),
            resolution='l',area_thresh=1000.,projection='lcc',
            lat_1=stdpar,lat_2=stdpar,lat_0=latcent,lon_0=longcent)
            #lat_1=39.5,lat_2=39.5,lat_0=39.5,lon_0=-98.35)
  xm, ym = m(lons,lats)
  fig = plt.figure(figsize=(14,11))
  ax=fig.add_axes([0.03,0.1,0.94,0.8])
  im = plt.pcolormesh(xm,ym[::-1],data_var[:],cmap='Greys_r',vmin=0,vmax=255)
  m.drawcoastlines(color='red')
  m.drawcountries(color='red')
  m.drawstates(color='red')
  ax.annotate('Univ. of Maryland - Dept. of Atmos. & Oceanic. Sci.',
              xy=(-0.005,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='right',verticalalignment='bottom',
              color='Black',fontsize=12)
  ax.annotate('Trowal - UMD Weather - http://trowal.weather.umd.edu',
              xy=(1.01,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
              color='Black',fontsize=12)
  ax.annotate(sat+' '+title[dtype], xy=(0,1.0), xycoords=('axes fraction'), horizontalalignment='left',
              verticalalignment='bottom', color='black',fontsize=15)
  ax.annotate(timestamp.strftime('%Y-%m-%d %H:%M'), xy=(1.0,1.0), xycoords=('axes fraction'), horizontalalignment='right',
              verticalalignment='bottom', color='black',fontsize=15)
  pos = ax.get_position()
  l, b, w, h = pos.bounds
  ch = 0.015
  cw = 0.8
  cax=plt.axes([l + w*(1-cw)/2,b-ch-0.005,w*cw,ch])
  cb = plt.colorbar(cax=cax, orientation='horizontal')
  cb.set_label(cbarlabel)
  dtype = dtype.strip('.')
  plt.savefig(plotDir+'/'+timestamp.strftime('%Y%m%d_%H%M')+'_'+dtype+'_'+d+'.png',bbox_inches='tight',pad_inches=0)
  plt.close('all')
