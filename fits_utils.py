import copy

import numpy as np

import matplotlib.pyplot as plt

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


def sanitize_fits(filename, output_filename):

    data = fits.getdata(
        filename=filename
    )

    list_of_keys=[
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
        "CTYPE3",
        "CRVAL3",
        "CDELT3",
        "CRPIX3",
        "CUNIT3",
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

# ----------------------- #
#
# ----------------------- #

def run_tests():

    #test__get_pixel_scale_from_fits()
    test__extract_list_of_keys_from_header()


if __name__ == "__main__":
    pass
    #run_tests()

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
    filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_125_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"

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
