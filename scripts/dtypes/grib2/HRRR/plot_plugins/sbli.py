import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='sbli'
title ='Lifted Index (surface based)'
cbarlabel = 'C'
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

    li = gribobj.select(name='Surface lifted index')[0]
    li = li.values

    units = 'C'

    #levels = np.arange(-100,150,cont_int)
    levels2 = np.arange(-30,0,0.1)

    #P = m.contour(x,y,var2,levels=levels,colors='gray')
    #plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)


    m.contourf(x,y,li,cmap='gist_ncar', levels=levels2, extend='both')
