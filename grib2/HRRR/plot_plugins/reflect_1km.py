import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm

filename='reflect_1km'
title ='Simulated Reflectivity 1km AGL (dBZ)'
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

    dBZ = gribobj.select(name='Derived radar reflectivity',typeOfLevel='heightAboveGround',level=1000)[0]
    dBZ = dBZ.values

    units = 'dBZ'

    radarcolors = [
	"#ffffff",   
 	"#73a26f",
	"#4fa548",
	"#26b91b",
	"#16c909",
	"#1ae30b",
	"#08ff00",
	"#ccff00",
	"#ffcc00",
	"#ff1b0b",
	"#b71004",
	"#7b0101",
	"#7b0142",
        ]

    colormap = mpl.colors.ListedColormap(radarcolors)
    levels = [0,5,10,15,20,25,30,35,40,45,50,55,60]
    norm = mpl.colors.BoundaryNorm(levels, 14)

    m.contourf(x,y, dBZ, levels, cmap=colormap, norm=norm, extend="both")
   

