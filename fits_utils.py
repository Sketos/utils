import numpy as np
from astropy import units as au
from astropy.io import fits

def get_pixel_scale_from_header(header, units="deg"):

    if ("CDELT1" in header) & ("CDELT2" in header):
        pixel_scale_x = abs(header["CDELT1"])
        pixel_scale_y = abs(header["CDELT2"])
    elif ("CD1_1" in header) & ("CD1_2" in header) & \
            ("CD2_1" in header) & ("CD2_2" in header):
        _arg = np.arctan(header["CD2_1"] / header["CD1_1"])
        pixel_scale_x = abs(header["CD1_1"] / np.cos(_arg))
        pixel_scale_y = abs(header["CD2_2"] / np.cos(_arg))
    elif ("PC1_1" in header) & ("PC1_2" in header) & \
            ("PC2_1" in header) & ("PC2_2" in header):
        _arg = np.arctan(header["PC2_1"] / header["PC1_1"])
        pixel_scale_x = abs(header["PC1_1"] / np.cos(_arg))
        pixel_scale_y = abs(header["PC2_2"] / np.cos(_arg))
    else:
        raise ValueError

    # NOTE: Can we do this in a more elegant way?
    if units == "arcsec":
        pixel_scale_x = pixel_scale_x * au.deg.to(au.arcsec)
        pixel_scale_y = pixel_scale_y * au.deg.to(au.arcsec)
    pixel_scale = np.sqrt(
        pixel_scale_x * pixel_scale_y
    )

    return pixel_scale


def get_pixel_scale_from_fits(filename, image_hdu=0, units="deg"):

    hdu = fits.open(filename)

    return get_pixel_scale_from_header(
        header=hdu[image_hdu].header, units=units
    )


def extract_header_keys(header, keys=None):

    if keys is None:
        _keys = [
            "CTYPE3",
            "CRVAL3",
            "CDELT3",
            "CRPIX3",
            "CUNIT3"
        ]
    else:
        _keys = keys
    header_keys = {}
    for key in _keys:
        if key in header:
            header_keys[key] = header[key]
        else:
            raise ValueError(
                "{} was not found in the header".format(key)
            )

    return header_keys


def updated_header_with_header_keys(header, header_keys, replace=False):
    header = copy.copy(header)

    if header_keys is None:
        return header

    for key in header_keys:
        if key in header:
            pass # TODO: CHECK IF YOU WANT TO FORCE THE REPLACEMENT OF THIS KEY
        else:
            header[key] = header_keys[key]

    return header


# ----------------------- #
#
# ----------------------- #

def test_get_pixel_scale_from_fits():

    filename = "data/test.fits"

    pixel_scale = get_pixel_scale_from_fits(
        filename=filename, image_hdu=0, units="deg"
    )


    print(pixel_scale)


# ----------------------- #
#
# ----------------------- #

def run_tests():

    test_get_pixel_scale_from_fits()


if __name__ == "__main__":
    run_tests()
