import os, sys, copy

import numpy as np

import matplotlib.pyplot as plt

from astropy import units as au

from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS

import aplpy

# ---------------------------------------------------------------------------- #
# NOTE:

import spectral_utils as spectral_utils

# ---------------------------------------------------------------------------- #


def cutout(
    hdu,
    xmin=None,
    xmax=None,
    ymin=None,
    ymax=None,
    return_products=False,
    filename=None
):

    header = hdu.header
    if not np.logical_and.reduce((
        "CRVAL1" in header,
        "CRVAL2" in header,
        "CRPIX1" in header,
        "CRPIX2" in header,
    )):
        raise NotImplementedError()
    else:
        CRPIX1 = header["CRPIX1"]
        CRPIX2 = header["CRPIX2"]
    header_cutout = copy.deepcopy(header)


    # NOTE: make cutout
    data = hdu.data
    # print("ymin =", ymin)
    # print("ymax =", ymax)
    # print("xmin =", xmin)
    # print("xmax =", xmax)
    # exit()
    data_cutout = data[
        ymin:ymax,
        xmin:xmax,
    ]

    # NOTE: update astrometry
    CRPIX1_cutout = CRPIX1 - xmin
    CRPIX2_cutout = CRPIX2 - ymin
    header_cutout["CRPIX1"] = CRPIX1_cutout
    header_cutout["CRPIX2"] = CRPIX2_cutout

    # NOTE:
    # if filename is not None:
    #     pass

    if return_products:
        return data_cutout, header_cutout, ymin, ymax, xmin, xmax
    return data_cutout, header_cutout


def angle_from_header(header):

    # NOTE: tan(x) = sin(x) / cos(x)

    if np.logical_and("PC1_1" in header, "PC1_2" in header):
        PC1_2 = header["PC1_2"]
        PC1_1 = header["PC1_1"]
        angle = np.degrees(np.arctan2(PC1_2, PC1_1))
    elif np.logical_and("CD1_1" in header, "CD1_2" in header):
        CD1_1 = header["CD1_1"]
        CD1_2 = header["CD1_2"]
        angle = np.degrees(np.arctan2(CD1_2, CD1_1))
    #return 180.0 - angle
    return angle

def get_beam_from_header(header, units="deg"):
    pass

def get_beam_from_fits(filename, ext=0, units="arcsec"):

    header = fits.getheader(
        filename=filename, ext=ext
    )

    print(header["BMAJ"] * au.deg.to(au.arcsec))
    print(header["BMIN"] * au.deg.to(au.arcsec))

    beam_x = header["BMAJ"] * au.deg.to(au.arcsec)
    beam_y = header["BMIN"] * au.deg.to(au.arcsec)

    return np.pi * (beam_x * beam_y)

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
            "CD1_1",
            "CD1_2",
            "CD2_1",
            "CD2_2"
        ]
    ]):
        #print("method 1:")
        _arg = np.arctan(
            header["CD2_1"] / header["CD1_1"]
        )
        pixel_scale_x = abs(header["CD1_1"] / np.cos(_arg))
        pixel_scale_y = abs(header["CD2_2"] / np.cos(_arg))
    elif all([
        key in header
        for key in [
            "CDELT1",
            "CDELT2"
        ]
    ]):
        #print("method 2:")
        pixel_scale_x = abs(header["CDELT1"])
        pixel_scale_y = abs(header["CDELT2"])
    elif all([
        key in header
        for key in [
            "PC1_1",
            "PC1_2",
            "PC2_1",
            "PC2_2"
        ]
    ]):
        #print("method 3:")
        arg = np.arctan(
            header["PC2_1"] / header["PC1_1"]
        )
        pixel_scale_x = abs(header["PC1_1"] / np.cos(arg))
        pixel_scale_y = abs(header["PC2_2"] / np.cos(arg))
    else:
        raise ValueError("...")

    # ...
    pixel_scale = np.sqrt(
        pixel_scale_x * pixel_scale_y
    )


    # # NOTE: Check the units of the pixel scale by looking at these header keys.
    # "CUNIT1"
    # "CUNIT2"

    # NOTE: Can we do this in a more elegant way?
    # NOTE: Should I return a value with units or just a float?
    if units == "deg":
        pass
    elif units == "arcsec":
        pixel_scale = pixel_scale * au.deg.to(au.arcsec)
    else:
        raise NotImplementedError()

    #print("pixel_scale =", pixel_scale)

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


