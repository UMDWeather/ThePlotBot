#!/usr/bin/env python
""" GFS Grid Interpolation
    Loop through each timestep in the model
    and through each MOS station in the text file
    and output to a .txt file various values
    interpolated at the gridpoint nearest the station

    C. Martin - 9/2016
"""
import numpy as np
import pygrib
import datetime as dt
import sys
import os
import glob
import shutil
from metpy.calc import get_wind_components, get_wind_speed, get_wind_dir
from metpy.units import units, concatenate

fcsthrs = [0,6,9,12,15,18,21,24,27,30,33,36,42,48,54,60,66,72]
# get runtime of most recent GFS
newest = sorted(glob.iglob('/home/ldm/data/grib2/GFS/*'))[-1]
newest = newest.split('/')
runtime = dt.datetime.strptime(newest[-1],"%Y%m%d%H")
gfsdir = '/home/ldm/data/grib2/GFS/'

# get list of stations to process
stationfile = '/var/www/html/models/GridInterp/stations_nws.html'
headers = []
stations = []
for line in open(stationfile):
  if line.startswith('K'):
    headers.append(line.rstrip())
    stations.append(line.rstrip().split())
  else:
    continue

codes = [] ; lats = []; lons=[]
for station in stations:
  codes.append(station[0])
  lats.append(station[-2])
  lons.append(station[-1])

from math import pi
def findpoint(latvar,lonvar,lat0,lon0):
    '''
    Find closest point in a set of (lat,lon) points to specified point
    latvar - 2D latitude variable from an open netCDF dataset
    lonvar - 2D longitude variable from an open netCDF dataset
    lat0,lon0 - query point
    Returns iy,ix such that the square of the tunnel distance
    between (latval[it,ix],lonval[iy,ix]) and (lat0,lon0)
    is minimum.
    From Unidata python workshop
    '''
    rad_factor = pi/180.0 # for trignometry, need angles in radians
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:] * rad_factor
    lonvals = lonvar[:] * rad_factor
    ny,nx = latvals.shape
    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    # Compute numpy arrays for all values, no loops
    clat,clon = np.cos(latvals),np.cos(lonvals)
    slat,slon = np.sin(latvals),np.sin(lonvals)
    delX = np.cos(lat0_rad)*np.cos(lon0_rad) - clat*clon
    delY = np.cos(lat0_rad)*np.sin(lon0_rad) - clat*slon
    delZ = np.sin(lat0_rad) - slat;
    dist_sq = delX**2 + delY**2 + delZ**2
    minindex_1d = dist_sq.argmin()  # 1D index of minimum element
    iy_min,ix_min = np.unravel_index(minindex_1d, latvals.shape)
    return iy_min,ix_min

outfile = '/var/www/html/products/ourtext/GridInterp/'+'tmp_GFS_'+runtime.strftime('%Y%m%d%H')

# blank lists to append lists of each value at each time step
t2 = []
t850 = []
t700 = []
t500 = []
thick = []
dew2 = []
d850 = []
d700 = []
d500 = []
qpf = []
w10 = []
d10 = []
w850 = []
w700 = []
w500 = []
w250 = []
wd850 = []
wd700 = []
wd500 = []
wd250 = []
mslp = []
hgt500 = []

