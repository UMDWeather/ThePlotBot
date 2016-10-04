#!/usr/bin/env python
""" 500 hgt Spaghetti Plot of 
	deterministic model guidance
	C. Martin - 9/2016
"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import datetime as dt
import pygrib as grb
import netCDF4 as nc
import os
import glob
import matplotlib.patches as mpatches

""" parameters below """
plotdir = '/var/www/html/products/spaghetti'
lev500 = [540,588]

pltenv={}
# just the CONUS domain here...
m = Basemap(width=5100000, height=3600000, rsphere=(6378137.00,6356752.3142),
            resolution='l',area_thresh=1000.,projection='lcc',
            lat_1=39.5,lat_2=39.5,lat_0=39.5,lon_0=-98.35)
            

""" just most recent model run of each """
now = dt.datetime.utcnow()

# GFS most recent time
newest = sorted(glob.iglob('/home/ldm/data/grib2/GFS/*'))[-1]
newest = newest.split('/')
gfstime = dt.datetime.strptime(newest[-1],"%Y%m%d%H")
# CMC most recent time
newest = sorted(glob.iglob('/home/ldm/data/grib2/CMC/*'))[-1]
newest = newest.split('/')
cmctime = dt.datetime.strptime(newest[-1][8:-11],"%Y%m%d%H")


fcsthrs = [0,24,48]
for hr in fcsthrs:
	validtime = gfstime + dt.timedelta(hours=hr)
	fig = plt.figure(figsize=(14,11))
	ax=fig.add_axes([0.03,0.1,0.94,0.8])
	pltenv['map'] = m
	pltenv['ax']=ax
	pltenv['map'].drawcoastlines(color='gray')
	pltenv['map'].drawcountries(color='black')
	pltenv['map'].drawstates(color='gray')
	ax.annotate('valid: '+validtime.strftime('%Y-%m-%d %HZ'),xy=(1,1.01),fontsize=15,
	              xycoords="axes fraction", horizontalalignment='right')
	ax.annotate('University of Maryland Dept. of Atmospheric and Oceanic Science',
				  xy=(1.01,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
				  color='gray',fontsize=8)
	ax.annotate('Deterministic Model Comparison', xy=(0,1.01), xycoords=('axes fraction'),horizontalalignment='left',
				  verticalalignment='bottom', color='red')
	plt.title('500 hPa Geopotential Heights',fontweight='bold')
	# plot GFS data
	gfs = grb.open('/home/ldm/data/grib2/GFS/'+gfstime.strftime('%Y%m%d%H')+'/'+'gfs.t'+gfstime.strftime('%H')+'z.pgrb2.0p25.f%03d' % (hr))
	gfs500 = gfs.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=500)[0]
	var,lats,lons = gfs500.data(lat1=20,lat2=57,lon1=220,lon2=320) 
	x,y = m(lons,lats)
	m.contour(x,y,var/10.,levels=lev500,colors='red',label='GFS0.25')
	# plot CMC data
	cmc = grb.open('/home/ldm/data/grib2/CMC/CMC_reg_'+cmctime.strftime('%Y%m%d%H')+'_F%03d.grib2' % (hr))
	cmc.rewind()
	cmc500 = cmc.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=500)[0]
	var = cmc500.values
	lats, lons = cmc500.latlons()
	x,y = m(lons,lats)
	m.contour(x,y,var/10.,levels=lev500,colors='blue',label='CMC')
	# add legend
	blue_patch = mpatches.Patch(color='blue', label='CMC')
	red_patch = mpatches.Patch(color='red', label='GFS0.25')
	plt.legend(handles=[red_patch,blue_patch],bbox_to_anchor=(0.00, -0.0), loc=2, borderaxespad=0.,ncol=5)
	plt.savefig(plotdir+'/500hpa_mostrecent_F'+str(hr)+'.png')