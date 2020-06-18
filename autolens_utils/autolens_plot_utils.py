import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import autolens as al

# NOTE: ...
sys.path.append(
    "{}/utils".format(
        os.environ["GitHub"]
    )
)
import list_utils as list_utils
#import getdist_utils as getdist_utils
import directory_utils as directory_utils
import voronoi_utils as voronoi_utils



def dirty_image_from_visibilities_and_transformer(visibilities, transformer):

    # NOTE: Depending the transformer invert the image.

    dirty_image = transformer.image_from_visibilities(
        visibilities=visibilities
    )

    if isinstance(transformer, al.TransformerFINUFFT):
        dirty_image = dirty_image[::-1, :]
    if isinstance(transformer, al.TransformerNUFFT):
        pass

    return dirty_image


def plot_dirty_image_from_visibilities_and_transformer(visibilities, transformer):

    dirty_image = dirty_image_from_visibilities_and_transformer(
        visibilities=visibilities,
        transformer=transformer
    )

    plt.figure()
    plt.imshow(dirty_image)
    plt.show()



def dirty_cube_from_visibilities(visibilities, transformers, shape):
    # NOTE: shape is 3d

    if len(transformers) != visibilities.shape[0]:
        raise ValueError("...")

    dirty_cube = np.zeros(
        shape=shape
    )
    for i in range(visibilities.shape[0]):
        dirty_image = transformers[i].image_from_visibilities(
            visibilities=visibilities[i]
        )

        if isinstance(transformers[i], al.TransformerFINUFFT):
            dirty_image = dirty_image[::-1, :]
        dirty_cube[i] = dirty_image

    return dirty_cube


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


# NOTE: WHAT AM I DOING HERE?
def plot(inversion, tracer, grid, indexes):

    regions, vertices = voronoi_polygons(
        voronoi=inversion.mapper.voronoi
    )

    values = inversion.mapper.reconstructed_pixelization_from_solution_vector(
        solution_vector=inversion.reconstruction
    )

    cmap = plt.get_cmap("jet")

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
            alpha=1.0,
            facecolor=cmap(
                facecolor_array[index]
            ),
            lw=1
        )

    image = np.zeros(shape=grid.total_pixels)
    for idx in indexes:
        source_i_image = tracer.galaxies[
            idx
        ].profile_image_from_grid(grid=grid)
        image += source_i_image
    image = image.reshape(grid.shape_2d)

    plt.contour(
        image[::-1, :],
        colors="w",
        extent=[
            np.min(grid) - grid.pixel_scale,
            np.max(grid) + grid.pixel_scale,
            np.min(grid) - grid.pixel_scale,
            np.max(grid) + grid.pixel_scale
        ],
        alpha=0.75
    )

    plt.xlim(((np.min(grid) - grid.pixel_scale) / 3.0, (np.max(grid) + grid.pixel_scale) / 3.0))
    plt.ylim(((np.min(grid) - grid.pixel_scale) / 3.0, (np.max(grid) + grid.pixel_scale) / 3.0))

    plt.xlabel("x (arcsec)", fontsize=15)
    plt.ylabel("y (arcsec)", fontsize=15)

    plt.show()


