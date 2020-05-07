import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# NOTE: ...
sys.path.append(
    os.environ["GitHub"] + "/utils"
)
import list_utils as list_utils
import getdist_utils as getdist_utils
import directory_utils as directory_utils

import autofit as af
import autolens as al

def adada():
    print("ASDSADAS")


# figure = plt.figure()
# figure.axes
# plt.show()
# exit()


def plot_visibilities(visibilities, spectral_mask=None):

    #total_number_of_channels = visibilities.shape[0]
    if len(visibilities.shape) == 1:
        raise ValueError
    elif len(visibilities.shape) == 2:

        # WARNING: The spectral_mask is not being used in this case.

        real_visibilities = visibilities[:, 0]
        imag_visibilities = visibilities[:, 1]

        plt.figure()
        plt.plot(
            real_visibilities,
            imag_visibilities,
            linestyle="None",
            marker="."
        )

        plt.show()

    elif len(visibilities.shape) == 3:
        real_visibilities = visibilities[:, :, 0]
        imag_visibilities = visibilities[:, :, 1]

        plt.figure()
        colors = pl.cm.jet(
            np.linspace(0, 1, visibilities.shape[0])
        )
        for i in range(visibilities.shape[0]):
            plt.plot(
                real_visibilities[i, :],
                imag_visibilities[i, :],
                linestyle="None",
                marker=".",
                color=colors[i]
            )

        plt.show()


def interpolated_reconstruction(voronoi, values, grid):

    return interpolate.griddata(
        voronoi._points,
        values,
        grid.in_2d,
        method="cubic",
        fill_value=0.0
    )

# interpolated_reconstruction = interpolate.griddata(
#     fit.inversion.mapper.voronoi._points,
#     source_pixel_values,
#     grid.in_2d,
#     method="cubic",
#     fill_value=0.0
# )

def plot(inversion):

    regions, vertices = voronoi_polygons(
        voronoi=inversion.mapper.voronoi
    )

    values = inversion.mapper.reconstructed_pixelization_from_solution_vector(
        solution_vector=inversion.reconstruction
    )

    facecolor_array = np.divide(
        values[:], np.max(values)
    )

    plt.figure()

    for i, (region, index) in enumerate(
        zip(regions, range(inversion.mapper.pixels))
    ):
        polygon = vertices[region]

        plt.fill(
            *zip(*polygon),
            edgecolor="black",
            alpha=0.75,
            facecolor=cmap(
                facecolor_array[index]
            ),
            lw=1
        )

    plt.show()


def draw_voronoi_pixels(mapper, values, cmap, axes, alpha=1.0, fill_polygons=True, cb=None, min_value=None):

    regions, vertices = voronoi_polygons(voronoi=mapper.voronoi)

    if values is not None:
        color_array = values[:] / np.max(values)
        cmap = plt.get_cmap(cmap)
        #cb.set_with_values(cmap=cmap, color_values=values)
    else:
        cmap = plt.get_cmap("Greys")
        color_array = np.zeros(shape=mapper.pixels)

    for i, (region, index) in enumerate(zip(regions, range(mapper.pixels))):
        polygon = vertices[region]
        col = cmap(color_array[index])
        if min_value is not None:
            if values[i] > min_value:
                if fill_polygons:
                    axes.fill(
                        *zip(*polygon),
                        edgecolor="black",
                        alpha=alpha,
                        facecolor=col,
                        lw=1
                    )
                else:
                    axes.fill(
                        *zip(*polygon),
                        edgecolor="black",
                        alpha=alpha,
                        facecolor="None",
                        lw=1
                    )
        else:
            if fill_polygons:
                axes.fill(
                    *zip(*polygon),
                    edgecolor="black",
                    alpha=alpha,
                    facecolor=col,
                    lw=1
                )
            else:
                axes.fill(
                    *zip(*polygon),
                    edgecolor="black",
                    alpha=alpha,
                    facecolor="None",
                    lw=1
                )


    # plt.plot(
    #     mapper.voronoi._points[:, 0],
    #     mapper.voronoi._points[:, 1],
    #     linestyle="None",
    #     marker="o",color="black"
    # )
    #
    # plt.show()


