import os
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)
import voronoi_utils as voronoi_utils

import autoarray as aa
import autolens as al


def mapped_reconstructed_visibilities(transformed_mapping_matrices, reconstruction, indexes):

    real_transformed_mapping_matrix = transformed_mapping_matrices[0]
    imag_transformed_mapping_matrix = transformed_mapping_matrices[1]

    real_visibilities = aa.util.inversion_util.mapped_reconstructed_data_from_mapping_matrix_and_reconstruction(
        mapping_matrix=real_transformed_mapping_matrix[:, indexes],
        reconstruction=reconstruction[indexes],
    )
    imag_visibilities = aa.util.inversion_util.mapped_reconstructed_data_from_mapping_matrix_and_reconstruction(
        mapping_matrix=imag_transformed_mapping_matrix[:, indexes],
        reconstruction=reconstruction[indexes],
    )

    return aa.structures.visibilities.Visibilities(
        visibilities_1d=np.stack(
            arrays=(real_visibilities, imag_visibilities),
            axis=-1
        )
    )

def func_1(fit, indexes, xlim_image_plane, ylim_image_plane, xlim_source_plane, ylim_source_plane, directory):

    dirty_model_image = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.model_visibilities
    )

    dirty_model_image_region = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=mapped_reconstructed_visibilities(
            transformed_mapping_matrices=fit.inversion.transformed_mapping_matrices,
            reconstruction=fit.inversion.reconstruction,
            indexes=indexes
        )
    )

    extent = [
        np.min(fit.grid[:, 1]),
        np.max(fit.grid[:, 1]),
        np.max(fit.grid[:, 0]),
        np.min(fit.grid[:, 0])
    ]

    regions, vertices = voronoi_utils.voronoi_polygons(
        voronoi=fit.inversion.mapper.voronoi
    )

    reconstruction = fit.inversion.reconstruction

    colors = np.divide(
        reconstruction,
        np.max(reconstruction)
    )

    cmap = plt.get_cmap("jet")

    figure, axes = plt.subplots(
        nrows=1,
        ncols=3,
        figsize=(15, 4)
    )

    vmin = np.min(dirty_model_image)
    vmax = np.max(dirty_model_image)

    axes[0].imshow(
        dirty_model_image,
        cmap="jet",
        extent=extent,
        aspect="auto",
        vmin=vmin,
        vmax=vmax
    )

    axes[1].imshow(
        dirty_model_image_region,
        cmap="jet",
        extent=extent,
        aspect="auto",
        vmin=vmin,
        vmax=vmax
    )

    for i in [0, 1]:
        axes[i].contour(
            dirty_model_image[::-1, :],
            levels=[vmax * percentage
                for percentage in np.linspace(0.25, 1.0, 10)
            ],
            colors="black",
            extent=extent,
            alpha=0.5
        )

    for i, (region, index) in enumerate(
        zip(regions, range(fit.inversion.mapper.pixels))
    ):

        polygon = vertices[region]

        if i in indexes:
            axes[2].fill(
                *zip(*polygon),
                edgecolor="black",
                alpha=1.0,
                facecolor=cmap(colors[index]),
                lw=1
            )
        else:
            axes[2].fill(
                *zip(*polygon),
                edgecolor="black",
                alpha=1.0,
                facecolor="w",
                lw=1
            )


    axes[0].set_xticks([])
    axes[0].set_yticks([])
    axes[0].set_xlim(xlim_image_plane)
    axes[0].set_ylim(ylim_image_plane)
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    axes[1].set_xlim(xlim_image_plane)
    axes[1].set_ylim(ylim_image_plane)
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    axes[2].set_xlim(xlim_source_plane)
    axes[2].set_ylim(ylim_source_plane)
    plt.subplots_adjust(
        wspace=0.0
    )
    plt.show()





def func(fit, xlim_image_plane, ylim_image_plane, xlim_source_plane, ylim_source_plane, directory):

    extent = [
        np.min(fit.grid[:, 1]),
        np.max(fit.grid[:, 1]),
        np.max(fit.grid[:, 0]),
        np.min(fit.grid[:, 0])
    ]

    dirty_model_image = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.model_visibilities
    )

    vmin = np.min(dirty_model_image)
    vmax = np.max(dirty_model_image)

    regions, vertices = voronoi_utils.voronoi_polygons(
        voronoi=fit.inversion.mapper.voronoi
    )

    reconstruction = fit.inversion.reconstruction

    colors = np.divide(
        reconstruction,
        np.max(reconstruction)
    )

    real_transformed_mapping_matrices = fit.inversion.transformed_mapping_matrices[0]
    imag_transformed_mapping_matrices = fit.inversion.transformed_mapping_matrices[1]


    cmap = plt.get_cmap("jet")


    for i, value in enumerate(reconstruction):

        real_visibilities = real_transformed_mapping_matrices[:, i] * value
        imag_visibilities = imag_transformed_mapping_matrices[:, i] * value

        visibilities = np.stack(
            arrays=(real_visibilities, imag_visibilities),
            axis=-1
        )

        dirty_model_image_temp = fit.masked_interferometer.transformer.image_from_visibilities(
            visibilities=visibilities
        )

        figure, axes = plt.subplots(
            nrows=1,
            ncols=4,
            figsize=(20, 4)
        )

        for j, (region, index) in enumerate(
            zip(regions, range(fit.inversion.mapper.pixels))
        ):
            polygon = vertices[region]

            axes[0].imshow(
                dirty_model_image,
                cmap="jet",
                extent=extent,
                aspect="auto"
            )
            # vmin=np.min(dirty_model_image),
            # vmax=np.max(dirty_model_image),



            axes[1].imshow(
                dirty_model_image_temp,
                cmap="Greys",
                extent=extent,
                aspect="auto"
            )
            # vmin=vmin_temp,
            # vmax=vmax_temp,

            axes[2].fill(
                *zip(*polygon),
                edgecolor="black",
                alpha=1.0 if j == i else 0.75,
                facecolor=cmap(colors[index]),
                lw=1
            )
            axes[3].fill(
                *zip(*polygon),
                edgecolor="black",
                alpha=1.0 if j == i else 0.75,
                facecolor="w",
                lw=1
            )

            if j == i:
                axes[3].fill(
                    *zip(*polygon),
                    edgecolor="black",
                    alpha=1.0,
                    facecolor=cmap(colors[index]),
                    lw=1
                )

        axes[0].set_xticks([])
        axes[0].set_yticks([])
        axes[0].set_xlim(xlim_image_plane)
        axes[0].set_ylim(ylim_image_plane)
        axes[1].set_xticks([])
        axes[1].set_yticks([])
        axes[1].set_xlim(xlim_image_plane)
        axes[1].set_ylim(ylim_image_plane)
        axes[2].set_xticks([])
        axes[2].set_yticks([])
        axes[2].set_xlim(xlim_source_plane)
        axes[2].set_ylim(ylim_source_plane)
        axes[3].set_xticks([])
        axes[3].set_yticks([])
        axes[3].set_xlim(xlim_source_plane)
        axes[3].set_ylim(ylim_source_plane)
        plt.savefig(
            "{}/pixel_{}_continuum_model.png".format(directory, i)
        )
        plt.close()
        #plt.show()
