# NOTE: A LOT NEED TO CHANGE HERE ...

# TODO: The samples in the 2dmarginal plot need not be in a grid.

import os
import numpy as np
import matplotlib.pyplot as plt
import getdist
#from getdist import plots, MCSamples

from list_utils import *
from directory_utils import *


def get_list_of_directory_trees_in_directory(directory):
    return [
        x[0]
        for x in os.walk(directory)
    ]

def get_subphase_directory(x_i, x_j, y_i, y_j):

    str_0 = "galaxies_subhalo_mass_centre_0_" + "{0:.2f}".format(x_i) + "_" + "{0:.2f}".format(x_j)
    str_1 = "galaxies_subhalo_mass_centre_1_" + "{0:.2f}".format(y_i) + "_" + "{0:.2f}".format(y_j)

    return str_0 + "_" + str_1


def get_subphase_directories_for_gridsearch(phase_directory, xmin, xmax, ymin, ymax, number_of_steps):

    x = np.linspace(xmin, xmax, number_of_steps + 1)
    y = np.linspace(ymin, ymax, number_of_steps + 1)

    directories = []
    for i in range(number_of_steps):
        directories_temp = []
        for j in range(number_of_steps):
            subphase_directory = get_subphase_directory(
                x_i=x[i], x_j=x[i+1], y_i=y[j], y_j=y[j+1]
            )

            # TODO: sanitize the phase directory
            phase_directory = sanitize_directory(
                directory=phase_directory
            )
            subphase_directory = phase_directory + "/" + subphase_directory
            if not os.path.isdir(subphase_directory):
                raise IOError(subphase_directory + " does not exist")

            list_of_directory_trees_filtered = filter_input_list_of_strings_after_split_with_ending_string(
                input_list_of_strings=get_list_of_directory_trees_in_directory(
                    directory=subphase_directory
                ),
                split_character="/",
                ending_string="optimizer_backup"
            )

            if len(list_of_directory_trees_filtered) == 1:
                if not os.listdir(list_of_directory_trees_filtered[0]):
                    directories_temp.append(None)
                else:
                    directories_temp.append(list_of_directory_trees_filtered[0])
            if len(list_of_directory_trees_filtered) < 1:
                directories_temp.append(None)
                #raise ValueError("optimizer_backup does not exist")
            if len(list_of_directory_trees_filtered) > 1:
                raise ValueError("THIS IS WEIRD...")

        directories.append(directories_temp)

    return directories



def get_samples_from_subphase_directories(directories):

    samples = []
    for i in range(np.shape(directories)[0]):
        samples_temp = []
        for j in range(np.shape(directories)[1]):
            if directories[i][j] is not None:
                directory = directories[i][j] + "/multinest"
                try:
                    sample = getdist.mcsamples.loadMCSamples(directory)
                    #print(sample.__dict__)
                except:
                    sample = None
            else:
                sample = None

            samples_temp.append(sample)

        samples.append(samples_temp)

    return samples




def subhalo_grid_plot_from_samples(samples, levels=None):

    plt.figure(
        figsize=(15, 15)
    )

    # ...
    if levels is None:
        levels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    # ...
    for i in range(np.shape(samples)[0]):
        for j in range(np.shape(samples)[0]):
            sample_temp = samples[i][j]
            if sample_temp is not None:

                density2D = sample_temp.get2DDensity(
                    'galaxies_subhalo_mass_centre_1',
                    'galaxies_subhalo_mass_centre_0'
                )

                if density2D is not None:
                    plt.contour(
                        density2D.x,
                        density2D.y,
                        density2D.P,
                        levels=levels,
                        colors="black"
                    )
                    #print("OK")



    for i in np.linspace(-2.0, 2.0, 5):
        plt.axvline(i, linestyle="--", linewidth=2, color="r")
        plt.axhline(i, linestyle="--", linewidth=2, color="r")

    plt.plot([-1.0], [0.0], marker="*", markersize=20, color="b")

    plt.xlabel("x (arcsec)", fontsize=20)
    plt.ylabel("y (arcsec)", fontsize=20)
    plt.xlim((-2.1, 2.1))
    plt.ylim((-2.1, 2.1))
    plt.show()

if __name__ == "__main__":

    phase_directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer/lens_powerlaw_and_shear_and_subhalo__source_ellipticalcoresersic/model_1/total_flux_1.0_Jy/5.6/230GHz/t_tot__60s/t_int__10s/n_channels_128/0.5mm/width_128/pipeline__lens_fixed_with_subhalo__source_inversion/general/source__pix_voro_mag__reg_const__with_shear/phase_2__subhalo_search__source/phase_tag__rs_shape_125x125__rs_pix_0.04x0.04__sub_2__pos_0.20/"
    xmin = -2.0
    xmax = 2.0
    ymin = -2.0
    ymax = 2.0
    number_of_steps = 4

    subphase_directories = get_subphase_directories_for_gridsearch(
        phase_directory=phase_directory,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        number_of_steps=number_of_steps
    )

    samples = get_samples_from_subphase_directories(directories=subphase_directories)

    subhalo_grid_plot_from_samples(samples=samples)
