import copy as copy
import numpy as np
import matplotlib.pyplot as plt
from getdist import mcsamples, plots
import corner as corner

import matplotlib
matplotlib.use('QT5Agg')

import directory_utils as directory_utils



def get_contours_from_samples(samples, parameter_1="galaxies_subhalo_mass_centre_1", parameter_2="galaxies_subhalo_mass_centre_0"):

    density2D = samples.get2DDensity(
        x=parameter_1,
        y=parameter_2
    )

    if density2D is not None:
        return density2D.x, density2D.y, density2D.P
    return None


def get_list_of_contours_from_list_of_samples(list_of_samples, parameter_1="galaxies_subhalo_mass_centre_1", parameter_2="galaxies_subhalo_mass_centre_0"):

    list_of_contours = []
    for samples in list_of_samples:
        contours = get_contours_from_samples(
            samples=samples,
            parameter_1=parameter_1,
            parameter_2=parameter_2
        )

        list_of_contours.append(contours)

    return list_of_contours

# def get_contours_from_samples(samples, parameter_1="galaxies_subhalo_mass_centre_1", parameter_2="galaxies_subhalo_mass_centre_0"):
#
#     # NOTE: CHECK THE SHAPE OF SAMPLES. FLATTEN IT. THEN ITERATE.
#     contours = []
#     for i in range(np.shape(samples)[0]):
#         for j in range(np.shape(samples)[1]):
#             sample_temp = samples[i][j]
#             if sample_temp is not None:
#
#                 density2D = sample_temp.get2DDensity(
#                     parameter_1, parameter_2
#                 )
#
#                 if density2D is not None:
#                     contours.append([
#                         density2D.x, density2D.y, density2D.P
#                     ])
#
#     return contours


# def get_samples_from_subphase_directories(directories):
#
#     samples = []
#     for i in range(np.shape(directories)[0]):
#         samples_temp = []
#         for j in range(np.shape(directories)[1]):
#             if directories[i][j] is not None:
#                 directory = directories[i][j] + "/multinest"
#                 try:
#                     sample = getdist.mcsamples.loadMCSamples(directory)
#                     #print(sample.__dict__)
#                 except:
#                     sample = None
#             else:
#                 sample = None
#
#             samples_temp.append(sample)
#
#         samples.append(samples_temp)
#
#     return samples


def get_samples_from_multinest_outputs_in_directory(directory, suffix=""):

    return mcsamples.loadMCSamples(
        "{}/multinest{}".format(
            directory_utils.sanitize_directory(directory=directory),
            suffix
        )
    )


def get_list_of_samples_from_multinest_outputs_in_list_of_directories(list_of_directories):

    list_of_samples = []
    for directory in list_of_directories:
        samples = get_samples_from_multinest_outputs_in_directory(directory=directory)
        list_of_samples.append(samples)

    return list_of_samples


def sanitize_paramNames():
    pass


def triangle_plot(directory, suffix="", width_inch=16):

    samples = get_samples_from_multinest_outputs_in_directory(
        directory=directory,
        suffix=suffix
    )


    plots.get_single_plotter(width_inch=width_inch).triangle_plot(
        samples,
        params=[
            name for name in samples.paramNames.names
        ],
        filled=True
    )
    plt.show()


def map_paramnames_to_labels(paramnames):

    mappings = {
        "galaxies_lens_mass_slope":r"$\alpha$",
        "galaxies_lens_mass_axis_ratio":r"$q$",
        "galaxies_lens_mass_einstein_radius":r"$\theta_E$",
        "galaxies_lens_mass_phi":r"$\phi$",
        "galaxies_lens_mass_centre_0":r"$y_{cen}$",
        "galaxies_lens_mass_centre_1":r"$x_{cen}$",
        "galaxies_lens_shear_magnitude":r"$\gamma$",
        "galaxies_lens_shear_phi":r"$\theta_{\gamma}$",

    }

    labels = []

    for i in range(
        len(paramnames)
    ):
        labels.append(mappings[paramnames[i].name])

    return labels