def extract_key_from_fits(filename, key):

    header = fits.getheader(filename=filename)

    if key in header:
        return header[key]
    else:
        raise ValueError(
            "{} was not found in the header".format(key)
        )

def extract_list_of_keys_from_header(header, list_of_keys, error=False):
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

    if not isinstance(list_of_keys, list):
        raise TypeError("It is not a list")

    if list_of_keys is None:
        raise ValueError("The list is empty")

    header_keys = {}
    for key in list_of_keys:
        if key in header:
            header_keys[key] = header[key]
        else:
            if error:
                raise ValueError(
                    "{} was not found in the header".format(key)
                )
            else:
                print(
                    "WARNING: {} was not found in the header".format(key)
                )

    return header_keys

def remove_keys_from_header(header, list_of_keys):

    header_keys = {}
    for key in header:
        print(key, header[key])
        if key not in list_of_keys:
            header_keys[key] = header[key]

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys
    )

def header_from_header_and_list_of_keys(header, list_of_keys):

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys
    )

def filter_header(header, list_of_keys):

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    return updated_header_with_header_keys(
        header=fits.Header(), header_keys=header_keys
    )

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

def updated_header_with_header_keys_from_filename(filename, header_keys, replace=False):
    header = fits.getheader(filename=filename)
    for key in header_keys:
        if key in header:
            pass # TODO: CHECK IF YOU WANT TO FORCE THE REPLACEMENT OF THIS KEY
        else:
            header[key] = header_keys[key]

    data = fits.getdata(filename=filename)

    fits.writeto(
        filename,
        data=data,
        header=header,
        overwrite=True
    )

def get_extent_from_header(header):

    # NOTE:
    # NAXIS1 -> rows
    # NAXIS2 -> cols

    print(
        header["NAXIS1"],
        header["NAXIS2"]
    )
    pixel_scale = get_pixel_scale_from_header(header=header)

    extent = [
        0,
        header["NAXIS2"] * pixel_scale,
        0,
        header["NAXIS1"] * pixel_scale
    ]

    return extent

def extract_keys_from_header_for_2d(header):

    list_of_keys = [
        "BMAJ",
        "BMIN",
        "BPA",
        "PC1_1",
        "PC2_1",
        "PC1_2",
        "PC2_2",
        "CTYPE1",
        "CRVAL1",
        "CDELT1",
        "CRPIX1",
        "CUNIT1",
        "CTYPE2",
        "CRVAL2",
        "CDELT2",
        "CRPIX2",
        "CUNIT2",
    ]

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )

def default_list_of_keys():

    return [
        "BMAJ",
        "BMIN",
        "BPA",
        "PC1_1",
        "PC2_1",
        "PC1_2",
        "PC2_2",
        "CTYPE1",
        "CRVAL1",
        "CDELT1",
        "CRPIX1",
        "CUNIT1",
        "CTYPE2",
        "CRVAL2",
        "CDELT2",
        "CRPIX2",
        "CUNIT2",
    ]

def header_from_header_and_default_list_of_keys(header):

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=default_list_of_keys()
    )

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys
    )

def sanitize_fits(filename, output_filename, flipped=False):

    data = fits.getdata(
        filename=filename
    )

    list_of_keys = [
        "BMAJ",
        "BMIN",
        "BPA",
        "PC1_1",
        "PC2_1",
        "PC1_2",
        "PC2_2",
        "CTYPE1",
        "CRVAL1",
        "CDELT1",
        "CRPIX1",
        "CUNIT1",
        "CTYPE2",
        "CRVAL2",
        "CDELT2",
        "CRPIX2",
        "CUNIT2",
        #"CTYPE3",
        #"CRVAL3",
        #"CDELT3",
        #"CRPIX3",
        #"CUNIT3",
    ]

    header_keys = extract_list_of_keys_from_header(
        header=fits.getheader(
            filename=filename
        ),
        list_of_keys=list_of_keys
    )

    header = updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )

    data = np.squeeze(a=data)
    if flipped:
        data = data[::-1]
    fits.writeto(
        filename=output_filename,
        data=np.squeeze(
            a=data
        ),
        header=header,
        overwrite=True
    )


