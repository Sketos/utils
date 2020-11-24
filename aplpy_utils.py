import os as os
import numpy as np
import matplotlib.pyplot as plt

from astropy import units
from astropy.io import fits
from astropy.coordinates import SkyCoord

import aplpy

import fits_utils as fits_utils


def export_sanitized_slice(filename, output_filename, slice):

    data = fits.getdata(
        filename=filename
    )

    data = np.squeeze(data)

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
    ]

    header_keys = fits_utils.extract_list_of_keys_from_header(
        header=fits.getheader(
            filename=filename
        ),
        list_of_keys=list_of_keys
    )

    header = fits_utils.updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )


    fits.writeto(
        filename=output_filename,
        data=data[slice, :, :],
        header=header,
        overwrite=True
    )

def sanitize_from_list_of_keys(filename, output_filename, list_of_keys):

    data = fits.getdata(
        filename=filename
    )

    header_keys = fits_utils.extract_list_of_keys_from_header(
        header=fits.getheader(
            filename=filename
        ),
        list_of_keys=list_of_keys
    )

    header = fits_utils.updated_header_with_header_keys(
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




def sanitize(filename, output_filename):

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
    ]

    header_keys = fits_utils.extract_list_of_keys_from_header(
        header=fits.getheader(
            filename=filename
        ),
        list_of_keys=list_of_keys
    )

    header = fits_utils.updated_header_with_header_keys(
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



"""
figure = plt.figure(
    figsize=(12, 4)
)


#filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/product/member.uid___A001_X894_X33.SPT-0532_sci.spw21_23_25_27.cont.I.pbcor.fits"
#filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/product/member.uid___A001_X894_X39._SPT-S_J053816-5030.8__sci.spw21_23_25_27.cont.I.pbcor.fits"
filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2d/product/member.uid___A001_X894_X2d.SPT-0418_sci.spw21_23_25_27.cont.I.pbcor.fits"


output_filename = "image_1.fits"
sanitize(
    filename=filename,
    output_filename=output_filename
)



x0 = 0.05
y0 = 0.05
dx = 0.3
dy = 0.9

#figure.text(x=x0 + 0.0125, y=dy - 0.0125, s="SPT-0532", color="black", weight="bold", fontsize=17.5)

f1 = aplpy.FITSFigure(
    output_filename,
    figure=figure,
    subplot=[
        x0,
        y0,
        dx,
        dy],
    hdu=0,
)

# ra = 5:32:51.05
# dec = -50:47:07.65



#centre = SkyCoord('05h32m51.05s', '-50d47m07.65s', frame='icrs')
#centre = SkyCoord('05h38m16.81s', '-50d30m51.94s', frame='icrs')
centre = SkyCoord('04h18m39.68s', '-47d51m52.69s', frame='icrs')
#print(centre.ra.deg, centre.dec.deg)
radius = 2.0 * units.arcsec
f1.recenter(
    centre.ra.deg,
    centre.dec.deg,
    radius=radius.to(units.deg).value
)
f1.show_colorscale(cmap="jet", vmin=-0.00002, vmax=0.0002)

f1.tick_labels.hide_x()
f1.tick_labels.hide_y()
f1.axis_labels.hide_x()
f1.axis_labels.hide_y()

# f1.ticks.set_color("black")
# f1.ticks.set_length(8)
# f1.ticks.set_linewidth(1.25)

f1.add_scalebar(0.5*units.arcsec)
f1.scalebar.set_label("0.5$^{\prime\prime}$")
f1.add_beam()
f1.beam.set_color("black")
plt.show()
"""


def func(
    sources,
    centres,
    radii,
    colorscales,
    figsize,
    nrows,
    ncols,
    x0,
    y0
):

    if nrows * ncols < len(sources):
        raise ValueError("...")

    figure = plt.figure(
        figsize=figsize
    )

    dx = (1.0 - 2.0 * x0) / ncols
    dy = (1.0 - 2.0 * y0) / nrows

    # k = 0
    # for i in range(nrows):
    #     for j in range(ncols):
    #
    #         k += 1

    for i, source in enumerate(sources):
        output_filename = "image_{}.fits".format(i)

        figure.text(
            x=x0 + i * dx + 0.0125,
            y=dy - 0.025,
            s=source.name,
            color="w",
            weight="bold",
            fontsize=17.5
        )

        sanitize(
            filename=source.filename,
            output_filename=output_filename
        )

        f = aplpy.FITSFigure(
            output_filename,
            figure=figure,
            subplot=[
                x0 + i * dx,
                y0,
                dx,
                dy],
            hdu=0,
        )


        centre = centres[i]
        radius = radii[i]


        f.recenter(
            centre.ra.deg,
            centre.dec.deg,
            radius=radius.to(units.deg).value
        )

        colorscale = colorscales[i]

        f.show_colorscale(
            cmap=colorscale.cmap,
            vmin=colorscale.vmin,
            vmax=colorscale.vmax
        )

        f.tick_labels.hide_x()
        f.tick_labels.hide_y()
        f.axis_labels.hide_x()
        f.axis_labels.hide_y()

        f.add_scalebar(0.5*units.arcsec)
        f.scalebar.set_label("0.5$^{\prime\prime}$")
        f.scalebar.set_color("w")
        f.add_beam()
        f.beam.set_color("w")

    plt.subplots_adjust(
        left=0.1, bottom=0.1, right=0.9, top=0.9
    )
    plt.show()


class source:

    def __init__(self, filename, name):

        if os.path.isfile(filename):
            self.filename = filename
        else:
            raise IOError(
                "File does not exist"
            )

        self.name = name


class colorscale:

    def __init__(self, cmap, vmin, vmax):

        self.cmap = cmap

        self.vmin = vmin
        self.vmax = vmax


class figsize:

    def __init__(self, centre, radius):

        # NOTE: Check that this is a SkyCoord object.
        self.centre = centre

        # NOTE: Check that this has units
        self.radius = radius


class beam:

    def __init__(self):
        pass

# class test_class:
#
#     def __init__(self, filename, centre, radius, vmin, vmax, ):
#         pass



if __name__ == "__main__":

    """
    sources = [
        source(
            filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/product/member.uid___A001_X894_X33.SPT-0532_sci.spw21_23_25_27.cont.I.pbcor.fits",
            name="SPT-0532"
        ),
        source(
            filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/product/member.uid___A001_X894_X39._SPT-S_J053816-5030.8__sci.spw21_23_25_27.cont.I.pbcor.fits",
            name="SPT-S J053816-5030.8"
        ),
        source(
            filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2d/product/member.uid___A001_X894_X2d.SPT-0418_sci.spw21_23_25_27.cont.I.pbcor.fits",
            name="SPT-0418"
        ),
    ]



    centres = [
        SkyCoord('05h32m51.05s', '-50d47m07.65s', frame='icrs'),
        SkyCoord('05h38m16.81s', '-50d30m51.94s', frame='icrs'),
        SkyCoord('04h18m39.68s', '-47d51m52.69s', frame='icrs')
    ]



    radii = [
        1.00 * units.arcsec,
        2.75 * units.arcsec,
        2.00 * units.arcsec
    ]

    colorscales = [
        colorscale(cmap="cividis", vmin=-0.000050, vmax=0.000750),
        colorscale(cmap="cividis", vmin=-0.000025, vmax=0.000325),
        colorscale(cmap="cividis", vmin=-0.000005, vmax=0.000200),
    ]

    func(
        sources=sources,
        centres=centres,
        radii=radii,
        colorscales=colorscales,
        figsize=(12, 4),
        nrows=1,
        ncols=3,
        x0=0.05,
        y0=0.05
    )
    """

    figure = plt.figure(
        figsize=(16, 6)
    )

    uv_taper = "500klambda"
    #uv_taper = "1000klambda"

    niter = 5000

    if niter == 0:
        filename_0 = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01093.S/science_goal.uid___A001_X899_X8b/group.uid___A001_X899_X8c/member.uid___A001_X899_X8f/imaging/CASA_5.6.1/cube/temp/temp_{}.image.pbcor.fits".format(uv_taper)
    else:
        filename_0 = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01093.S/science_goal.uid___A001_X899_X8b/group.uid___A001_X899_X8c/member.uid___A001_X899_X8f/imaging/CASA_5.6.1/cube/temp/temp_{}_niter_{}.image.pbcor.fits".format(
            uv_taper, niter
        )
    if niter == 0:
        filename_1 = "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_{}.clean.cube.image.pbcor.fits".format(uv_taper)
    else:
        filename_1 = "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_{}_niter_{}.clean.cube.image.pbcor.fits".format(
            uv_taper, niter
        )
    if niter == 0:
        filename_2 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}.clean.cube.image.pbcor.fits".format(uv_taper)
    else:
        filename_2 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}_niter_{}.clean.cube.image.pbcor.fits".format(
            uv_taper, niter
        )
        # filename_2 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}_niter_{}_threshold_0.40mJy.clean.cube.image.pbcor.fits".format(
        #     uv_taper, niter
        # )

    # # NOTE: THIS IS A TEST
    # filename_0 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}_niter_{}.clean.cube.image.pbcor.fits".format(
    #     uv_taper, niter
    # )
    # filename_1 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}_niter_{}_threshold_0.40mJy.clean.cube.image.pbcor.fits".format(
    #     uv_taper, niter
    # )
    # filename_2 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}_niter_{}_threshold_0.80mJy.clean.cube.image.pbcor.fits".format(
    #     uv_taper, niter
    # )

    slice = 13

    if niter == 0:
        output_filename_0 = "./SDP81_{}_CII_slice_{}.fits".format(uv_taper, slice)
    else:
        output_filename_0 = "./SDP81_{}_niter_{}_CII_slice_{}.fits".format(uv_taper, niter, slice)
    if niter == 0:
        output_filename_1 = "./SDP81_{}_CO54_slice_{}.fits".format(uv_taper, slice)
    else:
        output_filename_1 = "./SDP81_{}_niter_{}_CO54_slice_{}.fits".format(uv_taper, niter, slice)
    if niter == 0:
        output_filename_2 = "./SDP81_{}_CO87_slice_{}.fits".format(uv_taper, slice)
    else:
        output_filename_2 = "./SDP81_{}_niter_{}_CO87_slice_{}.fits".format(uv_taper, niter, slice)


    export_sanitized_slice(
        filename=filename_0,
        output_filename=output_filename_0,
        slice=slice
    )
    export_sanitized_slice(
        filename=filename_1,
        output_filename=output_filename_1,
        slice=slice
    )
    export_sanitized_slice(
        filename=filename_2,
        output_filename=output_filename_2,
        slice=slice
    )

    ncols = 3
    nrows = 1
    x0 = 0.05
    y0 = 0.05

    dx = (1.0 - 2.0 * x0) / ncols
    dy = (1.0 - 2.0 * y0) / nrows

    velocity_min = -600
    dv = 50
    velocity = velocity_min + slice * dv

    i = 0
    figure.text(
        x=x0 + i * dx + 0.0125,
        y=dy - 0.025,
        s=r"$C_{II}$",
        color="black",
        weight="bold",
        fontsize=25.0
    )
    figure.text(
        x=x0 + i * dx + 0.0125,
        y=y0 + 0.025,
        s="v = {} km / s".format(velocity),
        color="black",
        fontsize=25.0
    )
    f_0 = aplpy.FITSFigure(
        output_filename_0,
        figure=figure,
        hdu=0,
        dimensions=[0, 1],
        subplot=[
            x0 + i * dx,
            y0,
            dx,
            dy],
    )

    i = 1
    figure.text(
        x=x0 + i * dx + 0.0125,
        y=dy - 0.025,
        s="CO (J = 5 - 4)",
        color="black",
        weight="bold",
        fontsize=25.0
    )
    f_1 = aplpy.FITSFigure(
        output_filename_1,
        figure=figure,
        hdu=0,
        dimensions=[0, 1],
        subplot=[
            x0 + i * dx,
            y0,
            dx,
            dy],
    )

    i = 2
    figure.text(
        x=x0 + i * dx + 0.0125,
        y=dy - 0.025,
        s="CO (J = 8 - 7)",
        color="black",
        weight="bold",
        fontsize=25.0
    )
    f_2 = aplpy.FITSFigure(
        output_filename_2,
        figure=figure,
        hdu=0,
        dimensions=[0, 1],
        subplot=[
            x0 + i * dx,
            y0,
            dx,
            dy],
    )

    centre = SkyCoord('09h03m11.58s', '00d39m06.58s', frame='icrs')
    radius = 3.0 * units.arcsec

    f_0.recenter(
        centre.ra.deg,
        centre.dec.deg,
        radius=radius.to(units.deg).value
    )
    f_1.recenter(
        centre.ra.deg,
        centre.dec.deg,
        radius=radius.to(units.deg).value
    )
    f_2.recenter(
        centre.ra.deg,
        centre.dec.deg,
        radius=radius.to(units.deg).value
    )

    f_0.show_colorscale(cmap="jet",)
    f_1.show_colorscale(cmap="jet",)
    f_2.show_colorscale(cmap="jet",)

    f_1.tick_labels.hide_x()
    f_1.tick_labels.hide_y()
    f_1.axis_labels.hide_x()
    f_1.axis_labels.hide_y()
    f_2.tick_labels.hide_x()
    f_2.tick_labels.hide_y()
    f_2.axis_labels.hide_x()
    f_2.axis_labels.hide_y()

    f_0.add_scalebar(0.5*units.arcsec)
    f_0.scalebar.set_label("0.5$^{\prime\prime}$")
    f_0.scalebar.set_color("black")
    f_1.add_scalebar(0.5*units.arcsec)
    f_1.scalebar.set_label("0.5$^{\prime\prime}$")
    f_1.scalebar.set_color("black")
    f_2.add_scalebar(0.5*units.arcsec)
    f_2.scalebar.set_label("0.5$^{\prime\prime}$")
    f_2.scalebar.set_color("black")

    plt.subplots_adjust(
        left=0.1, bottom=0.1, right=0.9, top=0.9
    )

    # if niter == 0:
    #     plt.savefig(
    #         "SDP81_{}_{}.png".format(
    #             uv_taper, velocity
    #         ),
    #         overwrite=True
    #     )
    # else:
    #     plt.savefig(
    #         "SDP81_{}_niter_{}_{}.png".format(
    #             uv_taper, niter, velocity
    #         ),
    #         overwrite=True
    #     )
    plt.show()
