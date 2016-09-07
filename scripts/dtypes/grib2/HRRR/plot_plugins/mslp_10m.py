import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.filters import minimum_filter, maximum_filter
from mpl_toolkits.basemap import cm
import __main__

filename='mslp_10m'
title ='MSLP / 10m Winds'
cbarlabel = 'Knots'
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
    thin = pltenv['thin'] # for wind barbs

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
    local_min, local_max = extrema(mslp3, window=100)
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


    # 10m winds
    gribobj.rewind()
    u10 = gribobj.select(name='10 metre U wind component')[0]
    u10 = u10.values
    gribobj.rewind()
    v10 = gribobj.select(name='10 metre V wind component')[0]
    v10 = v10.values
    gribobj.rewind()
    spd10 = gribobj.select(name='10 metre wind speed')[0]
    spd10 = spd10.values
    # convert to knots
    u10 = u10*1.944 ; v10 = v10*1.944 ; spd10 = spd10*1.944 
    levels2 = np.arange(0,120,1)
    WS=m.contourf(x,y,spd10,cmap='gist_ncar', levels=levels2, extend='both')
    m.barbs(x[::thin,::thin], y[::thin,::thin], u10[::thin,::thin], v10[::thin,::thin], length=6)
    
