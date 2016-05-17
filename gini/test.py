from metpy.io.gini import GiniFile
gini = GiniFile('/home/ldm/data/sat/20160516/01/GOES-15/0140Z_WV_4km_WEST-CONUS-TIGW05_KNES_68255.satz.2016051601')
print(gini)
gini_ds = gini.to_dataset()
print(gini_ds)
print(gini_ds.variables)
data_var = gini_ds.variables['WV']
print(data_var)
x = gini_ds.variables['x'][:]
y = gini_ds.variables['y'][:]
proj_var = gini_ds.variables[data_var.grid_mapping]
print(proj_var)

import matplotlib.pyplot as plt

# Create a new figure with size 10" by 10"
fig = plt.figure(figsize=(10, 10))

# Put a single axes on this figure; set the projection for the axes to be our
# Lambert conformal projection
ax = fig.add_subplot(1, 1, 1)

# Plot the data using a simple greyscale colormap (with black for low values);
# set the colormap to extend over a range of values from 140 to 255.
# Note, we save the image returned by imshow for later...
im = ax.imshow(data_var[:], extent=(x[0], x[-1], y[0], y[-1]), origin='upper',
               cmap='Greys_r', norm=plt.Normalize(140, 255))

# Add high-resolution coastlines to the plot
plt.savefig('out.png')