def plot_chains_from_samples(list_of_samples, discard=0, parameter_indexes_arrays=None, parameter_labels=None, ncols=5, figsize=None):


    var = False
    if len(parameter_indexes_arrays.shape) == 1:
        number_of_parameters = len(parameter_indexes_arrays)
        var = False
    elif len(parameter_indexes_arrays.shape) == 2:
        number_of_parameters = parameter_indexes_arrays.shape[-1]
        var = True




    nrows = int(
        number_of_parameters / ncols
    )
    if not number_of_parameters % ncols == 0:
        nrows += 1

    figure, axes = plt.subplots(
        nrows=nrows, ncols=ncols, figsize=figsize
    )

    # if parameter_labels:
    #     if len(parameter_labels) != len(parameter_indexes):
    #         raise ValueError("...")

    colors = ["b", "r", "g", "y"]

    k = 0
    for i in range(nrows):
        for j in range(ncols):

            if k < number_of_parameters:

                for n, sample in enumerate(list_of_samples):
                    if var:
                        axes[i, j].plot(
                            list_of_samples[n].samples[
                                discard:,
                                parameter_indexes_arrays[n, k]
                            ],
                            color=colors[n],
                            alpha=0.75
                        )
                    else:
                        axes[i, j].plot(
                            list_of_samples[n].samples[
                                discard:,
                                parameter_indexes_arrays[k]
                            ],
                            color=colors[n],
                            alpha=0.75
                        )

                if parameter_labels:
                    axes[i, j].set_ylabel(parameter_labels[k], fontsize=15)

                k += 1

            else:

                axes[i, j].axis("off")

    plt.subplots_adjust(wspace=0.225, left=0.05, right=0.95)
    plt.show()