def sanitize_fits_with_scaling(filename, output_filename, scaling_factor=1.0, flipped=False):

    data = fits.getdata(
        filename=filename
    )

    data *= scaling_factor

    list_of_keys = [
        "BSCALE",
        "BZERO",
        "BMAJ",
        "BMIN",
        "BPA",
        "BUNIT",
        "PC1_1",
        "PC2_1",
        "PC1_2",
        "PC2_2",
        "CTYPE1",
        "CRVAL1",
        "CDELT1",
        "CRPIX1",
        "CUNIT1",
        "CTYPE2",
        "CRVAL2",
        "CDELT2",
        "CRPIX2",
        "CUNIT2",
        #"CTYPE3",
        #"CRVAL3",
        #"CDELT3",
        #"CRPIX3",
        #"CUNIT3",
        "RADESYS",
        "SPECSYS",
        "OBSRA",
        "OBSDEC",
        "OBSGEO-X",
        "OBSGEO-Y",
        "OBSGEO-Z",
    ]

    header = fits.getheader(
        filename=filename
    )

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )
    header = updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )

    data = np.squeeze(a=data)
    if flipped:
        data = data[::-1]
    fits.writeto(
        filename=output_filename,
        data=np.squeeze(
            a=data
        ),
        header=header,
        overwrite=True
    )

# def save_cube_to_fits(
#     CRVAL1,
#     CDELT1,
#     CRPIX1,
#     CRVAL2,
#     CDELT2,
#     CRPIX2,
#     data,
#     directory=None,
#     filename="cube"
# ):
#
#     if len(data.shape) == 3:
#         pass
#     else:
#         raise ValueError
#
#     header = fits.Header()
#     header["CTYPE1"] = "RA---SIN"
#     header["CRVAL1"] = CRVAL1
#     header["CDELT1"] = CDELT1
#     header["CRPIX1"] = CRPIX1
#     header["CUNIT1"] = "deg"
#     header["CTYPE2"] = "DEC--SIN"
#     header["CRVAL2"] = CRVAL2
#     header["CDELT2"] = CDELT2
#     header["CRPIX2"] = CRPIX2
#     header["CUNIT2"] = "deg"
#
#     # # ...
#     # if directory is None:
#     #     filename = "cube.fits"
#     # else:
#     #     if directory[-1] == "/":
#     #         directory = directory[:-1]
#     #     filename = directory + "/cube.fits"
#
#     if directory:
#         # TODO: check if directory exists.
#
#         if directory[-1] == "/":
#             directory = directory[:-1]
#     else:
#         directory = "."
#
#     filename = directory + "/" + filename + ".fits"
#
#     fits.writeto(
#         filename,
#         data=data,
#         header=header,
#         overwrite=True
#     )


def get_wavelengths_from_header(header):

    list_of_keys = [
        "NAXIS3",
        "CRVAL3",
        "CDELT3",
        "CRPIX3"
    ]

    list_of_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    NAXIS3 = list_of_keys["NAXIS3"]
    CRPIX3 = list_of_keys["CRPIX3"]
    CRVAL3 = list_of_keys["CRVAL3"]
    CDELT3 = list_of_keys["CDELT3"]

    # frequencies = np.asarray([CRVAL3 + i * CDELT3
    #     for i in range(1, NAXIS3 + 1)
    # ])
    # NOTE: DS9 ...
    wavelengths = np.asarray([CRVAL3 + i * CDELT3
        for i in range(0, NAXIS3)
    ])

    return wavelengths


def get_frequencies_from_fits(filename, units=au.Hz):
    header = fits.getheader(filename=filename)
    return get_frequencies_from_header(header=header, units=units)

def get_frequencies_from_filename(filename, units=au.Hz):
    return get_frequencies_from_fits(filename=filename, units=units)

