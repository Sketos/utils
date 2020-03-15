import numpy as np
from astropy import units as au
from astropy.io import fits


def get_pixel_scale_from_fits(filename, image_hdu=0, units="deg"):


    hdu = fits.open(filename)

    # ...
    header = hdu[image_hdu].header

    # ...
    if ("CDELT1" in header) & ("CDELT2" in header):
        pixel_scale_x = abs(header["CDELT1"])
        pixel_scale_y = abs(header["CDELT2"])
    elif ("CD1_1" in header) & ("CD1_2" in header) & \
            ("CD2_1" in header) & ("CD2_2" in header):
        arg = np.arctan(header["CD2_1"]/header["CD1_1"])
        pixel_scale_x = abs(header["CD1_1"] / np.cos(arg))
        pixel_scale_y = abs(header["CD2_2"] / np.cos(arg))
    elif ("PC1_1" in header) & ("PC1_2" in header) & \
            ("PC2_1" in header) & ("PC2_2" in header):
        arg = np.arctan(header["PC2_1"]/header["PC1_1"])
        pixel_scale_x = abs(header["PC1_1"] / np.cos(arg))
        pixel_scale_y = abs(header["PC2_2"] / np.cos(arg))
    else:
        raise ValueError

    # ...
    if units=="arcsec":
        pixel_scale_x = pixel_scale_x * au.deg.to(au.arcsec)
        pixel_scale_y = pixel_scale_y * au.deg.to(au.arcsec)
    _pixel_scale = np.sqrt(pixel_scale_x * pixel_scale_y)

    return _pixel_scale
