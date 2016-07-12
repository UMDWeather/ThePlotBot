
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm
import __main__

filename='lvl_500vorticity'
title ='500mb Absolute Vorticity'
cbarlabel = 'x 10^-5 sec^-1'
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
    gpm500 = gribobj.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=500)[0]
    var,lats,lons = gpm500.data(lat1=20,lat2=57,lon1=220,lon2=320) 
    x,y = m(lons,lats)
    var = var/10.
    levels = np.arange(0,600,4)
    P = m.contour(x,y,var,levels=levels,colors='k')
    plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)

    u = gribobj.select(name='U component of wind',typeOfLevel='isobaricInhPa',level=500)[0]
    u = u.values
    v = gribobj.select(name='V component of wind',typeOfLevel='isobaricInhPa',level=500)[0]
    v = v.values
 
    u.shape = v.shape
    vort = gribobj.select(name='Absolute vorticity',typeOfLevel='isobaricInhPa',level=500)[0]
 
    vort,lats,lons = vort.data(lat1=20,lat2=57,lon1=220,lon2=320)
    # NOTE: why isn't relative vorticity working?
    #F = 7.292e-5*np.sin(__main__.lats)
    F = 0
    relvort = vort - F 
    NormalizedRelVort = relvort * 100000
    colortable = [
		 "#ffffff",
                 "#ffff00",
		 "#ffee00",
		 "#ffdd00",
  		 "#ffcc00",
                 "#ffbb00",
		 "#ffaa00",
 		 "#ff9900",
		 "#ff8800",
	 	 "#ff7700",
	         "#ff6600",
		 "#ff5500",
		 "#ff4400",
		 "#ff3300",
		 "#ff2200",
		 "#ff1100",
		 "#ff0000",
		 ]
    vort_colormap = mpl.colors.ListedColormap(colortable)
    levels2 = np.arange(0,51,3)
    norm = mpl.colors.BoundaryNorm(levels2,19)
    m.contourf(x,y,NormalizedRelVort,levels=levels2,cmap=vort_colormap,norm=norm, extend='both')
  
