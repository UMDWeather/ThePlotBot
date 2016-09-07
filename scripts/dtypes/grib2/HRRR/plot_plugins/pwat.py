import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='pwat'
title ='Precipitable Water'
cbarlabel = 'inches'
boundaryColor = 'black'
frequency = 3                   # frequency in hrs


def plot(gribobj, pltenv):

    cont_int = 10
    cont_smooth = 0.5

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']

    bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.75))

    grb = gribobj.select(name='Precipitable water')[0]
    precip = grb.values * 0.03937
    levels2 = np.arange(0,4,0.01)
    m.contourf(x,y,precip,levels=levels2,cmap='gist_ncar',extend='both')