def get_frequencies_from_header(header, units=au.Hz):

    list_of_keys = [
        "NAXIS3",
        "CRVAL3",
        "CDELT3",
        "CRPIX3",
        "CUNIT3"
    ]

    list_of_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    NAXIS3 = list_of_keys["NAXIS3"]
    CRPIX3 = list_of_keys["CRPIX3"]
    CRVAL3 = list_of_keys["CRVAL3"]
    CDELT3 = list_of_keys["CDELT3"]
    CUNIT3 = list_of_keys["CUNIT3"]

    # frequencies = np.asarray([CRVAL3 + i * CDELT3
    #     for i in range(1, NAXIS3 + 1)
    # ])
    # NOTE: DS9 ...
    frequencies = np.asarray([CRVAL3 + i * CDELT3
        for i in range(0, NAXIS3)
    ])
    if CUNIT3 == "Hz":
        frequencies = frequencies * au.Hz
    else:
        raise NotImplementedError()

    frequencies = frequencies.to(units)#;print(frequencies);exit()

    return frequencies


def convert_coords(coords, frame):

    skycoords_fk5 = SkyCoord(
        coords_fk5[0],
        coords_fk5[1],
        frame='fk5'
    )

def get_velocities_from_header(
    header,
    frequency_0=None,
    return_frequencies=False
):

    # if "RESTFRQ" is header.keys():
    #     pass
    # else:
    #     raise ValueError()

    frequencies = get_frequencies_from_header(header=header)
    
    #print("frequencies =", frequencies * au.Hz.to(au.GHz))#;exit()

    if frequency_0 is None:
        if "RESTFRQ" in header.keys():
            frequency_0 = header["RESTFRQ"]
        else:
            frequency_0 = np.mean(frequencies)

    velocities = spectral_utils.convert_frequencies_to_velocities(
        frequencies=frequencies, frequency_0=frequency_0
    )
    #print(velocities, velocities[1] - velocities[0])

    if return_frequencies:
        return velocities, frequencies
    return velocities


def get_velocities_from_fits(filename, frequency_0=None):

    return get_velocities_from_header(
        header=fits.getheader(
            filename=filename
        ),
        frequency_0=frequency_0
    )

def recenter(x, y, radius, header, filename=None):

    wcs = WCS(header)

    xpix, ypix = wcs.wcs_world2pix(x, y, 0)
    print(xpix, ypix)


    pixel_scale = get_pixel_scale_from_header(header=header)


    # obj = aplpy.FITSFigure(
    #     filename,
    #     #figure=figure,
    #     hdu=0,
    #     dimensions=[0, 1],
    # )
    # print(
    #     proj_plane_pixel_scales(obj._wcs)
    # )

    radius = radius.to(au.deg).value
    #print(radius, pixel_scale);exit()

    if radius:
        dx_pix = radius / pixel_scale
        dy_pix = radius / pixel_scale

    #print(xpix, dx_pix);exit()
    xmin = xpix - dx_pix
    xmax = xpix + dx_pix
    ymin = ypix - dy_pix
    ymax = ypix + dy_pix

    return xmin, xmax, ymin, ymax

def recenter_from_image(filename_i, filename_j):

    hdu_i = fits.open(filename_i)
    hdu_j = fits.open(filename_j)

    #wcs_i = WCS(hdu_i[0].header)
    #wcs_j = WCS(hdu_j[0].header)

    pixel_scale_i = get_pixel_scale_from_fits(
        filename=filename_i
    )
    pixel_scale_j = get_pixel_scale_from_fits(
        filename=filename_j
    )


    keys = extract_list_of_keys_from_header(
        header=hdu_i[0].header,
        list_of_keys=[
            "NAXIS1",
            "CRVAL1",
            "CRPIX1",
            "NAXIS2",
            "CRVAL2",
            "CRPIX2",
        ],
        error=False
    )

    center = SkyCoord(
        keys["CRVAL1"] * au.deg,
        keys["CRVAL2"] * au.deg,
        frame='icrs'
    )

    radius = keys["NAXIS1"] * pixel_scale_i / 2.0 * au.arcsec

    extent_i = [
        0.0,
        keys["NAXIS1"] * pixel_scale_i,
        0.0,
        keys["NAXIS1"] * pixel_scale_i
    ]

    xmin, \
    xmax, \
    ymin, \
    ymax = recenter(
        x=center.ra,
        y=center.dec,
        radius=radius,
        header=hdu_j[0].header
    )
    # print(
    #     xmin,
    #     xmax,
    #     ymin,
    #     ymax
    # )

    # xmin = int(xmin)
    # xmax = int(xmax)
    # ymin = int(ymin)
    # ymax = int(ymax)
    xmin = int(np.round(xmin))
    xmax = int(np.round(xmax))
    ymin = int(np.round(ymin))
    ymax = int(np.round(ymax))
    # print(
    #     xmin,
    #     xmax,
    #     ymin,
    #     ymax
    # )
    # exit()

    image_i = fits.getdata(filename=filename_i)
    image_j = fits.getdata(filename=filename_j)
    image_i = np.squeeze(image_i)
    image_j = np.squeeze(image_j)

    image_j_recentered = image_j[ymin:ymax, xmin:xmax]

    figure, axes = plt.subplots(nrows=1, ncols=2)


    extent_j = [
        0.0,
        image_j_recentered.shape[0] * pixel_scale_j, 0.0, image_j_recentered.shape[1] * pixel_scale_j]

    print(image_j_recentered.shape)
    print(image_i.shape)
    axes[0].imshow(image_j_recentered, cmap="jet", vmin=-0.005, vmax=0.5, origin="lower", extent=extent_j)
    axes[1].imshow(image_i, cmap="jet", origin="lower", extent=extent_i)
    axes[0].contour(image_i, colors="black", extent=extent_i)
    axes[1].contour(image_i, colors="black", extent=extent_i)

    plt.show()

    exit()