def voronoi_polygons(voronoi, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    voronoi : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if voronoi.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = voronoi.vertices.tolist()

    center = voronoi.points.mean(axis=0)
    if radius is None:
        radius = voronoi.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(voronoi.ridge_points, voronoi.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(voronoi.point_region):
        vertices = voronoi.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = voronoi.points[p2] - voronoi.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # hyper

            midpoint = voronoi.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = voronoi.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


def get_list_of_directories_from_GridPhase_directory(directory):

    list_of_directories = list_utils.filter_input_list_of_strings_after_split_with_ending_string(
        input_list_of_strings=[x[0]
            for x in os.walk(directory)
        ],
        split_character="/",
        ending_string="optimizer_backup"
    )

    return list_of_directories


def plot_contours_from_GridPhase(directory):

    list_of_directories = get_list_of_directories_from_GridPhase_directory(directory=directory)

    list_of_samples = getdist_utils.get_list_of_samples_from_multinest_outputs_in_list_of_directories(
        list_of_directories=list_of_directories
    )

    list_of_contours = getdist_utils.get_list_of_contours_from_list_of_samples(
        list_of_samples=list_of_samples,
        parameter_1="galaxies_subhalo_mass_centre_1",
        parameter_2="galaxies_subhalo_mass_centre_0"
    )

    plt.figure()
    for contours in list_of_contours:
        x, y, P = contours
        plt.contour(
            x, y, P, colors="black"
        )
    plt.show()




def load_results_from_GridPhase(filename):

    if os.path.isfile(filename):
        y, x, evidence_matrix_flattened = np.loadtxt(
            filename, delimiter=",", skiprows=1, unpack=True
        )

    return y, x, evidence_matrix_flattened


def plot_evidence_diff_matrix_from_GridPhase(directory, evidence_from_previous_phase):

    directory = directory_utils.sanitize_directory(
        directory=directory
    )

    y_grid_flattened, x_grid_flattened, evidence_matrix_flattened = load_results_from_GridPhase(
        filename=directory + "/results"
    )

    nsteps = int(
        np.sqrt(evidence_matrix_flattened.shape[0])
    )

    evidence_matrix = evidence_matrix_flattened.reshape(
        nsteps,
        nsteps
    )
    evidence_diff_matrix = evidence_matrix - evidence_from_previous_phase

    xmin = np.min(x_grid_flattened)
    xmax = np.max(x_grid_flattened)
    ymin = np.min(y_grid_flattened)
    ymax = np.max(y_grid_flattened)
    dx = (xmax - xmin) / (nsteps - 1)
    dy = (ymax - ymin) / (nsteps - 1)

    extent = [
        xmin,
        xmax + dx,
        ymin,
        ymax + dy,
    ]

    xticks = np.linspace(xmin, xmax + dx, nsteps)
    yticks = np.linspace(ymin, ymax + dy, nsteps)


    plt.figure(figsize=(8, 8))
    plt.imshow(evidence_diff_matrix, cmap="jet", extent=extent)
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.xlabel("x (arcsec)", fontsize=15)
    plt.ylabel("y (arcsec)", fontsize=15)
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    pass

    # directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer/lens_powerlaw__source_ellipticalcoresersic/model_1/total_flux_1.0_Jy/5.6/230GHz/t_tot__60s/t_int__10s/n_channels_128/0.5mm/width_128/pipeline__lens_sie__source_ellipticalcoresersic__local/general/source__ellipticalcoresersic__with_shear/pipeline__lens_powerlaw__source__from__parametric/general/source__ellipticalcoresersic__with_shear/mass__powerlaw__no_shear/pipeline_subhalo__nfw/general/source__ellipticalcoresersic__with_shear/mass__powerlaw__no_shear/phase_1__subhalo_search__source/phase_tag__rs_shape_125x125__rs_pix_0.04x0.04__sub_1__pos_0.20/"

    directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer/lens_powerlaw__source_ellipticalcoresersic/model_1/total_flux_1.0_Jy/5.6/230GHz/t_tot__60s/t_int__10s/n_channels_128/0.5mm/width_128/pipeline_subhalo__nfw__with_lens_fixed_and_source_fixed/general/phase_1__subhalo_search__source/phase_tag__rs_shape_125x125__rs_pix_0.04x0.04__sub_1__pos_0.20"

    filename = directory + "results"

    #plot_contours_from_GridPhase(directory=directory)


    # list_of_directories = list_utils.filter_input_list_of_strings_after_split_with_ending_string(
    #     input_list_of_strings=[x[0]
    #         for x in os.walk(directory)
    #     ],
    #     split_character="/",
    #     ending_string="optimizer_backup"
    # )

    """
    # samples = getdist_utils.get_samples_from_multinest_outputs_in_directory(directory=list_of_directories[0])
    #
    # x, y, P = getdist_utils.get_contours_from_samples(
    #     samples=samples, parameter_1="galaxies_subhalo_mass_centre_1", parameter_2="galaxies_subhalo_mass_centre_0"
    # )
    #
    # plt.contour(
    #     x, y, P, colors="black"
    # )
    # plt.show()
    """







    # evidence_from_previous_phase = 57402.27681519
    #
    # def load_results_from_GridPhase(filename):
    #     if os.path.isfile(filename):
    #         y, x, evidences = np.loadtxt(
    #             filename, delimiter=",", skiprows=1, unpack=True
    #         )
    #         return y, x, evidences
    #
    # y, x, evidences = load_results_from_GridPhase(filename=filename)
    #
    # nsteps = int(np.sqrt(evidences.shape[0]))
    #
    # y_reshaped = y.reshape(nsteps, nsteps)
    # x_reshaped = x.reshape(nsteps, nsteps)
    #
    # evidences_reshaped = evidences.reshape(nsteps, nsteps)
    # evidences_reshaped -= evidence_from_previous_phase
    # plt.imshow(evidences_reshaped)
    # plt.colorbar()
    # plt.show()



    plot_evidence_diff_matrix_from_GridPhase(directory=directory, evidence_from_previous_phase=58017.81689441838)
