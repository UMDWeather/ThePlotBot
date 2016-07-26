import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from metpy.cbook import get_test_data
from metpy.calc import get_wind_components
from metpy.plots import SkewT, Hodograph
from metpy.units import units

fig = plt.figure(figsize=(9, 9))

# Grid for plots
gs = gridspec.GridSpec(3, 3)
skew = SkewT(fig, rotation=45, subplot=gs[:, :2])

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.ax.set_ylim(1000, 100)

# Add the relevant special lines

# Good bounds for aspect ratio
skew.ax.set_xlim(-30, 40)

# Create a hodograph
ax = fig.add_subplot(gs[0, -1])
h = Hodograph(ax, component_range=60.)
h.add_grid(increment=20)

# Show the plot
plt.show()