def save_image_with_extent(image, extent):
    pass

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

    # ...
    list_of_keys = [
        "CTYPE3",
        "CRVAL3",
        "CDELT3",
        "CRPIX3",
        "CUNIT3"
    ]

    # ...
    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    print(header_keys)




def get_list_of_keys_for_aplpy(header):

    list_of_keys = [
        "NAXIS1",
        "NAXIS2",
        "CRVAL1",
        "CDELT1",
        "CRPIX1",
        "CTYPE1",
        "CUNIT1",
        "CRVAL2",
        "CDELT2",
        "CRPIX2",
        "CTYPE2",
        "CUNIT2",
        # "PC1_1",
        # "PC2_1",
        # "PC1_2",
        # "PC2_2",
    ]


    return extract_list_of_keys_from_header(
        header=header,
        list_of_keys=list_of_keys
    )

# ----------------------- #
#
# ----------------------- #

def run_tests():

    #test__get_pixel_scale_from_fits()
    test__extract_list_of_keys_from_header()


def func():
    pass


if __name__ == "__main__":


    get_velocities_from_fits(filename="/Volumes/MyPassport_red/2023.1.01354.S_HERMES_J021830.5-053124/imaging_uvcontsub_HERMES_J021830.5-053124/cube/width_60/HERMES_J021830.5-053124_spw_31.dirty.cube.image.pbcor.fits", frequency_0=None)

    filename = "/Users/ccbh87/Downloads/member.uid___A001_X3621_X45c4.SPT0346-52_sci.spw25.mfs.I.pb.fits"
    frequencies = get_frequencies_from_fits(filename=filename, units=au.Hz)
    print(
        np.min(frequencies) * au.Hz.to(au.GHz),
        np.max(frequencies) * au.Hz.to(au.GHz),
    )
    exit()


    filename_f444w = "/Users/ccbh87/Desktop/GitHub/Database/Images/SPT2147-50/jw01355-o024_t004_nircam_clear-f444w_i2d_SCI.fits"
    header_f444w = fits.getheader(filename=filename_f444w)

    from astropy.wcs import WCS
    wcs_f444w = WCS(header_f444w)
    print(wcs_f444w.wcs.pc)
    exit()

    filename_f560w = "/Users/ccbh87/Desktop/GitHub/Database/Images/SPT2147-50/jw01355-o023_t004_miri_f560w_i2d_SCI.fits"
    header_f560w = fits.getheader(filename=filename_f560w)

    filename = "/Users/ccbh87/Desktop/GitHub/Database/Images/SPT2147-50/HST_Spilker_2023/iev704010_drz.fits"
    filename = "/Users/ccbh87/Desktop/GitHub/Database/Images/SPT0418-47/jw01355-o015_t001_miri_f560w_i2d.fits"
    header = fits.getheader(filename=filename, ext=1)

    angle_f444w = angle_from_header(header=header_f444w)
    angle_f560w = angle_from_header(header=header_f560w)
    angle = angle_from_header(header=header)
    print(angle_f444w)
    #print(angle_f560w)
    #print(angle)

    exit()



    # #filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01512.S/science_goal.uid___A001_X1284_X1a8a/group.uid___A001_X1284_X1a8b/member.uid___A001_X1284_X1a8c/product/member.uid___A001_X1284_X1a8c._ALESS068.1__sci.spw25.cube.I.pbcor.fits"
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X35/product/member.uid___A001_X894_X35.SPT-0532_sci.spw25.cube.I.pbcor.fits"
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X35/product/member.uid___A001_X894_X35.SPT-0532_sci.spw27.cube.I.pbcor.fits"
    # frequencies = get_frequencies_from_fits(filename=filename).to(au.GHz)
    # #print((frequencies[0] - frequencies[-1]) * au.Hz.to(au.GHz))
    # print(
    #     "fmin:{}".format(np.min(frequencies)),
    #     "fmax:{}".format(np.max(frequencies))
    # )
    # exit()

    # # NOTE: SPT-0418 (2016.1.01374.S; lres)
    # for filename in [
    #     #"/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2f/product/member.uid___A001_X894_X2f.SPT-0418_sci.spw25.cube.I.pbcor.fits",
    #     #"/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2f/product/member.uid___A001_X894_X2f.SPT-0418_sci.spw27.cube.I.pbcor.fits",
    #
    #     "/Volumes/MyPassport_red/ALMA_data/2016.1.01499.S/science_goal.uid___A001_X87a_X835/group.uid___A001_X87a_X836/member.uid___A001_X87a_X837/product/member.uid___A001_X87a_X837.SPT0418-47_sci.spw25.cube.I.pbcor.fits",
    #     "/Volumes/MyPassport_red/ALMA_data/2016.1.01499.S/science_goal.uid___A001_X87a_X835/group.uid___A001_X87a_X836/member.uid___A001_X87a_X837/product/member.uid___A001_X87a_X837.SPT0418-47_sci.spw27.cube.I.pbcor.fits",
    #     "/Volumes/MyPassport_red/ALMA_data/2016.1.01499.S/science_goal.uid___A001_X87a_X835/group.uid___A001_X87a_X836/member.uid___A001_X87a_X837/product/member.uid___A001_X87a_X837.SPT0418-47_sci.spw29.cube.I.pbcor.fits",
    #     "/Volumes/MyPassport_red/ALMA_data/2016.1.01499.S/science_goal.uid___A001_X87a_X835/group.uid___A001_X87a_X836/member.uid___A001_X87a_X837/product/member.uid___A001_X87a_X837.SPT0418-47_sci.spw31.cube.I.pbcor.fits",
    # ]:
    #     frequencies = get_frequencies_from_fits(filename=filename)
    #     print(
    #         np.min(frequencies) * au.Hz.to(au.GHz),
    #         np.max(frequencies) * au.Hz.to(au.GHz),
    #     )
    # exit()


    filename_j = "/Users/ccbh87/Desktop/GitHub/Database/Images/SPT0532-50/final_drz_sci_F110W_Mattia.fits"
    hdu_j = fits.open(filename_j)
    center = SkyCoord('05h32m51.05s', '-50d47m07.66s', frame='icrs')
    # recenter(
    #     x=center.ra,
    #     y=center.dec,
    #     radius=2.0 * au.arcsec,
    #     header=hdu_j[0].header,
    #     filename=filename_j
    # )

    filename_i = "/Volumes/MyPassport_red/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X35/imaging/temp/temp.image.fits"
    hdu_i = fits.open(filename_i)

    recenter_from_image(
        filename_i=filename_i,
        filename_j=filename_j,
        # x=center.ra,
        # y=center.dec,
        # radius=2.0 * au.arcsec,
        # header=hdu[0].header,
        # filename=filename
    )
    exit()


    # filename = "/Users/ccbh87/Desktop/ALMA_data/2019.1.00663.S/science_goal.uid___A001_X146a_X85/group.uid___A001_X146a_X86/member.uid___A001_X146a_X87/product/member.uid___A001_X146a_X87._J053816-5030.8__sci.spw17.cube.I.pbcor.fits"
    # frequencies = get_frequencies_from_fits(filename=filename)
    # print(frequencies * au.Hz.to(au.GHz))
    #exit()




    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2d/product/member.uid___A001_X894_X2d.SPT-0418_sci.spw21_23_25_27.cont.I.pbcor.fits"
    #
    # pixel_scale = get_pixel_scale_from_fits(
    #     filename=filename
    # )
    # print("pixel_scale = {}".format(pixel_scale))
    # exit()

    # NOTE: Turn this into a function

    #filename = "/Volumes/Elements_v1/2016.1.00450.S/science_goal.uid___A001_X87d_X527/group.uid___A001_X87d_X528/member.uid___A001_X87d_X529/imaging/J142413.9+022304/cube/width_1/J142413.9+022304_spw_0.clean.cube.image.pbcor.fits"
    #filename = "/Volumes/Elements_v1/2016.1.00450.S/science_goal.uid___A001_X87d_X527/group.uid___A001_X87d_X528/member.uid___A001_X87d_X529/imaging/J142413.9+022304/cube/width_1/J142413.9+022304_spw_1.clean.cube.image.pbcor.fits"

    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_50_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_100_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_125_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS067.1/cube/width_100_km_per_s/ALESS067.1_spw_3.clean.cube.image.pbcor.fits"
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01512.S/imaging/ALESS003.1/cube/width_100_km_per_s/ALESS003.1_spws_29_31.clean.cube.image.pbcor.fits"

    #filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01512.S/imaging/ALESS001.1/cube/width_100_km_per_s/ALESS001.1_spw_25_27.clean.cube.image.pbcor.fits"
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01512.S/imaging/ALESS001.1/cube/width_100_km_per_s/ALESS001.1_spw_29_31.clean.cube.image.pbcor.fits"

    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS005.1/cube/width_100_km_per_s/ALESS005.1_spw_3.clean.cube.image.pbcor.fits"

    filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01677.S/science_goal.uid___A001_X1284_X207e/group.uid___A001_X1284_X207f/member.uid___A001_X1284_X2080/product/member.uid___A001_X1284_X2080.Gal3_sci.spw25.cube.I.pbcor.fits"





    list_of_keys = extract_list_of_keys_from_header(
        header=fits.getheader(filename=filename),
        list_of_keys=[
            "NAXIS3",
            "CRVAL3",
            "CDELT3",
        ]
    )

    NAXIS3 = list_of_keys["NAXIS3"]
    CRVAL3 = list_of_keys["CRVAL3"]
    CDELT3 = list_of_keys["CDELT3"]

    # frequencies = [CRVAL3 + i * CDELT3
    #     for i in range(list_of_keys["NAXIS3"])
    # ]
    #
    # print(frequencies)

    min_frequency = CRVAL3
    max_frequency = CRVAL3 + NAXIS3 * CDELT3

    f = min_frequency
    for i in range(NAXIS3):
        print(i, f * au.Hz.to(au.GHz))

        f += CDELT3

    print(
        "min", min_frequency * au.Hz.to(au.GHz),
        "max", max_frequency * au.Hz.to(au.GHz),
    )

    frequencies = get_frequencies_from_fits(filename=filename)
    print(len(frequencies))

    """# NOTE: Make this a function
    def add_images(filenames, ):
        pass

        cubes = []
        for name in filenames:
            hdu = fits.open(name=name)

            print(hdu[0].header["CRVAL1"], hdu[0].header["CRVAL2"])

            print(hdu[0].data.shape)

            cubes.append(hdu[0].data)

        cube = np.add(cubes[0], cubes[1])

        #print(cube.shape)
        # 1) load the image
        # 2) align the images
        # 3) add the images

        for i in range(cube.shape[1]):

            figure, axes = plt.subplots(nrows=1, ncols=3, figsize=(16, 8))

            vmin = np.nanmin(cube[0, i, :, :])
            vmax = np.nanmax(cube[0, i, :, :])

            axes[0].imshow(cube[0, i, :, :], origin="lower", vmin=vmin, vmax=vmax)
            axes[1].imshow(cubes[0][0, i, :, :], origin="lower", vmin=vmin, vmax=vmax)
            axes[2].imshow(cubes[1][0, i, :, :], origin="lower", vmin=vmin, vmax=vmax)
            plt.show()





    add_images(
        filenames=[
            "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_500klambda_niter_5000.clean.cube.image.pbcor.fits",
            "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_500klambda_niter_5000.clean.cube.image.pbcor.fits"
        ]
    )
    exit()
    """
