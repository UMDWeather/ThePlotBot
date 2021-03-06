import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm
import __main__

filename='surface'
title ='MSLP / 1000mb-500mb thicknes / 6-hr precip'
cbarlabel = 'inches of precipitation'
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
    lvl_500 = 11


    x = pltenv['x']
    y = pltenv['y']
    m = pltenv['map']


    bbox = dict(boxstyle="square",ec='None',fc=(1,1,1,0.75))

    #calculate MSLP with smoothing
    grb = gribobj.select(name='Pressure reduced to MSL')[0]
    mslp = grb.values/100.
    mslp2 = ndimage.gaussian_filter(mslp,sigma=gauss_sigma)
    levels = np.arange(0,1500,4)
    P=m.contour(x,y,mslp2, levels=levels,colors='k')
    plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=1)


    #plot lows and high
    mslp3 = ndimage.gaussian_filter(mslp,sigma=7)
    local_min, local_max = extrema(mslp3, window=5)
    xlows = x[local_min]; xhighs = x[local_max]
    ylows = y[local_min]; yhighs = y[local_max]
    lowvals = mslp[local_min]; highvals = mslp[local_max]

    # plot lows as blue L's, with min pressure value underneath.
    xyplotted = []
    # don't plot if there is already a L or H within dmin meters.
    yoffset = 0.022*(m.ymax-m.ymin)
    dmin = yoffset
    for hlx,hly,p in zip(xlows, ylows, lowvals):
        if hlx < m.xmax and hlx > m.xmin and hly < m.ymax and hly > m.ymin:
            dist = [np.sqrt((hlx-x0)**2+(hly-y0)**2) for x0,y0 in xyplotted]
            if not dist or min(dist) > dmin:
                plt.text(hlx,hly,'L',fontsize=16,fontweight='bold',
                    ha='center',va='center',color='r')
                plt.text(hlx,hly-yoffset,repr(int(p)),fontsize=11,
                    ha='center',va='top',color='r',
                    bbox = bbox)
                xyplotted.append((hlx,hly))

    # plot highs as red H's, with max pressure value underneath.
    xyplotted = []
    for hlx,hly,p in zip(xhighs, yhighs, highvals):
        if hlx < m.xmax and hlx > m.xmin and hly < m.ymax and hly > m.ymin:
            dist = [np.sqrt((hlx-x0)**2+(hly-y0)**2) for x0,y0 in xyplotted]
            if not dist or min(dist) > dmin:
                plt.text(hlx,hly,'H',fontsize=16,fontweight='bold',
                    ha='center',va='center',color='b')
                plt.text(hlx,hly-yoffset,repr(int(p)),fontsize=11,
                    ha='center',va='top',color='b',
                    bbox = bbox)
                xyplotted.append((hlx,hly))


    #calculate 1000-500mb thickness
    #TODO, use actual model value if H1000 occurs above ground

    gribobj.rewind()
    gpm500 = gribobj.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=500)[0]
    gpm1000 = gribobj.select(name='Geopotential Height',typeOfLevel='isobaricInhPa',level=1000)[0]
    gpm500,lats,lons = gpm500.data(lat1=20,lat2=55,lon1=220,lon2=320)
    gpm1000,lats,lons = gpm1000.data(lat1=20,lat2=55,lon1=220,lon2=320)
    x,y = m(lons,lats)
    thck = gpm500-gpm1000
    thck = thck/10.
    thck2 = ndimage.gaussian_filter(thck,sigma=gauss_sigma)

    #plot thickness
    colors = [
        (0, 540, 'cyan'),
        (540, 541, 'blue'),
        (546, 570, 'red'),
        (570, 700, 'brown'),
        ]

    for c in colors:
        levels = np.arange(c[0],c[1],6)
        P = m.contour(x,y,thck2,levels=levels,colors=c[2], linestyles='dashed')
        plt.clabel(P,inline=1,fontsize=10,fmt='%1.0f',inline_spacing=2)


    # precip
    x = pltenv['x']
    y = pltenv['y']
    gribobj.rewind()
    if __main__.timestep == '000':
      precip = thck 
      precip[:] = 0
    else:
      precip = gribobj.select(name='Total Precipitation')[0]
      precip = precip.values # this is in mm
      precip = precip * 0.0393701 # convert to inches for plot

    nws_precip_colors = [
        "#7fff00",  # 0.01 - 0.10 inches
        "#00cd00",  # 0.10 - 0.25 inches
        "#008b00",  # 0.25 - 0.50 inches
        "#104e8b",  # 0.50 - 0.75 inches
        "#1e90ff",  # 0.75 - 1.00 inches
        "#00b2ee",  # 1.00 - 1.25 inches
        "#00eeee",  # 1.25 - 1.50 inches

        "#8968cd",  # 1.50 - 1.75
        "#912cee",  # 1.75 -
        "#8b008b",  # 2.0 - 
        "#8b0000",  # 2.5 - 
        "#cd0000",  # 3.0 -
        "#ee4000",  # 4.0 -
        "#ff7f00",  # 5.0 -
        "#cd8500",  # 6.0 -
        "#ffd700",  # 7.0 -
        "#eeee00",  # 8.0 - 
        "#ffff00",  # 9.0 -
        ]
    precip_colormap = mpl.colors.ListedColormap(nws_precip_colors)
    levels = [0.01, 0.1, 0.25, 0.50, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 5.0,
          6.0, 7.0, 8.0, 9.0, 10.,]
    norm = mpl.colors.BoundaryNorm(levels, 18)
    
    m.contourf(x,y,precip,levels,cmap=precip_colormap, norm=norm)
#    plt.colorbar()
