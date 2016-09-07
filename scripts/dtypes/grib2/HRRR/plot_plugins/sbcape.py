import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='sbcape'
title ='Convective Available Potential Energy (surface based)'
cbarlabel = 'J/kg'
boundaryColor = 'gray'
frequency = 3                   # frequency in hrs


def plot(gribobj, pltenv):

    gauss_sigma = 3
    
    cont_int = 10
    cont_smooth = 0.5

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']
    bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.75))

    cape = gribobj.select(name='Convective available potential energy',typeOfLevel='surface',level=0)[0]
    cape = cape.values

    units = 'J/kg'

    #levels = np.arange(-100,150,cont_int)
    levels2 = np.arange(0,6000,100)

    #P = m.contour(x,y,var2,levels=levels,colors='gray')
    #plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)


    m.contourf(x,y,cape,cmap='gist_ncar', levels=levels2, extend='both')
