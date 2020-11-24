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


def fit_subplots(
    fit,
    xlim_image_plane=None,
    ylim_image_plane=None,
    xlim_source_plane=None,
    ylim_source_plane=None
):

    extent = [
        np.min(fit.grid[:, 1]),
        np.max(fit.grid[:, 1]),
        np.max(fit.grid[:, 0]),
        np.min(fit.grid[:, 0])
    ]

    dirty_image = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.visibilities
    )
    dirty_image_model = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.model_visibilities
    )
    dirty_residuals = fit.masked_interferometer.transformer.image_from_visibilities(
        visibilities=fit.residual_map
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
        aspect="auto",
        vmin=vmin,
        vmax=vmax
    )

    axes[1].imshow(
        dirty_image_model,
        cmap="jet",
        extent=extent,
        aspect="auto",
        vmin=vmin,
        vmax=vmax
    )

    axes[2].imshow(
        dirty_residuals,
        cmap="jet",
        extent=extent,
        aspect="auto",
    )


    regions, vertices = voronoi_utils.voronoi_polygons(
        voronoi=fit.inversion.mapper.voronoi
    )

    reconstruction = fit.inversion.reconstruction

    colors = np.divide(
        reconstruction,
        np.max(reconstruction)
    )

    cmap = plt.get_cmap("jet")

    for i, (region, index) in enumerate(
        zip(regions, range(fit.inversion.mapper.pixels))
    ):

        polygon = vertices[region]

        axes[3].fill(
            *zip(*polygon),
            edgecolor="black",
            alpha=1.0,
            facecolor=cmap(colors[index]),
            lw=1
        )


    axes[0].set_xticks([])
    axes[0].set_yticks([])
    # if xlim_image_plane is not None:
    #     axes[0].set_xlim(xlim_image_plane)
    #     axes[0].set_ylim(ylim_image_plane)
    #     axes[1].set_xlim(xlim_image_plane)
    #     axes[1].set_ylim(ylim_image_plane)
    #     axes[2].set_xlim(xlim_image_plane)
    #     axes[2].set_ylim(ylim_image_plane)

    axes[1].set_xticks([])
    axes[1].set_yticks([])

    axes[2].set_xticks([])
    axes[2].set_yticks([])

    axes[3].set_xticks([])
    axes[3].set_yticks([])
    # axes[3].set_xlim(xlim_source_plane)
    # axes[3].set_ylim(ylim_source_plane)
    plt.show()