# def draw_voronoi_pixels(mapper, values, cmap, axes=None, alpha=1.0, fill_polygons=True, cb=None, min_value=None):
#
#     regions, vertices = voronoi_utils.voronoi_polygons(
#         voronoi=mapper.voronoi
#     )
#
#     if axes is None:
#         figure = plt.figure()
#         axes = figure.axes
#
#     if values is not None:
#         color_array = values[:] / np.max(values)
#         cmap = plt.get_cmap(cmap)
#         #cb.set_with_values(cmap=cmap, color_values=values)
#     else:
#         cmap = plt.get_cmap("Greys")
#         color_array = np.zeros(shape=mapper.pixels)
#
#     for i, (region, index) in enumerate(zip(regions, range(mapper.pixels))):
#         polygon = vertices[region]
#         col = cmap(color_array[index])
#         if min_value is not None:
#             if values[i] > min_value:
#                 if fill_polygons:
#                     axes.fill(
#                         *zip(*polygon),
#                         edgecolor="black",
#                         alpha=alpha,
#                         facecolor=col,
#                         lw=1
#                     )
#                 else:
#                     axes.fill(
#                         *zip(*polygon),
#                         edgecolor="black",
#                         alpha=alpha,
#                         facecolor="None",
#                         lw=1
#                     )
#         else:
#             if fill_polygons:
#                 axes.fill(
#                     *zip(*polygon),
#                     edgecolor="black",
#                     alpha=alpha,
#                     facecolor=col,
#                     lw=1
#                 )
#             else:
#                 axes.fill(
#                     *zip(*polygon),
#                     edgecolor="black",
#                     alpha=alpha,
#                     facecolor="None",
#                     lw=1
#                 )
#
#
#     # plt.plot(
#     #     mapper.voronoi._points[:, 0],
#     #     mapper.voronoi._points[:, 1],
#     #     linestyle="None",
#     #     marker="o",color="black"
#     # )
#     #
#     plt.show()

def draw_voronoi_polygons(mapper):

    regions, vertices = voronoi_utils.voronoi_polygons(
        voronoi=mapper.voronoi
    )

    for i, (region, index) in enumerate(
        zip(regions, range(mapper.pixels))
    ):
        polygon = vertices[region]

        plt.fill(
            *zip(*polygon),
            edgecolor="black",
            facecolor="None",
            lw=1
        )

