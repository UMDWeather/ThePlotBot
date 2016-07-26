#!/usr/bin/env python
""" skewt4trowal
    C. Martin - 7/2016
    Plot Skew-Ts + Hodographs and
    other relevant info on PNG
    for display on Trowal
"""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime as dt
import netCDF4 as nc
import numpy as np
from metpy.plots import SkewT, Hodograph
from metpy.calc import get_wind_components, lcl, dry_lapse, parcel_profile
from metpy.units import units, concatenate

# directories
plotdir = '/var/www/html/products/raob'
ldmdir = '/home/ldm/data/netcdf/raob2'
stationfile = '/home/plotbot/scripts/raob/stations.tbl'

# get station lat/lon and nickname
stainfo = np.genfromtxt(stationfile,delimiter=',',dtype='str') 
stainfo_code = stainfo[:,1]
stainfo_title = stainfo[:,2]
stainfo_state = stainfo[:,3]
stainfo_country = stainfo[:,4]

# get netCDF file name to read
today = dt.datetime.utcnow()
ncfile = ldmdir+'/Upperair_'+today.strftime('%Y%m%d')+'_0000.nc'

# read in data
f = nc.Dataset(ncfile)
wmoStaNum = f.variables['wmoStaNum'][:]
staName = f.variables['staName'][:]
staName = [''.join(staName[a]) for a in range(len(staName))]
staLat = f.variables['staLat'][:]
staLon = f.variables['staLon'][:]
staElev = f.variables['staElev'][:]
synTime = f.variables['synTime'][:]
synTime = [dt.datetime.utcfromtimestamp(synTime[t]) for t in range(len(synTime))]

# for each record in the file
for r in range(len(wmoStaNum)):
  # set up figure
  fig = plt.figure(figsize=(12, 9))
  gs = gridspec.GridSpec(3, 3)
  # skew T plot
  skew = SkewT(fig, rotation=45, subplot=gs[:, :2]) 
  skew.ax.set_ylim(1000, 100)
  skew.ax.set_xlim(-30, 40)
  # top left hodograph
  ax = fig.add_subplot(gs[0, -1])
  h = Hodograph(ax, component_range=60.)
  h.add_grid(increment=20)
  # annotations
  for b in range(len(stainfo_code)):
    if int(stainfo_code[b]) == int(wmoStaNum[r]):
      nameind = b
  staname = stainfo_title[nameind]
  stastate = stainfo_state[nameind]
  stacountry = stainfo_country[nameind]
  plt.annotate(str(wmoStaNum[r])+' '+staName[r]+' - '+staname.strip()+','+stastate+','+stacountry,xy=(0.02,0.98),xycoords='figure fraction',horizontalalignment='left',verticalalignment='top',fontsize=15)
  plt.annotate(str(staLat[r])+','+str(staLon[r])+' Elev: '+str(int(staElev[r]))+'m',xy=(0.02,0.95),xycoords='figure fraction',horizontalalignment='left',verticalalignment='top',fontsize=12)
  plt.annotate(synTime[r].strftime('%Y-%m-%d %HZ'),xy=(0.98,0.98),xycoords='figure fraction',horizontalalignment='right',verticalalignment='top',fontsize=15)
  plt.annotate('Trowal - UMD Weather - http://trowal.weather.umd.edu',
              xy=(0.02,0.02), xycoords=('figure fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
              color='Black',fontsize=12)
  ## get data
  # mandatory levels
  prMan = f.variables['prMan'][r][:]
  tpMan = f.variables['tpMan'][r][:]
  tpMan = tpMan - 273.15
  tdMan = f.variables['tdMan'][r][:]
  tdMan = tpMan - tdMan
  wdMan = f.variables['wdMan'][r][:]
  wsMan = f.variables['wsMan'][r][:]
  htMan = f.variables['htMan'][r][:]
  # sig T
  prSigT = f.variables['prSigT'][r][:]
  tpSigT = f.variables['tpSigT'][r][:]
  tpSigT = tpSigT - 273.15
  tdSigT = f.variables['tdSigT'][r][:]
  tdSigT = tpSigT - tdSigT
  # sig Wind
  htSigW = f.variables['htSigW'][r][:]
  wdSigW = f.variables['wdSigW'][r][:]
  wsSigW = f.variables['wsSigW'][r][:]
  # concatentate data
  T = np.array([])
  T = np.append(T,tpMan); T = np.append(T,tpSigT)
  Td = np.array([])
  Td = np.append(Td,tdMan); Td = np.append(Td,tdSigT)
  p = np.array([])
  p = np.append(p,prMan); p = np.append(p,prSigT)
  Ws = np.array([]); Wd = np.array([])
  Ws = np.append(Ws,wsMan); Ws = np.append(Ws,wsSigW)
  Wd = np.append(Wd,wdMan); Wd = np.append(Wd,wdSigW)
  hgt = np.array([])
  hgt = np.append(hgt,htMan); hgt = np.append(hgt,htSigW)
  porder = p.argsort()
  p = p[porder[::-1]]
  T = T[porder[::-1]]
  Td = Td[porder[::-1]]
  horder = hgt.argsort()
  hgt = hgt[horder[::-1]]
  Ws = Ws[horder[::-1]]
  Wd = Wd[horder[::-1]]
  p[p>90000] = np.nan
  T[T>90000] = np.nan
  Td[Td>90000] = np.nan
  Ws[Ws>90000] = np.nan
  Wd[Wd>90000] = np.nan
  hgt[hgt>99000] = np.nan

  T = T*units.degC
  Td = Td * units.degC
  p = p * units.mbar
  Ws = Ws*units('m/s')
  Wd = Wd*units.deg
  u, v = get_wind_components(Ws,Wd)
  uman,vman = get_wind_components(wsMan*units('m/s').to(units('knots')),wdMan*units.deg)
  # plot data
  skew.plot(p, T, 'r')
  skew.plot(p, Td, 'g') 
  pmax = np.nanmax(p)
  Pw = [pmax/np.exp(hgt[z]/8000.) for z in range(len(hgt))]
  skew.plot_barbs(prMan,uman,vman)
  skew.plot_dry_adiabats()
  skew.plot_moist_adiabats()
  skew.plot_mixing_lines()
  h.plot_colormapped(u,v,Ws)
  #### calculate parameters
  # LCL
  l = lcl(p[0], T[0], Td[0])
  lcl_temp = dry_lapse(concatenate((p[0], l)), T[0])[-1]
  skew.plot(l, lcl_temp, 'ko', markerfacecolor='black')
  print l,lcl_temp
  # save figure
  plt.savefig(plotdir+'/SkewT_'+staName[r]+'_'+synTime[r].strftime('%Y%m%d%H')+'.png')
  plt.close('all')
