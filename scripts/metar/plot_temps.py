#!/usr/bin/env python
""" plot_temps.py
    C. Martin - 7/2016
    Plot METAR observations in a given domain
    for temperature, both values at the points
    and color shading to look better
"""
import netCDF4 as nc
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap,maskoceans
import numpy as np
import datetime as dt
from scipy.interpolate import griddata

metardir = '/home/ldm/data/netcdf/metar/'
outdir = '/var/www/html/products/surface/'
### get filename based off of time
now = dt.datetime.utcnow()
ncfile = metardir + 'Surface_METAR_'+now.strftime('%Y%m%d')+'_0000.nc'
f = nc.Dataset(ncfile) # netCDF metar file from LDM
doms = np.genfromtxt('/home/plotbot/scripts/metar/domains.txt',delimiter=',',dtype='str',skip_header=1) # read in domains
lons = f.variables['lon'][:]
lats = f.variables['lat'][:]
times = f.variables['time_obs'][:]
snames = f.variables['stn_name'][:]
snames = [''.join(snames[a,:]) for a in range(len(snames))]
snames = np.array(snames)
times = np.array(times); lons = np.array(lons) ; lats = np.array(lats)
oldtime = now - dt.timedelta(minutes=59)
oldtime = (oldtime - dt.datetime(1970,1,1)).total_seconds()
temperatures = f.variables['T_tenths'][:]
temperatures = temperatures * 1.8 + 32 # this is 'Murica
# for each specified domain in the input file
for d in doms:
  lat1 = float(d[1]); lat2 = float(d[2])
  lon1 = float(d[3]); lon2 = float(d[4])
  # find records within the specified time period and domain
  i = np.where((lats > lat1-2.) & (lats < lat2+2.) & (lons > lon1-2.) & (lons < lon2+2.) & (times >= oldtime) & (temperatures > -40.))
  slats = lats[i] ; slons = lons[i]
  temps = temperatures[i]
  sname = snames[i]
  fig = plt.figure(figsize=(14,11))
  ax=fig.add_axes([0.03,0.1,0.94,0.8])
  m= Basemap(llcrnrlon=lon1,llcrnrlat=lat1,urcrnrlon=lon2,urcrnrlat=lat2,
            resolution='i',area_thresh=100.,projection='merc')
  m.drawcountries()
  m.drawcoastlines()
  m.drawstates()
  m.drawcounties()
  xstat, ystat = m(slons,slats)
  dstats = np.genfromtxt('/home/plotbot/scripts/metar/domains/'+d[0]+'.txt',delimiter=',',dtype='str')
  for ds in dstats:
    dsname = ds[0]
    dslabel = ds[1]
    dslat = float(ds[2])
    dslon = float(ds[3])
    xl,yl = m(dslon,dslat) 
    if d[0] == 'CONUS':
      ax.annotate(dslabel,xy=(xl,yl-150000), xycoords=('data'),
	horizontalalignment='center',verticalalignment='center',fontsize=20,color='white')
    else:
      ax.annotate(dslabel,xy=(xl,yl-15000), xycoords=('data'),
	horizontalalignment='center',verticalalignment='center',fontsize=20,color='white')
    try:
      l = np.where(sname == dsname) # find the datapoint for this station
      ax.annotate(str(int(temps[l])),xy=(xl,yl), xycoords=('data'),
	horizontalalignment='center',verticalalignment='center',fontsize=30,color='white')
    except:
      pass
  glats = np.arange(lat1-1.,lat2+1.,0.01)
  glons = np.arange(lon1-1.,lon2+1.,0.01)
  xg,yg = np.meshgrid(glons,glats)
  GD = griddata((slons,slats),temps,(xg,yg), method='linear') 
  if d[0] == 'CONUS':
    GDmask = maskoceans(xg,yg,GD,resolution='i',grid = 1.25)
    xg,yg = m(xg,yg)
    m.pcolormesh(xg,yg,GDmask,vmin=-140,vmax=120)
    m.drawlsmask(land_color=(0, 0, 0, 0), ocean_color='darkgray', lakes=True)
  else:  
    xg,yg = m(xg,yg)
    m.pcolormesh(xg,yg,GD,vmin=-140,vmax=120)
  ax.annotate('Univ. of Maryland - Dept. of Atmos. & Oceanic. Sci.',
              xy=(-0.005,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='right',verticalalignment='bottom',
              color='Black',fontsize=12)
  ax.annotate('Trowal - UMD Weather - http://trowal.weather.umd.edu',
              xy=(1.01,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
              color='Black',fontsize=12)
  ax.annotate('Current Temperatures', xy=(0,1.01), xycoords=('axes fraction'), horizontalalignment='left',
              verticalalignment='bottom', color='red',fontsize=15)
  ax.annotate('Plot Generated: '+now.strftime('%Y-%m-%d %H:%MZ'),xy=(1,1.01),fontsize=15,
              xycoords="axes fraction", horizontalalignment='right')
  plt.savefig(outdir+now.strftime('%Y%m%d%H%M')+'_CurrTemp_'+d[0]+'.png')
  plt.close('all')