if __name__ == "__main__":


    # optimizer_directory = '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_8/contsub/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup'
    # optimizer_directory = '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup'

    optimizer_directories = [
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_8/contsub/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup',
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup'
    ]

    # optimizer_directories = [
    #     "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_8/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/",
    #     "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_8/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic__centre_with_GaussianPrior/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/"
    # ]

    optimizer_directories = [
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup',
        "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_8/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic__centre_with_GaussianPrior/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/"
    ]

    optimizer_directories = [
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/contsub/spws_0_1/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup',
        "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_8/contsub/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/"
    ]

    # SDP11 - ALMA
    optimizer_directories = [
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/contsub/spws_0_1/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup',
        "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_2_3/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/",
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/'
    ]

    # optimizer_directories = [
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/contsub/spws_0_1/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/pipeline__lens_powerlaw_and_shear__source/general/source__sersic__with_shear/mass__powerlaw__with_shear/phase_1__lens_powerlaw_and_shear__source/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup',
    #     "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_2_3/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/pipeline__lens_powerlaw_and_shear__source/general/source__sersic__with_shear/mass__powerlaw__with_shear/phase_1__lens_powerlaw_and_shear__source/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/",
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/'
    # ]
    legend_labels = [r'$C_{II}$; spw = 0, 1', 'Continuum; spw = 2, 3', r'$C_{II} +$ Continuum; spw = 0, 1']

    # # SDP11 - HST - multiple phases
    # optimizer_directories = [
    #     "/Users/ccbh87/Desktop/HATLAS_J091043-000322/output_0.45.0/HATLAS_J091043-000322/HST/WFC3/F160W/pipeline_source__parametric/general__hyper_galaxies_bg_noise/source__sersic__with_shear/phase_1__lens_sie__source_sersic/phase_tag__sub_2__pos_0.20/optimizer_backup/",
    #     "/Users/ccbh87/Desktop/HATLAS_J091043-000322/output_0.45.0/HATLAS_J091043-000322/HST/WFC3/F160W/pipeline_source__parametric/general__hyper_galaxies_bg_noise/source__sersic__with_shear/pipeline_source__inversion/general__hyper_galaxies_bg_noise/source__pix_voro_image__reg_adapt_bright__with_shear/phase_2__lens_sie__source_inversion_magnification/phase_tag__sub_2__pos_0.20/optimizer_backup/"
    # ]
    # legend_labels = None


    optimizer_directories = [
        "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_2_3/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/",
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/contsub/spws_0_1/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/'
    ]
    # optimizer_directories = [
    #     "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_2_3/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/pipeline__lens_powerlaw_and_shear__source/general/source__sersic__with_shear/mass__powerlaw__with_shear/phase_1__lens_powerlaw_and_shear__source/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/",
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/contsub/spws_0_1/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/pipeline__lens_powerlaw_and_shear__source/general/source__sersic__with_shear/mass__powerlaw__with_shear/phase_1__lens_powerlaw_and_shear__source/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/'
    # ]
    legend_labels = ['Continuum; spw = 2, 3', r'$C_{II}$; spw = 0, 1']

    optimizer_directories = [
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/contsub/spws_0_1/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/pipeline__lens_sie_and_shear__source_inversion/general/source__pix_voro_mag__reg_const__with_shear/phase_2__lens_sie_and_shear__source_inversion_magnification/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/',
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_2_3/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/pipeline__lens_sie_and_shear__source_inversion/general/source__pix_voro_mag__reg_const__with_shear/phase_2__lens_sie_and_shear__source_inversion_magnification/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/'
    ]
    legend_labels = [r'$C_{II}$; spw = 0, 1', 'Continuum; spw = 2, 3']

    optimizer_directories = [
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/',
        '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/'
    ]
    legend_labels = ['Continuum + $C_{II}$ + x1 sersic; spw = 0, 1', 'Continuum + $C_{II}$ + x2 sersic; spw = 0, 1']


    

    # optimizer_directories = [
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/',
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/',
    #     "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_2_3/pipeline__lens_sie_and_shear__source_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/",
    # ]
    # legend_labels = ['Continuum + $C_{II}$ + x1 sersic; spw = 0, 1', 'Continuum + $C_{II}$ + x2 sersic; spw = 0, 1', 'Continuum; spw = 2, 3']

    # optimizer_directories = [
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_1__lens_sie_and_shear__source_x2_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/',
    #     '/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/HATLAS_J091043-000322/2015.1.01362.S/width_128/spws_0_1/pipeline__lens_sie_and_shear__source_x2_sersic/general/source__sersic__with_shear/phase_2__lens_sie_and_shear__source_x2_sersic/phase_tag__rs_shape_200x200__rs_pix_0.05x0.05__sub_1/optimizer_backup/',
    # ]

    # params = [
    #     'galaxies_lens_mass_axis_ratio',
    #     'galaxies_lens_mass_phi',
    #     'galaxies_lens_shear_magnitude',
    #     'galaxies_lens_shear_phi',
    #     'galaxies_lens_mass_einstein_radius',
    #     'galaxies_lens_mass_centre_0',
    #     'galaxies_lens_mass_centre_1'
    # ]

    # optimizer_directory = '/Users/ccbh87/Desktop/HATLAS_J091043-000322/output_0.45.0/HATLAS_J091043-000322/HST/WFC3/F160W/pipeline_source__parametric/general__hyper_galaxies_bg_noise/source__sersic__with_shear/pipeline_source__inversion/general__hyper_galaxies_bg_noise/source__pix_voro_image__reg_adapt_bright__with_shear/phase_2__lens_sie__source_inversion_magnification/phase_tag__sub_2__pos_0.20/optimizer_backup'

    # params = [
    #     'galaxies_lens_mass_axis_ratio',
    #     'galaxies_lens_mass_phi',
    #     'galaxies_lens_shear_magnitude',
    #     'galaxies_lens_shear_phi',
    #     'galaxies_lens_mass_einstein_radius_value',
    #     'galaxies_lens_mass_centre_0',
    #     'galaxies_lens_mass_centre_1'
    # ]

    list_of_samples = []
    for optimizer_directory in optimizer_directories:
        samples = mcsamples.loadMCSamples(
            optimizer_directory + "/multinest"
        )

        list_of_samples.append(samples)

        #print(samples.getParamNames());exit()
        #print(samples.weights.shape, samples.samples.shape)


    galaxy = "lens"
    params = [
        name for name in samples.paramNames.names
        if str(name).startswith(
            "galaxies_{}".format(galaxy)
        )
    ]

    plots.get_single_plotter(width_inch=16).triangle_plot(
        list_of_samples,
        params=params,
        filled=True,
        legend_labels=legend_labels
    )
    plt.show()


    # for galaxy in ["source_0", "source_1"]:
    #     params = [
    #         name for name in samples.paramNames.names
    #         if str(name).startswith(
    #             "galaxies_{}".format(galaxy)
    #         )
    #     ]
    #
    #     plots.get_single_plotter(width_inch=16).triangle_plot(
    #         list_of_samples,
    #         params=params,
    #         filled=True,
    #     )
    # plt.show()








    # plt.figure()
    # plt.plot(list_of_samples[0].loglikes)
    # #plt.plot(list_of_samples[1].loglikes)
    # plt.yscale("log")
    # plt.show()
    # exit()





    # galaxy = "lens"
    #
    # parameter_info = [
    #     (name, i) for i, name in enumerate(list_of_samples[0].paramNames.names)
    #     if str(name).startswith(
    #         "galaxies_{}".format(galaxy)
    #     )
    # ]
    #
    # plot_chains_from_samples(
    #     list_of_samples=list_of_samples,
    #     discard=200,
    #     parameter_indexes=[i_tuple[1] for i_tuple in parameter_info],
    #     parameter_labels=map_paramnames_to_labels(
    #         paramnames=[i_tuple[0] for i_tuple in parameter_info]
    #     ),
    #     ncols=4,
    #     figsize=(20, 6)
    # )




    # NOTE: This is not working ...

    parameter_info_0 = [
        (name, i) for i, name in enumerate(list_of_samples[0].paramNames.names)
        if str(name).startswith(
            "galaxies_{}".format("source_0")
        )
    ]
    parameter_info_1 = [
        (name, i) for i, name in enumerate(list_of_samples[1].paramNames.names)
        if str(name).startswith(
            "galaxies_{}".format("source_1")
        )
    ]
    parameter_info = [
        (name, i) for i, name in enumerate(list_of_samples[2].paramNames.names)
        if str(name).startswith(
            "galaxies_{}".format("source")
        )
    ]

    plot_chains_from_samples(
        list_of_samples=list_of_samples,
        discard=200,
        parameter_indexes_arrays=np.array([
            [i_tuple[1] for i_tuple in parameter_info_0],
            [i_tuple[1] for i_tuple in parameter_info_1],
            [i_tuple[1] for i_tuple in parameter_info],
            [i_tuple[1] for i_tuple in parameter_info]
        ]),
        parameter_labels=None,
        ncols=4,
        figsize=(20, 6)
    )


    # NOTE: NOPE
    # parameter_info_0 = [
    #     (name, i) for i, name in enumerate(list_of_samples[0].paramNames.names)
    #     if str(name).startswith(
    #         "galaxies_{}".format("source_0")
    #     )
    # ]
    # parameter_info_1 = [
    #     (name, i) for i, name in enumerate(list_of_samples[0].paramNames.names)
    #     if str(name).startswith(
    #         "galaxies_{}".format("source_1")
    #     )
    # ]
    #
    #
    # asdas =list_of_samples[0].samples[:, [0, 1, 2]]
    #
    # fig = corner.corner(
    #     xs=list_of_samples[0].samples[:, [i_tuple[1] for i_tuple in parameter_info_0]],
    #     weights=list_of_samples[0].weights,
    #     bins=20,
    #     colors="b",
    #     quantiles=[0.16, 0.5, 0.84],
    #     plot_datapoints=False
    # )
    #
    # corner.corner(
    #     xs=list_of_samples[1].samples[:, [i_tuple[1] for i_tuple in parameter_info_1]],
    #     weights=list_of_samples[1].weights,
    #     bins=20,
    #     quantiles=[0.16, 0.5, 0.84],
    #     plot_datapoints=False,
    #     fig=fig
    # )

    plt.show()