# lists of GFS nearest coordinates for each station
eyes = []
jays = []
for a in range(len(fcsthrs)):
  print a
  # blank arrays for each value at each station
  var1 = []
  var2 = []
  var3 = []
  var4 = []
  var5 = []
  var6 = []
  var7 = []
  var8 = []
  var9 = []
  var10 = []
  var11 = []
  var12 = []
  var13 = []
  var14 = []
  var15 = []
  var16 = []
  var17 = []
  var18 = []
  var19 = []
  var20 = []
  var21 = []
  var22 = []
  gfs = pygrib.open(gfsdir+'/'+runtime.strftime('%Y%m%d%H')+'/'+'gfs.t'+runtime.strftime('%H')+'z.pgrb2.0p25.f%03d' % (fcsthrs[a]))
  grb = gfs.read(1)[0]
  gfslats, gfslons = grb.latlons()
  gfs.seek(0)
  grb = gfs.select(name='2 metre temperature')[0]
  vart2 = (grb.values -273.15) * 1.8 + 32
  gfs.seek(0)
  grb = gfs.select(name='Temperature',typeOfLevel='isobaricInhPa',level=850)[0]
  vart850 = (grb.values - 273.15)
  gfs.seek(0)
  grb = gfs.select(name='Temperature',typeOfLevel='isobaricInhPa',level=700)[0]
  vart700 = (grb.values - 273.15)
  gfs.seek(0)
  grb = gfs.select(name='Temperature',typeOfLevel='isobaricInhPa',level=500)[0]
  vart500 = (grb.values - 273.15)
  gfs.seek(0)
  grb = gfs.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=500)[0]
  var500hgt = grb.values
  gfs.seek(0)
  grb = gfs.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=1000)[0]
  varthick = var500hgt - grb.values 
  gfs.seek(0)
  grb = gfs.select(name='2 metre dewpoint temperature')[0]
  vardew2 = (grb.values -273.15) * 1.8 + 32
  gfs.seek(0)
  grb = gfs.select(name='Relative humidity',typeOfLevel='isobaricInhPa',level=850)[0]
  vard850 = grb.values
  gfs.seek(0)
  grb = gfs.select(name='Relative humidity',typeOfLevel='isobaricInhPa',level=700)[0]
  vard700 = grb.values
  gfs.seek(0)
  grb = gfs.select(name='Relative humidity',typeOfLevel='isobaricInhPa',level=500)[0]
  vard500 = grb.values
  gfs.seek(0)
  if a == 0:
    varqpf = 0
  else:
    grb = gfs.select(name='Total Precipitation')[0]
    varqpf = grb.values * 0.0393701 
  gfs.seek(0)
  grb = gfs.select(name='10 metre U wind component')[0]
  varu10 = grb.values * 1.943844492 # knots
  gfs.seek(0)
  grb = gfs.select(name='10 metre V wind component')[0]
  varv10 = grb.values * 1.943844492 # knots
  varw10 = get_wind_speed(varu10*units('knots'),varv10*units('knots'))
  vard10 = get_wind_dir(varu10*units('knots'),varv10*units('knots'))
  gfs.seek(0)
  grb = gfs.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=850)[0]
  varu850 = grb.values * 1.943844492 # knots
  gfs.seek(0)
  grb = gfs.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=850)[0]
  varv850 = grb.values * 1.943844492 # knots
  varw850 = get_wind_speed(varu850*units('knots'),varv850*units('knots'))
  varwd850 = get_wind_dir(varu850*units('knots'),varv850*units('knots'))
  gfs.seek(0)
  grb = gfs.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=700)[0]
  varu700 = grb.values * 1.943844492 # knots
  gfs.seek(0)
  grb = gfs.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=700)[0]
  varv700 = grb.values * 1.943844492 # knots
  varw700 = get_wind_speed(varu700*units('knots'),varv700*units('knots'))
  varwd700 = get_wind_dir(varu700*units('knots'),varv700*units('knots'))
  gfs.seek(0)
  grb = gfs.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=500)[0]
  varu500 = grb.values * 1.943844492 # knots
  gfs.seek(0)
  grb = gfs.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=500)[0]
  varv500 = grb.values * 1.943844492 # knots
  varw500 = get_wind_speed(varu500*units('knots'),varv500*units('knots'))
  varwd500 = get_wind_dir(varu500*units('knots'),varv500*units('knots'))
  gfs.seek(0)
  grb = gfs.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=250)[0]
  varu250 = grb.values * 1.943844492 # knots
  gfs.seek(0)
  grb = gfs.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=250)[0]
  varv250 = grb.values * 1.943844492 # knots
  varw250 = get_wind_speed(varu250*units('knots'),varv250*units('knots'))
  varwd250 = get_wind_dir(varu250*units('knots'),varv250*units('knots'))
  gfs.seek(0)
  grb = gfs.select(name='Pressure reduced to MSL')[0]
  varmslp = grb.values/100.
  gfs.seek(0)
  for b in range(len(stations)):
    print codes[b]
    if a == 0:
      j,i = findpoint(gfslats,gfslons,float(lats[b][:-1]),-float(lons[b][:-1])) # hard coded the negative, only care about US
      eyes.append(i);jays.append(j)
    i = eyes[b]; j = jays[b]
    # append each station value to the intermediate lists
    var1.append(vart2[j,i])
    var2.append(vart850[j,i])
    var3.append(vart700[j,i])
    var4.append(vart500[j,i])
    var5.append(varthick[j,i]/10.)
    var6.append(vardew2[j,i])
    var7.append(vard850[j,i])
    var8.append(vard700[j,i])
    var9.append(vard500[j,i])
    if a == 0:
      var10.append(0)
    else:
      var10.append(varqpf[j,i])
    var11.append(varw10[j,i].magnitude)
    var12.append(vard10[j,i].magnitude)
    var13.append(varw850[j,i].magnitude)
    var14.append(varwd850[j,i].magnitude)
    var15.append(varw700[j,i].magnitude)
    var18.append(varwd700[j,i].magnitude)
    var19.append(varw500[j,i].magnitude)
    var20.append(varwd500[j,i].magnitude)
    var21.append(varw250[j,i].magnitude)
    var22.append(varwd250[j,i].magnitude)
    var16.append(varmslp[j,i])
    var17.append(var500hgt[j,i]/10.)
  # append the intermediate lists to the main lists
  t2.append(var1) 
  t850.append(var2)
  t700.append(var3)
  t500.append(var4)
  thick.append(var5)
  dew2.append(var6)
  d850.append(var7)
  d700.append(var8)
  d500.append(var9)
  qpf.append(var10)
  w10.append(var11)
  d10.append(var12)
  w850.append(var13)
  wd850.append(var14)
  w700.append(var15)
  wd700.append(var16)
  w500.append(var18)
  wd500.append(var19)
  w250.append(var20)
  wd250.append(var21)
  mslp.append(var16)
  hgt500.append(var17)