def draw_voronoi_pixels(mapper, values, cmap="jet", alpha=1.0, fill_polygons=True, cb=None, min_value=None, value_max=None):

    regions, vertices = voronoi_utils.voronoi_polygons(
        voronoi=mapper.voronoi
    )

    if value_max is None:
        colors = values[:] / np.max(values)
    else:
        colors = values[:] / value_max


    cmap = plt.get_cmap(cmap)
        #cb.set_with_values(cmap=cmap, color_values=values)
    # else:
    #     cmap = plt.get_cmap("Greys")
    #     color_array = np.zeros(shape=mapper.pixels)

    for i, (region, index) in enumerate(zip(regions, range(mapper.pixels))):
        polygon = vertices[region]

        col = cmap(colors[index])

        if min_value is not None:
            if values[i] > min_value:
                if fill_polygons:
                    plt.fill(
                        *zip(*polygon),
                        edgecolor="black",
                        alpha=alpha,
                        facecolor=col,
                        lw=1
                    )
                else:
                    plt.fill(
                        *zip(*polygon),
                        edgecolor="black",
                        alpha=alpha,
                        facecolor="None",
                        lw=1
                    )
        else:
            if fill_polygons:
                plt.fill(
                    *zip(*polygon),
                    edgecolor="black",
                    alpha=alpha,
                    facecolor=col,
                    lw=1
                )
            else:
                plt.fill(
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
    #plt.show()


def plot_reconstructions_from_inversions(
    inversions,
    nrows,
    ncols,
    figsize=(20, 10),
    cmap="jet",
    xlim=None,
    ylim=None,
    n_xticks=5,
    n_yticks=5,
    subplots_kwargs={
        "wspace":0.0,
        "hspace":0.0,
        "left":0.05,
        "right":0.95,
        "bottom":0.05,
        "top":0.95
    },
    cmap_type="same"
):

    figure = plt.figure(figsize=figsize)

    print("n = ", len(inversions))
    if nrows * ncols < len(inversions):
        raise ValueError("...")

    if xlim is not None:
        xticks = np.linspace(xlim[0], xlim[1], n_xticks)
    if ylim is not None:
        yticks = np.linspace(ylim[0], ylim[1], n_yticks)

    if cmap_type == "same":
        value_max = np.max(
            [inversion.reconstruction
                for inversion in inversions
            ]
        )
    elif cmap_type == "individual":
        value_max = [np.max(inversion.reconstruction)
            for inversion in inversions
        ]
    else:
        raise ValueError("...")

    i = 0
    j = 0
    for n, inversion in enumerate(inversions):
        print("n = ", n)

        plt.subplot(
            nrows,
            ncols,
            n+1
        )

        if cmap_type == "same":
            draw_voronoi_pixels(
                mapper=inversion.mapper,
                values=inversion.reconstruction,
                value_max=value_max
            )
        if cmap_type == "individual":
            draw_voronoi_pixels(
                mapper=inversion.mapper,
                values=inversion.reconstruction,
                value_max=value_max[n]
            )

        if xlim is not None:
            plt.xlim(xlim)
        if ylim is not None:
            plt.ylim(ylim)

        if i == nrows - 1:
            if xlim is not None:
                plt.xticks(xticks[1:-1])
            else:
                plt.xticks([])
        else:
            plt.xticks([])

        if j == 0:
            if ylim is not None:
                plt.yticks(yticks[1:-1])
            else:
                plt.yticks([])
        else:
            plt.yticks([])

        j += 1
        if j == ncols:
            j = 0
            i += 1

    plt.subplots_adjust(
        **subplots_kwargs
    )

    plt.show()


def plot_fit_imaging(
    fit,

):
    pass

def plot_fit(
    fit,
    centre,
    radius,
    normalize_residuals=True,
    show_contours=True,
    xlim_image_plane=None,
    ylim_image_plane=None,
    xlim_source_plane=None,
    ylim_source_plane=None
):

    def normalize(array, min_value=-1.0, max_value=1.0):
        return min_value + (max_value - min_value) * (
            (array - np.min(array)) / (np.max(array) - np.min(array))
        )

    extent = [
        np.min(fit.grid[:, 1]),
        np.max(fit.grid[:, 1]),
        np.max(fit.grid[:, 0]),
        np.min(fit.grid[:, 0])
    ]

    dirty_image = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.visibilities
    )
    dirty_model_image = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.model_visibilities
    )

    vmin = np.min(dirty_image)
    vmax = np.max(dirty_image)

    figure, axes = plt.subplots(
        nrows=1,
        ncols=4,
        figsize=(20, 4)
    )

    axes[0].imshow(
        dirty_image,
        cmap="jet",
        extent=extent,
        vmin=vmin,
        vmax=vmax,
        aspect="auto"
    )


    # for mass_profile_centre in fit.tracer.mass_profile_centres:
    #     if mass_profile_centre != (0.0, 0.0):
    #
    #         axes[0].plot([mass_profile_centre[1]], [mass_profile_centre[0]], linestyle="None", marker="o", markersize=10, color="w")

    axes[1].imshow(
        dirty_model_image,
        cmap="jet",
        extent=extent,
        vmin=vmin,
        vmax=vmax,
        aspect="auto"
    )

    residuals = np.subtract(
        dirty_image, dirty_model_image
    )
    if normalize_residuals:
        axes[2].imshow(
            normalize(residuals),
            cmap="jet",
            extent=extent,
            vmin=-1.0,
            vmax=1.0,
            aspect="auto"
        )
    else:
        axes[2].imshow(
            residuals,
            cmap="jet",
            extent=extent,
            vmin=vmin,
            vmax=vmax,
            aspect="auto"
        )

    if show_contours:
        levels = [
            vmax * percent / 100.0 for percent in np.arange(20, 100, 10)
        ]

        # axes[0].contour(
        #     dirty_model_image[::-1, :],
        #     levels=levels,
        #     colors="black",
        #     extent=extent,
        #     alpha=0.5
        # )
        axes[2].contour(
            dirty_model_image[::-1, :],
            levels=levels,
            colors="black",
            extent=extent,
            alpha=0.5
        )


    # for i in range(len(axes)):
    #     axes[i].set_xticks([])
    #     axes[i].set_yticks([])
    #     if i in [0, 1, 2]:
    #         axes[i].set_xlim(
    #             np.add(centre[1], -radius),
    #             np.add(centre[1], radius)
    #         )
    #         axes[i].set_ylim(
    #             np.add(centre[0], radius),
    #             np.add(centre[0], -radius)
    #         )



    if fit.inversion is None:

        source_plane_image = fit.tracer.source_plane.profile_image_from_grid(
            grid=fit.grid
        )

        axes[3].imshow(
            source_plane_image.in_2d,
            cmap="jet",
            extent=extent,
            aspect="auto"
        )
        #axes[3].set_xticks([])
        #axes[3].set_yticks([])
        #axes[3].set_xlim(xlim_image_plane)
        #axes[3].set_ylim(ylim_image_plane)

    else:
        draw_voronoi_pixels(
            mapper=fit.inversion.mapper,
            values=fit.inversion.reconstruction
        )

    axes[3].plot(
        fit.tracer.tangential_caustic[:, 1],
        fit.tracer.tangential_caustic[:, 0],
        linewidth=2,
        color="w"
    )

    if xlim_image_plane is not None and ylim_image_plane is not None:
        for i in [0, 1, 2]:
            axes[i].set_xticks([])
            axes[i].set_yticks([])
            axes[i].set_xlim(xlim_image_plane)
            axes[i].set_ylim(ylim_image_plane)

    if xlim_source_plane is not None and ylim_source_plane is not None:
        axes[3].set_xticks([])
        axes[3].set_yticks([])
        axes[3].set_xlim(xlim_source_plane)
        axes[3].set_ylim(ylim_source_plane)

    plt.subplots_adjust(wspace=0.0, hspace=0.0)

    plt.show()










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

    def sanitize_filename():
        pass

    if os.path.isfile(filename):
        y, x, evidence_matrix_flattened = np.loadtxt(
            filename, delimiter=",", skiprows=1, unpack=True
        )
    else:
        raise ValueError(
            "{} does not exist".format(filename)
        )

    return y, x, evidence_matrix_flattened


