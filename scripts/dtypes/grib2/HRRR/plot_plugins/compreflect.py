import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='compreflect'
title ='Maximum/Composite Radar Reflectivity'
cbarlabel = 'dBZ'
boundaryColor = 'gray'
frequency = 3                   # frequency in hrs

def extrema(mat,mode='wrap',window=10):
    """find the indices of local extrema (min and max)
    in the input array."""
    mn = minimum_filter(mat, size=window, mode=mode)
    mx = maximum_filter(mat, size=window, mode=mode)
    # (mat == mx) true if pixel is equal to the local max
    # (mat == mn) true if pixel is equal to the local in
    # Return the indices of the maxima, minima
    return np.nonzero(mat == mn), np.nonzero(mat == mx)


def plot(gribobj, pltenv):

    gauss_sigma = 3
    
    cont_int = 10
    cont_smooth = 0.5

    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']
    bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.75))

    dBZ = gribobj.select(name='Maximum/Composite radar reflectivity')[0]
    dBZ = dBZ.values

    units = 'dBZ'

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

    m.contourf(x,y, dBZ, levels,cmap=colormap,norm=norm,extend="both",alpha=0.7)
