#!/usr/bin/env python
"""
   metar2nc
   C. Martin - Univ. of MD - 7/2016
   takes input from stdin of raw METAR data and
   write converted METAR data to netCDF file
"""
from netCDF4 import Dataset
import datetime as dt
import os
import sys
from metar import Metar

metardir = '/home/ldm/data/netcdf/metar'
now = dt.datetime.utcnow()

# get input from stdin
metarin = sys.stdin.read()
metarin = metarin.replace('\n','')
records = metarin.split('=') # records end with equals sign
for record in records:
  try:
    obs = Metar.Metar(record)
    stationid = obs.station_id
    outdir = metardir+'/'+now.strftime('%Y%m%d')
    if not os.path.exists(outdir):
      os.makedirs(outdir)
    cdffile = outdir+'/'+now.strftime('%Y%m%d')+'_'+stationid+'.nc'
    # check if netCDF file exists
    if os.path.isfile(cdffile):
      # open as appendable
      cdfout = Dataset(cdffile,'a',format='NETCDF4')
      stationout = cdfout.variables["StationID"]
      timestampout = cdfout.variables["Timestamp"]
      tempout = cdfout.variables["Temp"]
      dewout = cdfout.variables["DewTemp"]
      pressout = cdfout.variables["Pressure"]
      remarksout = cdfout.variables["Remarks"]
      wspdout = cdfout.variables["WindSpeed"]
      wdirout = cdfout.variables["WindDir"]
    else:
      # create new netcdf file
      cdfout = Dataset(cdffile,'w',format='NETCDF4') 
      # this also means we need to create the dimensions and vars
      timeout = cdfout.createDimension("Time", None)
      stationout = cdfout.createVariable("StationID", "S2", ("Time",))
      timestampout = cdfout.createVariable("Timestamp","S2",("Time",))
      tempout = cdfout.createVariable("Temp","f4",("Time",))
      dewout = cdfout.createVariable("DewTemp","f4",("Time",))
      pressout = cdfout.createVariable("Pressure","f4",("Time",))
      remarksout = cdfout.createVariable("Remarks","S2",("Time",))
      wspdout = cdfout.createVariable("WindSpeed","f4",("Time",))
      wdirout = cdfout.createVariable("WindDir","f4",("Time",))
    r = len(stationout)
    stationout[r] = stationid
    timestampout[r] = obs.time.ctime()
    tempout[r] = obs.temp.value("C")
    dewout[r] = obs.dewpt.value("C")
    pressout[r] = obs.press.value("mb")
    remarks = ', '.join(obs._remarks)
    remarksout[r] = remarks
    wspdout[r] = obs.wind_speed.value("KT")
    wdirout[r] = obs.wind_dir.value()
  except:
    pass
  try:
    cdfout.close()
  except:
    pass
