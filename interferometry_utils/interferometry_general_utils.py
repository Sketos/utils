import numpy as np

from astropy import units, \
                    constants



def image_plane_grid(resolution, size=5.0):

    def power(x):

        return int(
            pow(2, np.ceil(np.log(x) / np.log(2.0)))
        )

    pixel_scale_maximum = size / (0.5 * resolution)

    n_pixels = power(x=pixel_scale_maximum)

    pixel_scale = size / n_pixels

    return n_pixels, pixel_scale


def image_plane_grid_from_uv_wavelengths(uv_wavelengths, size=5.0):

    uv_distance = np.hypot(
        uv_wavelengths[..., 0], uv_wavelengths[..., 1]
    )

    resolution = 1.0 / np.max(uv_distance) * units.rad.to(units.arcsec)

    return image_plane_grid(resolution=resolution, size=size)



def resolution(uv_distance_max):

    pass
