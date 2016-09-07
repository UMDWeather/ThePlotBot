import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='visibility'
title ='Visibility'
cbarlabel = 'Miles'
boundaryColor = 'black'
frequency = 3                   # frequency in hrs


def plot(gribobj, pltenv):

    cont_int = 10
    cont_smooth = 0.5

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']

    bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.75))

    grb = gribobj.select(name='Visibility')[0]
    var = grb.values /1610. 
    levels = np.arange(0,50,1)

    #P = m.contour(x,y,var2,levels=levels,colors='gray')
    #plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)

    m.contourf(x,y,var,cmap='gist_ncar', levels=levels, extend='both')
