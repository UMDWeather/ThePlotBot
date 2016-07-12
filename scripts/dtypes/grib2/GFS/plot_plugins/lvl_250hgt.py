
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm
import __main__

filename='lvl_250hgt'
title ='250mb Height and Wind'
cbarlabel = 'knots'
boundaryColor = 'gray'
frequency = 3                   # frequency in hrs

def plot(gribobj, pltenv):

    cont_int = 10
    cont_smooth = 0.5
    thin = 10
    lvl = 11 

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']

    gribobj.rewind()
    gpm250 = gribobj.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=250)[0]
    var,lats,lons = gpm250.data(lat1=20,lat2=57,lon1=220,lon2=320) 
    x,y = m(lons,lats)
    var = var/10.
    levels = np.arange(876,1896,6)
    P = m.contour(x,y,var,levels=levels,colors='k')
    plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)

    u = gribobj.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=250)[0]
    u,lats,lons = u.data(lat1=20,lat2=57,lon1=220,lon2=320) 
    v = gribobj.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=250)[0]
    v,lats,lons = v.data(lat1=20,lat2=57,lon1=220,lon2=320) 
 
    u.shape = v.shape
    u=u*1.944
    v=v*1.944
    wspd = np.sqrt((u**2)+(v**2))
    
    
 
    colortable = [
		 '#ffffff',
		 '#b3c6ff',
		 '#99b3ff',
		 '#809fff',
		  '#3333ff',
		 '#1a1aff',
 		 '#0000ff',
		 '#ff66d9',
	     '#ff4dd2',
	      '#ff33cc',
	      '#732626',
 		  '#602020',
 		 ]
    vort_colormap = mpl.colors.ListedColormap(colortable)
    levels2 = np.arange(60,200,10)
    norm = mpl.colors.BoundaryNorm(levels2,14)
    m.contourf(x,y,wspd,levels=levels2,cmap=vort_colormap,norm=norm, extend='both')
    m.barbs(x[::thin,::thin], y[::thin,::thin], u[::thin,::thin], v[::thin,::thin], length=6)
  
