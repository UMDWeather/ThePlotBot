
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm
import __main__

filename='lvl_250winds'
title ='250mb Winds and Geopotential Height'
cbarlabel = 'Knots'
boundaryColor = 'gray'
frequency = 3                   # frequency in hrs

def plot(gribobj, pltenv):

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']

    gribobj.rewind()
    gpm250 = gribobj.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=250)[0]
    var,lats,lons = gpm250.data(lat1=20,lat2=57,lon1=220,lon2=320) 
    x,y = m(lons,lats)
    var = var/10.
    levels = np.arange(930,1218,12)
    P = m.contour(x,y,var,levels=levels,colors='k')
    plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)
    gribobj.rewind()

    u = gribobj.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=250)[0]
    u,lats,lons = u.data(lat1=20,lat2=57,lon1=220,lon2=320)
    gribobj.rewind()
    v = gribobj.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=250)[0]
    v,lats,lons = v.data(lat1=20,lat2=57,lon1=220,lon2=320)
 
    u.shape = v.shape
    wspd = np.sqrt(u**2 + v**2)
    wspd = wspd * 1.94384
    levels2 = np.arange(30,200,10)
    m.contourf(x,y,wspd,levels=levels2,cmap='cool', extend='both')
  
