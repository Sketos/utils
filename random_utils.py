import random

import astropy_wrappers as astropy_wrappers


# NOTE:
NUMBER_OF_CHARACTERS_FOR_COLOR_STRING = 6


def generate_list_of_random_colors(length_of_list):
    """Short summary.

    Parameters
    ----------
    length_of_list : type
        Description of parameter `length_of_list`.

    Returns
    -------
    type
        Description of returned object.

    """

    list_of_random_colors = [
        "#" + ''.join([
            random.choice('0123456789ABCDEF') for j in range(NUMBER_OF_CHARACTERS_FOR_COLOR_STRING)
        ])
        for i in range(length_of_list)
    ]

    return list_of_random_colors


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def measure(n):
    "Measurement model, return two coupled measurements."
    m1 = np.random.normal(size=n)
    m2 = np.random.normal(scale=0.5, size=n)
    return m1+m2, m1-m2

m1, m2 = measure(2000)
xmin = m1.min()
xmax = m1.max()
ymin = m2.min()
ymax = m2.max()

X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([X.ravel(), Y.ravel()])
values = np.vstack([m1, m2])
kernel = stats.gaussian_kde(values)
Z = np.reshape(kernel(positions).T, X.shape)

# fig, ax = plt.subplots()
# ax.imshow(np.rot90(Z), cmap=plt.cm.gist_earth_r,
#           extent=[xmin, xmax, ymin, ymax])
# ax.plot(m1, m2, 'k.', markersize=2)
# ax.set_xlim([xmin, xmax])
# ax.set_ylim([ymin, ymax])
# plt.show()

# TODO: Use this Gaussian to generate random numbers.
n_pixels = 100
Gaussian2D = astropy_wrappers.Gaussian2D(
    shape_2d=(
        n_pixels,
        n_pixels
    ),
    amplitude=1.0,
    x_mean=n_pixels/2.0,
    y_mean=n_pixels/2.0,
    x_stddev=n_pixels/10.0,
    y_stddev=n_pixels/15.0,
    theta=45.0
)
plt.figure()
plt.imshow(Gaussian2D)
plt.show()
exit()

# Generate the bins for each axis
x_bins = np.linspace(xmin, xmax, Z.shape[0]+1)
y_bins = np.linspace(ymin, ymax, Z.shape[1]+1)

# Find the middle point for each bin
x_bin_midpoints = x_bins[:-1] + np.diff(x_bins)/2
y_bin_midpoints = y_bins[:-1] + np.diff(y_bins)/2

# Calculate the Cumulative Distribution Function(CDF)from the PDF
cdf = np.cumsum(Z.ravel())
cdf = cdf / cdf[-1] # Normalização

# Create random data
values = np.random.rand(10000)

# Find the data position
value_bins = np.searchsorted(cdf, values)
x_idx, y_idx = np.unravel_index(value_bins,
                                (len(x_bin_midpoints),
                                 len(y_bin_midpoints)))

# Create the new data
new_data = np.column_stack((x_bin_midpoints[x_idx],
                            y_bin_midpoints[y_idx]))
new_x, new_y = new_data.T

kernel = stats.gaussian_kde(new_data.T)
new_Z = np.reshape(kernel(positions).T, X.shape)

fig, ax = plt.subplots()
ax.imshow(np.rot90(new_Z), cmap=plt.cm.gist_earth_r,
          extent=[xmin, xmax, ymin, ymax])
ax.plot(new_x, new_y, 'k.', markersize=2)
ax.set_xlim([xmin, xmax])
ax.set_ylim([ymin, ymax])
plt.show()


if __name__ == "__main__":
    pass
