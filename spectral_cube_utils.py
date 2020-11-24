import os
import sys
import copy

import numpy as np
import matplotlib.pyplot as plt

from astropy import units

from spectral_cube import SpectralCube


sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)
import plot_utils as plot_utils
import spectral_utils as spectral_utils


# def mask_cube(cube, mask):
#
#     if cube.shape[1:] == mask.shape:
#         pass
#     else:
#         raise ValueError(
#             "The shapes of the cube and mask are not the same"
#         )

def mask(cube, threshold):

    return cube.with_mask(
        cube > threshold * cube.unit
    )


def moment(
    cube,
    order=0,
    f_min=None,
    f_max=None,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
):

    masked_cube = cube.with_mask(
        cube > f_min * cube.unit,
        cube < f_max * cube.unit
    )

    #sub_masked_cube = masked_cube[z_min:z_max, y_min:y_max, x_min:x_max]

    moment_0 = sub_masked_cube.moment(
        order=order
    )

if __name__ == "__main__":


    CO_transition_frequencies = {
        "1-0": 115.271,
        "2-1": 230.538,
        "3-2": 345.796,
        "4-3": 461.041,
        "5-4": 576.268,
        "6-5": 691.473,
        "7-6": 806.652,
        "8-7": 921.800,
        "9-8": 1036.912,
    }

    CI_transition_frequencies = {
        "1-0": 492.1607,
        "2-1": 809.3435,
    }

    H20_transition_frequencies = {
        "1_11-0_00": 1113.343,
        "2_02-1_11": 987.927,
        "2_11-2_02": 752.033,
        "2_20-2_11": 1228.789,
        "3_12-3_03": 1097.365,
        "3_21-3_12": 1162.912,
        "4_22-4_13": 1207.639,
        "5_23-5_12": 1410.618,
    }

    # ID = "2017.1.01163.S"
    # science_goal = "uid___A001_X1288_X127"
    # group = "uid___A001_X1288_X128"
    # member = "uid___A001_X1288_X129"
    #
    # # ID = "2016.1.00754.S"
    # # science_goal = "uid___A001_X87a_Xad"
    # # group = "uid___A001_X87a_Xae"
    # # member = "uid___A001_X87a_Xaf"
    #
    # directory = "/Users/ccbh87/Desktop/ALMA_data/{}/science_goal.{}/group.{}/member.{}/product".format(
    #     ID,
    #     science_goal,
    #     group,
    #     member
    # )
    #
    # spw = 23
    # filename = "member.uid___A001_X1288_X129._ALESS_006.1__sci.spw{}.cube.I.pbcor.fits".format(spw)
    #
    #
    # cube = SpectralCube.read(
    #     "{}/{}".format(directory, filename)
    # )


    """
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01093.S/science_goal.uid___A001_X899_X8b/group.uid___A001_X899_X8c/member.uid___A001_X899_X8f/product/SDP.81_spw3_CIIb05.cl01.pbcor.fits"
    filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_006.1/ALESS_006.1_spw_23.clean.cube.image.pbcor.fits"
    cube = SpectralCube.read(filename)


    masked_cube = cube.with_mask(cube > 0.0085 * cube.unit, cube < 0.25 * cube.unit)
    #masked_cube = cube

    # x_min = 250
    # x_max = 750
    # y_min = 250
    # y_max = 750

    # x_min = 140
    # x_max = 280
    # y_min = 140
    # y_max = 280
    # z_min = 15
    # z_max = 45
    #
    # sub_masked_cube = masked_cube[z_min:z_max, y_min:y_max, x_min:x_max]
    # #print(sub_masked_cube._data)

    #plot_utils.plot_cube(cube=sub_masked_cube._data, ncols=20)

    moment_0 = masked_cube.moment(order=0)

    plt.figure()
    plt.imshow(moment_0.value)
    plt.colorbar()
    plt.show()
    """


    # filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_006.1/ALESS_006.1_spw_23.clean.cube.image.pbcor.fits"
    # cube = SpectralCube.read(filename)
    #
    #
    # masked_cube = cube.with_mask(cube > 0.0005 * cube.unit, cube < 0.1 * cube.unit)
    # #masked_cube = cube
    #
    # # x_min = 250
    # # x_max = 750
    # # y_min = 250
    # # y_max = 750
    #
    # # x_min = 140
    # # x_max = 280
    # # y_min = 140
    # # y_max = 280
    # z_min = 35
    # z_max = 60
    #
    # sub_cube = cube[z_min:z_max, :, :]
    # sub_masked_cube = masked_cube[z_min:z_max, :, :]
    #
    #
    # #plot_utils.plot_cube(cube=sub_masked_cube._data, ncols=20)
    #
    # moment_0 = sub_cube.moment(order=0)
    # moment_1 = sub_masked_cube.moment(order=1)
    #
    # figure, axes = plt.subplots(nrows=1, ncols=2)
    # axes[0].imshow(moment_0.value, cmap="jet")
    # axes[1].imshow(moment_1.value, cmap="jet")
    # plt.show()

    def moments(
        filename,
        z_min,
        z_max,
        f_min=None,
        f_max=None,
        xlim_min=None,
        xlim_max=None,
        ylim_min=None,
        ylim_max=None,
        vmin_moment_1=None,
        vmax_moment_1=None,
        rest_value=None,
        subtitle=None
    ):
        cube = SpectralCube.read(filename)


        if rest_value is not None:
            cube = cube.with_spectral_unit(
                units.km / units.s,
                velocity_convention='radio',
                rest_value=rest_value * units.GHz
            )


        sub_cube = cube[z_min:z_max, :, :]

        moment_0 = sub_cube.moment(order=0)

        masked_cube = cube.with_mask(
            cube > f_min * cube.unit,
            cube < f_max * cube.unit
        )
        sub_masked_cube = masked_cube[z_min:z_max, :, :]

        # plt.imshow(moment_0.value, cmap="jet")
        # plt.show()

        moment_1 = sub_masked_cube.moment(order=1)
        moment_2 = sub_masked_cube.moment(order=2)

        figure, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

        if subtitle is not None:
            figure.suptitle(subtitle, fontsize=20, fontweight='bold')

        moment_0_map = moment_0.value
        moment_1_map = moment_1.value
        moment_2_map = moment_2.value
        axes[0].imshow(moment_0_map, cmap="jet", origin="lower")
        axes[1].imshow(moment_1_map, cmap="jet", origin="lower", vmin=vmin_moment_1, vmax=vmax_moment_1)
        axes[2].imshow(moment_2_map, cmap="jet", origin="lower")


        moment_0_map_max = np.max(moment_0_map)
        levels = [percentage * moment_0_map_max
            for percentage in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.0]
        ]

        axes[1].contour(moment_0_map, levels=levels, origin="lower", colors="black", alpha=0.5)
        axes[2].contour(moment_0_map, levels=levels, origin="lower", colors="black", alpha=0.5)

        axes[0].set_xticks([])
        axes[0].set_yticks([])
        axes[1].set_xticks([])
        axes[1].set_yticks([])
        axes[2].set_xticks([])
        axes[2].set_yticks([])

        if xlim_min is not None and xlim_max is not None:
            axes[0].set_xlim((xlim_min, xlim_max))
            axes[1].set_xlim((xlim_min, xlim_max))
            axes[2].set_xlim((xlim_min, xlim_max))
        if ylim_min is not None and ylim_max is not None:
            axes[0].set_ylim((ylim_min, ylim_max))
            axes[1].set_ylim((ylim_min, ylim_max))
            axes[2].set_ylim((ylim_min, ylim_max))

        plt.subplots_adjust(wspace=0.0, hspace=0.0, bottom=0.05, top=0.95)
        plt.show()


    # #filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/product/member.uid___A001_X1288_X125._ALESS_061.1__sci.spw17.cube.I.pbcor.fits"
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_061.1/ALESS_061.1_spw_17.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=44,
    #     z_max=66,
    #     f_min=0.0005,
    #     f_max=0.1
    # )

    # #filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/product/member.uid___A001_X1288_X125._ALESS_065.1__sci.spw17.cube.I.pbcor.fits"
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_065.1/ALESS_065.1_spw_17.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=80,
    #     z_max=95,
    #     f_min=4.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=205,
    #     xlim_max=305,
    #     ylim_min=210,
    #     ylim_max=310,
    #     subtitle="ALESS 65.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["4-3"],
    #         redshift=4.445386331850715
    #     )
    # )



    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_088.1/ALESS_088.1_spw_23.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=85,
    #     z_max=110,
    #     f_min=4.0 * 10**-4.0,
    #     f_max=1.0
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_066.1/ALESS_066.1_spw_21.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=50,
    #     z_max=78,
    #     f_min=4.0 * 10**-4.0,
    #     f_max=1.0
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_101.1/ALESS_101.1_spw_23.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=10,
    #     z_max=30,
    #     f_min=5.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=200,
    #     xlim_max=300,
    #     ylim_min=200,
    #     ylim_max=300,
    #     subtitle="ALESS 101.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.353081402886241
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_006.1/ALESS_006.1_spw_23.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=36,
    #     z_max=58,
    #     f_min=6.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=128 - 32,
    #     xlim_max=128 + 32,
    #     ylim_min=128 - 32,
    #     ylim_max=128 + 32,
    #     vmin_moment_1=-250,
    #     vmax_moment_1=500.0,
    #     subtitle="ALESS 006.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.3368
    #     )
    # )


    # filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging/ALESS71_spw_0.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=36,
    #     z_max=60,
    #     f_min=7.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=600,
    #     xlim_max=1024,
    #     ylim_min=0,
    #     ylim_max=1024-600,
    #     vmin_moment_1=-250,
    #     vmax_moment_1=500.0,
    #     subtitle="ALESS 071.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["4-3"],
    #         redshift=3.7072348210731896
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_061.1/ALESS_061.1_spw_17.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=30,
    #     z_max=55,
    #     f_min=2.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=128 - 32,
    #     xlim_max=128 + 32,
    #     ylim_min=128 - 32,
    #     ylim_max=128 + 32,
    #     vmin_moment_1=-250,
    #     vmax_moment_1=250.0,
    #     subtitle="ALESS 061.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["4-3"],
    #         redshift=4.404619745761362
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_017.1/ALESS_017.1_spw_17.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=58,
    #     z_max=68,
    #     f_min=4.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64 - 16,
    #     xlim_max=256 + 64 - 16,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-75,
    #     vmax_moment_1=75.0,
    #     subtitle="ALESS 017.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["2-1"],
    #         redshift=1.5382506587318503
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_066.1/ALESS_066.1_spw_21.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=60,
    #     z_max=72,
    #     f_min=4.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-85,
    #     vmax_moment_1=85.0,
    #     subtitle="ALESS 066.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.552637057238822
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_065.1/ALESS_065.1_spw_17.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=80,
    #     z_max=100,
    #     f_min=4.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-150,
    #     vmax_moment_1=250.0,
    #     subtitle="ALESS 065.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["4-3"],
    #         redshift=4.445386331850715
    #     )
    # )


    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_062.2/ALESS_062.2_spw_21.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=75,
    #     z_max=90,
    #     f_min=4.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-150,
    #     vmax_moment_1=250.0,
    #     subtitle="ALESS 062.2",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["2-1"],
    #         redshift=1.3619760544602344
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/imaging/ALESS_098.1/ALESS_098.1_spw_21.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=42,
    #     z_max=62,
    #     f_min=4.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-150,
    #     vmax_moment_1=250.0,
    #     subtitle="ALESS 098.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["2-1"],
    #         redshift=1.3739182340970815
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_112.1/ALESS_112.1_spw_23.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=82,
    #     z_max=105,
    #     f_min=4.5 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-200,
    #     vmax_moment_1=350.0,
    #     subtitle="ALESS 112.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.31350142764345
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS031.1/cube/concatenated/width_100_km_per_s/ALESS031.1.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=30,
    #     z_max=45,
    #     f_min=5.0 * 10**-4.0,
    #     f_max=1.0,
    #     vmin_moment_1=-200,
    #     vmax_moment_1=350.0,
    #     subtitle="ALESS 31.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["4-3"],
    #         redshift=3.7123788087268546
    #     )
    # )

    # #filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xbf/group.uid___A001_X879_Xc0/member.uid___A001_X879_Xc1/product/member.uid___A001_X879_Xc1.ALESS031.1_spw2.image.pbcor.fits"
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS031.1/cube/width_100_km_per_s/ALESS031.1_spws_2_and_1.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=0,
    #     z_max=12,
    #     f_min=1.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=128 - 32,
    #     xlim_max=128 + 32,
    #     ylim_min=128 - 32,
    #     ylim_max=128 + 32,
    #     vmin_moment_1=-200,
    #     vmax_moment_1=350.0,
    #     subtitle="ALESS 31.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CI_transition_frequencies["1-0"],
    #         redshift=3.7123788087268546
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_101.1/ALESS_101.1_spw_23.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=10,
    #     z_max=28,
    #     f_min=5.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-200,
    #     vmax_moment_1=350.0,
    #     subtitle="ALESS 101.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.353081402886241
    #     )
    # )


    # filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_088.1/ALESS_088.1_spw_23.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=80,
    #     z_max=110,
    #     f_min=5.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-200,
    #     vmax_moment_1=350.0,
    #     subtitle="ALESS 88.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["2-1"],
    #         redshift=1.2064590753698612
    #     )
    # )

    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS035.1/cube/width_100_km_per_s/ALESS035.1_spw_1.clean.cube.image.fits"
    # moments(
    #     filename=filename,
    #     z_min=25,
    #     z_max=35,
    #     f_min=6.75 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-350,
    #     vmax_moment_1=200.0,
    #     subtitle="ALESS 035.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.9737
    #     )
    # )

    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS022.1/cube/width_50_km_per_s/ALESS022.1_spw_3.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=59,
    #     z_max=87,
    #     f_min=1.25 * 10**-3.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-150,
    #     vmax_moment_1=200.0,
    #     subtitle="ALESS 022.1",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["3-2"],
    #         redshift=2.2625397005822103
    #     )
    # )

    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_50_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    # z_min = 80
    # z_max = 100
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_100_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    # z_min = 38
    # z_max = 55
    filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS009.1/cube/width_125_km_per_s/ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    z_min = 31
    z_max = 44
    moments(
        filename=filename,
        z_min=z_min,
        z_max=z_max,
        f_min=7.5 * 10**-4.0,
        f_max=1.0,
        xlim_min=256 - 64,
        xlim_max=256 + 64,
        ylim_min=256 - 64,
        ylim_max=256 + 64,
        vmin_moment_1=-250,
        vmax_moment_1=100.0,
        subtitle="ALESS 009.1",
        rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
            frequency=CO_transition_frequencies["4-3"],
            redshift=3.6937454213160446
        )
    )



    # filename = "/Volumes/Elements_v1/2016.1.00450.S/science_goal.uid___A001_X87d_X527/group.uid___A001_X87d_X528/member.uid___A001_X87d_X529/imaging/J142413.9+022304/cube/width_1/J142413.9+022304_spw_0_contsub.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=30,
    #     z_max=58,
    #     f_min=2.5 * 10**-4.0,
    #     f_max=1.0,
    #     vmin_moment_1=-350,
    #     vmax_moment_1=350.0,
    #     subtitle="ID 141",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=H20_transition_frequencies["2_11-2_02"],
    #         redshift=4.243
    #     )
    # )





    #filename = "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_500klambda.clean.cube.image.pbcor.fits"
    # filename = "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_1000klambda_niter_5000.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=5,
    #     z_max=18,
    #     f_min=3.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-350,
    #     vmax_moment_1=200.0,
    #     subtitle="SDP.81",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["5-4"],
    #         redshift=3.042
    #     )
    # )

    # #filename = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_500klambda.clean.cube.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=5,
    #     z_max=18,
    #     f_min=1.0 * 10**-4.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-350,
    #     vmax_moment_1=200.0,
    #     subtitle="SDP.81",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=CO_transition_frequencies["8-7"],
    #         redshift=3.042
    #     )
    # )

    # filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.01093.S/science_goal.uid___A001_X899_X8b/group.uid___A001_X899_X8c/member.uid___A001_X899_X8f/imaging/CASA_5.6.1/cube/temp/temp_500klambda.image.pbcor.fits"
    # moments(
    #     filename=filename,
    #     z_min=5,
    #     z_max=18,
    #     f_min=5.0 * 10**-3.0,
    #     f_max=1.0,
    #     xlim_min=256 - 64,
    #     xlim_max=256 + 64,
    #     ylim_min=256 - 64,
    #     ylim_max=256 + 64,
    #     vmin_moment_1=-350,
    #     vmax_moment_1=200.0,
    #     subtitle="SDP.81",
    #     rest_value=spectral_utils.observed_line_frequency_from_rest_line_frequency(
    #         frequency=1900.537,
    #         redshift=3.042
    #     )
    # )









    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/imaging/ALESS41_spw_2.clean.cube.image.pbcor.reframe.image.pbcor.fits"
    # cube = SpectralCube.read(filename)
    #
    # print(cube.header["RESTFRQ"])
    # #print(vars(cube))
    #
    #
    # velocities = spectral_utils.convert_frequencies_to_velocities(
    #     frequencies=cube.spectral_axis,
    #     frequency_0=cube.header["RESTFRQ"] * units.Hz,
    # )
    # print(velocities)
    #
    # cube = cube.with_spectral_unit(units.km / units.s, velocity_convention='radio')
    # print(cube.spectral_axis)
    # exit()
    #
    # masked_cube = cube.with_mask(cube > 2.0 * 10**-4.0 * cube.unit, cube < 0.1 * cube.unit)
    # #masked_cube = cube
    #
    # # x_min = 250
    # # x_max = 750
    # # y_min = 250
    # # y_max = 750
    #
    # # x_min = 140
    # # x_max = 280
    # # y_min = 140
    # # y_max = 280
    # z_min = 44
    # z_max = 66
    #
    # sub_masked_cube = masked_cube[z_min:z_max, :, :]
    # print(sub_masked_cube._data.shape)
    #
    # #plot_utils.plot_cube(cube=sub_masked_cube._data, ncols=20)
    #
    # #moment_0 = sub_masked_cube.moment(order=0)
    # moment_1 = sub_masked_cube.moment(order=1)
    #
    # # plt.figure()
    # # plt.imshow(moment_1.value, origin="lower", cmap="jet")
    # # plt.colorbar()
    # # plt.show()
    #
    # #print(vars(masked_cube.mask._mask1._mask1._data))
    #
    # #plot_utils.plot_cube(cube=masked_cube.mask._mask1._mask1._data, ncols=20)
    #
    #
    # # moment_1_MINE = spectral_utils.moment_1(
    # #     cube=copy.copy(sub_masked_cube._data),
    # #     velocities=sub_masked_cube.spectral_axis.to(units.km / units.s).value,
    # #     f_min=4.0 * 10**-4.0,
    # #     axis=0
    # # )
    # #
    # # plt.figure()
    # # plt.imshow(moment_1_MINE, origin="lower", cmap="jet")
    # # plt.colorbar()
    # # plt.show()
