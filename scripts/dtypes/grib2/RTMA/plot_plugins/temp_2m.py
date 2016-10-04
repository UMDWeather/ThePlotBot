import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='t2'
title ='2m Temperature (F)'
cbarlabel = 'Degrees Fahrenheit'
boundaryColor = 'black'
frequency = 3                   # frequency in hrs


def plot(gribobj, pltenv):

    cont_int = 10
    cont_smooth = 0.5

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']

    bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.75))

    grb = gribobj.select(name='2 metre temperature')[-1]
    var = (grb.values -273.15) * 1.8 + 32
    print var
    var2 = ndimage.gaussian_filter(var,sigma=cont_smooth)
    levels = np.arange(-100,150,cont_int)
    levels2 = np.arange(-40,140,1)

    P = m.contour(x,y,var2,levels=levels,colors='black')
    plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)

    P = m.contour(x,y,var2,levels=[32],colors='r')
    plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)

    m.contourf(x,y,var,cmap='gist_ncar', levels=levels2, extend='both')