def plot_evidence_diff_matrix_from_GridPhase(directory, evidence_from_previous_phase=0.0):

    directory = directory_utils.sanitize_directory(
        directory=directory
    )

    results_filename = directory + "/results"
    y_grid_flattened, x_grid_flattened, evidence_matrix_flattened = load_results_from_GridPhase(
        filename=results_filename
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
    #plt.show()



def paramNamesMapping():
    pass

    # TODO: Map the names of parameters that are saved by multinest to something prettier.


if __name__ == "__main__":
    pass

    # directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer/lens_powerlaw__source_ellipticalcoresersic/model_1/total_flux_1.0_Jy/5.6/230GHz/t_tot__60s/t_int__10s/n_channels_128/0.5mm/width_128/pipeline__lens_sie__source_ellipticalcoresersic__local/general/source__ellipticalcoresersic__with_shear/pipeline__lens_powerlaw__source__from__parametric/general/source__ellipticalcoresersic__with_shear/mass__powerlaw__no_shear/pipeline_subhalo__nfw/general/source__ellipticalcoresersic__with_shear/mass__powerlaw__no_shear/phase_1__subhalo_search__source/phase_tag__rs_shape_125x125__rs_pix_0.04x0.04__sub_1__pos_0.20/"

    directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer/lens_powerlaw__source_ellipticalcoresersic/model_1/total_flux_1.0_Jy/5.6/230GHz/t_tot__60s/t_int__10s/n_channels_128/0.5mm/width_128/pipeline_subhalo__nfw__with_lens_fixed_and_source_fixed/general/phase_1__subhalo_search__source/phase_tag__rs_shape_125x125__rs_pix_0.04x0.04__sub_1__pos_0.20"

    filename = directory + "results"

    plot_contours_from_GridPhase(directory=directory)

    plot_evidence_diff_matrix_from_GridPhase(directory=directory, evidence_from_previous_phase=58017.81689441838)
