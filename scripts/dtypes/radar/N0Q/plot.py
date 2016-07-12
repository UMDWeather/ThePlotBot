#!/usr/bin/env python
""" N0Q plot
    plot nexrad base reflectivity
    C. Martin - 6/2016
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
plotDir = RootPlotDir+'/radar/'+site
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
radlat = f.lat
radlon = f.lon
lonfac = 111.32*np.cos(np.deg2rad(radlat))

ylocs = radlat + ylocs/111.2
xlocs = radlon + xlocs/(111.32*np.cos(np.deg2rad(ylocs)))

fig = plt.figure(figsize=(14,11))
ax=fig.add_axes([0.03,0.1,0.94,0.8])
titles = {'N0Z':'Base Reflectivity',
	'N0Q':'Base Reflectivity'}
m = Basemap(projection='cea',llcrnrlat=radlat-1.5,urcrnrlat=radlat+1.5,\
            llcrnrlon=radlon-1.5,urcrnrlon=radlon+1.5,resolution='h')
xm, ym = m(xlocs,ylocs)
radarcolors = [
        "#ffffff",
        "#00ffff",
        "#0099ff",
        "#0000ff",
        "#00ff00",
        "#00cc00",
        "#009900",
        "#ffff00",
        "#cccc00",
        "#ff9900",
        "#ff0000",
        "#d40000",
        "#bc0000",
        "#ff00ff",
        "#9966cc",
        "#ffffff"
        ]
colormap = mpl.colors.ListedColormap(radarcolors)
levels = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75]
norm = mpl.colors.BoundaryNorm(levels, 16)
data = data/3.5 # conversion factor?
m.pcolormesh(xm, ym, data,cmap=colormap,norm=norm,alpha=0.5)
m.drawcoastlines(color='black')
m.drawcountries(color='black')
m.drawstates(color='black')
m.drawcounties(color='black')
ax.annotate('Univ. of Maryland - Dept. of Atmos. & Oceanic. Sci.',
              xy=(-0.005,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='right',verticalalignment='bottom',
              color='Black',fontsize=12)
ax.annotate('Trowal - UMD Weather - http://trowal.weather.umd.edu',
              xy=(1.01,0), xycoords=('axes fraction'),rotation=90,horizontalalignment='left',verticalalignment='bottom',
              color='Black',fontsize=12)
ax.annotate(site+' '+f.product_name, xy=(0,1.0), xycoords=('axes fraction'), horizontalalignment='left',
              verticalalignment='bottom', color='black',fontsize=15)
ax.annotate(timestamp.strftime('%Y-%m-%d %H:%M'), xy=(1.0,1.0), xycoords=('axes fraction'), horizontalalignment='right',
              verticalalignment='bottom', color='black',fontsize=15)
pos = ax.get_position()
l, b, w, h = pos.bounds
ch = 0.015
cw = 0.8
cax=plt.axes([l + w*(1-cw)/2,b-ch-0.005,w*cw,ch])
cb = plt.colorbar(cax=cax, orientation='horizontal')
cb.set_label('Reflectivity (dBZ)')
plt.savefig(plotDir+'/'+timestamp.strftime('%Y%m%d_%H%M')+'_'+dtype+'.png')
#plt.savefig(plotDir+'/'+timestamp.strftime('%Y%m%d_%H%M')+'_'+dtype+'.png',bbox_inches='tight',pad_inches=0)
