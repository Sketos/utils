import numpy as np

from astropy import units, constants


def major_axis(phi, centre, n_pixels, pixel_scale):
    """
    # NOTE: This is used to extract the major axis from a kinematical model.
    """
    a = np.tan((phi - 90.0) * units.deg.to(units.rad))

    x_centre  = centre[1] / pixel_scale + n_pixels / 2.0
    y_centre  = -centre[0] / pixel_scale + n_pixels / 2.0

    x = np.arange(0, n_pixels + 1, 1)
    y = a * x + (y_centre  - a * x_centre )

    idx = np.logical_and(
        np.logical_and(y > 0, y < n_pixels),
        np.logical_and(x > 0, x < n_pixels)
    )

    x = x[idx]
    y = y[idx]

    return x, y, x_centre , y_centre