f = open(outfile,'w')
for a in range(len(stations)):
  f.write(str(headers[a])+'\n')
  f.write('GFS Initialization time: '+runtime.strftime('%Y-%m-%d %H')+'Z\n')
  f.write('Parameter/Time')
  for hr in fcsthrs:
    f.write('\t%03d' % hr)
  f.write('\n')
  f.write('--------------\t---------------------------------------------------------------------------------------------\n')
  f.write('   Day/Hour')
  for hr in fcsthrs:
     f.write('\t'+dt.datetime.strftime(runtime+dt.timedelta(hours=hr),'%d/%H'))
  f.write('\n')
  f.write('--------------\t---------------------------------------------------------------------------------------------\n')
  f.write('Temps\n')
  f.write(' SFC (2 M) (F)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(t2[b][a])))
  f.write('\n')
  f.write(' 850 MB (C)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(t850[b][a])))
  f.write('\n 700 mb (C)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(t700[b][a])))
  f.write('\n 500 mb (C)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(t500[b][a])))
  f.write('\n 1000-500 (dam)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(thick[b][a])))
  f.write('\n\n---------------------------------------------------------------------------------------------------------------------\n')
  #- moisture -#
  f.write('Moisture\n')
  f.write(' SFC Dew (F)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(dew2[b][a])))
  f.write('\n 850 RH %')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(d850[b][a])))
  f.write('\n 700 RH %')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(d700[b][a])))
  f.write('\n 500 RH %')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(d500[b][a])))
  f.write('\n 3-hr QPF (in)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(round(qpf[b][a],2)))
  f.write('\n\n---------------------------------------------------------------------------------------------------------------------\n')
  #- winds -#
  f.write('Winds Spd/Dir\n')
  f.write(' 10m (kts)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(w10[b][a]))+'/'+str(int(d10[b][a])))
  f.write('\n 850 winds')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(w850[b][a]))+'/'+str(int(wd850[b][a])))
  f.write('\n 700 winds')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(w700[b][a]))+'/'+str(int(wd700[b][a])))
  f.write('\n 500 winds')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(w500[b][a]))+'/'+str(int(wd500[b][a])))
  f.write('\n 250 winds')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(w250[b][a]))+'/'+str(int(wd250[b][a])))
  f.write('\n\n---------------------------------------------------------------------------------------------------------------------\n')
  #- misc -#
  f.write('Other\n')
  f.write(' MSLP (mb)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(mslp[b][a])))
  f.write('\n 500 hgt (dam)')
  for b in range(len(fcsthrs)):
     f.write('\t'+str(int(hgt500[b][a])))
  f.write('\n\n---------------------------------------------------------------------------------------------------------------------\n')
  f.write('- End Record - \n')
  f.flush() # write to disk
f.close()
outfilef = '/var/www/html/products/ourtext/GridInterp/'+'GFS_'+runtime.strftime('%Y%m%d%H')
shutil.move(outfile,outfilef)
