import numpy as np
from astropy import units as au
from astropy.io import fits


def get_pixel_scale_from_header(header, units="deg"):
    """Short summary.

    Parameters
    ----------
    header : type
        Description of parameter `header`.
    units : type
        Description of parameter `units`.

    Returns
    -------
    type
        Description of returned object.

    """

    if all([
        key in header
        for key in [
            "CDELT1",
            "CDELT2"
        ]
    ]):
        pixel_scale_x = abs(header["CDELT1"])
        pixel_scale_y = abs(header["CDELT2"])
    elif all([
        key in header
        for key in [
            "CD1_1",
            "CD1_2",
            "CD2_1",
            "CD2_2"
        ]
    ]):
        _arg = np.arctan(
            header["CD2_1"] / header["CD1_1"]
        )
        pixel_scale_x = abs(header["CD1_1"] / np.cos(_arg))
        pixel_scale_y = abs(header["CD2_2"] / np.cos(_arg))
    elif all([
        key in header
        for key in [
            "PC1_1",
            "PC1_2",
            "PC2_1",
            "PC2_2"
        ]
    ]):
        _arg = np.arctan(
            header["PC2_1"] / header["PC1_1"]
        )
        pixel_scale_x = abs(header["PC1_1"] / np.cos(_arg))
        pixel_scale_y = abs(header["PC2_2"] / np.cos(_arg))
    else:
        raise ValueError

    # ...
    pixel_scale = np.sqrt(
        pixel_scale_x * pixel_scale_y
    )

    # # NOTE: Check the units of the pixel scale by looking at these header keys.
    # "CUNIT1"
    # "CUNIT2"

    # NOTE: Can we do this in a more elegant way?
    # NOTE: Should I return a value with units or just a float?
    if units == "arcsec":
        pixel_scale = pixel_scale * au.deg.to(au.arcsec)

    return pixel_scale


def get_pixel_scale_from_fits(filename, ext=0, units="arcsec"):

    header = fits.getheader(
        filename=filename, ext=ext
    )

    return get_pixel_scale_from_header(
        header=header,
        units=units
    )


def extract_key_from_header(header, key):

    if key in header:
        return header[key]
    else:
        raise ValueError(
            "{} was not found in the header".format(key)
        )


def extract_list_of_keys_from_header(header, list_of_keys):
    """Short summary.

    Parameters
    ----------
    header : type
        Description of parameter `header`.
    list_of_keys : type
        Description of parameter `list_of_keys`.

    Returns
    -------
    type
        Description of returned object.

    """

    if list_of_keys is None:
        raise ValueError("The list is empty")

    header_keys = {}
    for key in list_of_keys:
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

def test__get_pixel_scale_from_fits():

    filename = "data/test.fits"

    ext = 0
    units = "arcsec"

    pixel_scale = get_pixel_scale_from_fits(
        filename=filename,
        ext=ext,
        units=units
    )

    print(
        "pixel scale = ", pixel_scale, "in units of", units
    )


def test__extract_list_of_keys_from_header():

    # ...
    filename = "data/test.fits"
    ext = 0

    # ...
    header = fits.getheader(
        filename=filename, ext=ext
    )
    #print(header["CDELT1"])

    list_of_keys = [
        "CTYPE3",
        "CRVAL3",
        "CDELT3",
        "CRPIX3",
        "CUNIT3"
    ]

    extract_list_of_keys_from_header
    #header, list_of_keys=None

# ----------------------- #
#
# ----------------------- #

def run_tests():

    #test__get_pixel_scale_from_fits()
    test__extract_list_of_keys_from_header()


if __name__ == "__main__":
    run_tests()
