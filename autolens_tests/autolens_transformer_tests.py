import os
import sys

import numpy as np

import matplotlib.pyplot as plt

import autolens as al


sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)

import autolens_utils.autolens_plot_utils as autolens_plot_utils


def test_1(uv_wavelengths, grid, image_1, image_2, transformer_class):

    transformer_1 = transformer_class(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
        apply_shift=True
    )
    transformer_2 = transformer_class(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
        apply_shift=False
    )

    visibilities_1 = transformer_1.visibilities_from_image(
        image=image_1
    )
    visibilities_2 = transformer_2.visibilities_from_image(
        image=image_2
    )

    # plt.figure()
    # plt.plot(
    #     visibilities_1[:, 0],
    #     visibilities_1[:, 1],
    #     linestyle="None",
    #     marker="o",
    #     color="b",
    #     alpha=0.5
    # )
    # plt.plot(
    #     visibilities_2[:, 0],
    #     visibilities_2[:, 1],
    #     linestyle="None",
    #     marker="o",
    #     color="r",
    #     alpha=0.5
    # )
    # plt.show()


    dirty_image_1 = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
        visibilities=visibilities_1,
        transformer=transformer_1
    )
    dirty_image_2 = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
        visibilities=visibilities_2,
        transformer=transformer_2
    )

    figure, axes = plt.subplots(
        nrows=1,
        ncols=3
    )

    axes[0].imshow(
        dirty_image_1,
        cmap="jet"
    )
    axes[1].imshow(
        dirty_image_2,
        cmap="jet"
    )
    axes[2].imshow(
        np.subtract(dirty_image_1, dirty_image_2),
        cmap="jet"
    )

    plt.show()


def test_2(uv_wavelengths, grid, tracer_1, tracer_2, transformer_class):

    transformer_1 = transformer_class(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
        apply_shift=True
    )
    transformer_2 = transformer_class(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
        apply_shift=False
    )

    visibilities_1 = tracer_1.profile_visibilities_from_grid_and_transformer(
        grid=grid, transformer=transformer_1
    )
    visibilities_2 = tracer_2.profile_visibilities_from_grid_and_transformer(
        grid=grid, transformer=transformer_2
    )

    dirty_image_1 = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
        visibilities=visibilities_1,
        transformer=transformer_1
    )
    dirty_image_2 = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
        visibilities=visibilities_2,
        transformer=transformer_2
    )

    figure, axes = plt.subplots(
        nrows=1,
        ncols=3
    )

    axes[0].imshow(
        dirty_image_1,
        cmap="jet"
    )
    axes[1].imshow(
        dirty_image_2,
        cmap="jet"
    )
    axes[2].imshow(
        np.subtract(dirty_image_1, dirty_image_2),
        cmap="jet"
    )

    plt.show()


def test_3(uv_wavelengths, grid, tracer):

    transformer_DFT = al.TransformerDFT(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
    )

    transformer_NUFFT = al.TransformerNUFFT(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
        apply_shift=True
    )

    visibilities_DFT = tracer.profile_visibilities_from_grid_and_transformer(
        grid=grid, transformer=transformer_DFT
    )
    visibilities_NUFFT = tracer.profile_visibilities_from_grid_and_transformer(
        grid=grid, transformer=transformer_NUFFT
    )

    plt.figure()
    plt.plot(
        visibilities_DFT[:, 0],
        visibilities_DFT[:, 1],
        linestyle="None",
        marker="o",
        markersize=2,
        color="black",
        alpha=0.5
    )

    plt.plot(
        visibilities_NUFFT[:, 0],
        visibilities_NUFFT[:, 1],
        linestyle="None",
        marker="o",
        markersize=1,
        color="r",
        alpha=1.0
    )
    plt.show()


    # dirty_image_1 = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
    #     visibilities=visibilities_DFT,
    #     transformer=transformer_NUFFT
    # )
    # dirty_image_2 = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
    #     visibilities=visibilities_NUFFT,
    #     transformer=transformer_NUFFT
    # )
    #
    # figure, axes = plt.subplots(
    #     nrows=1,
    #     ncols=3
    # )
    #
    # axes[0].imshow(
    #     dirty_image_1,
    #     cmap="jet"
    # )
    # axes[1].imshow(
    #     dirty_image_2,
    #     cmap="jet"
    # )
    # axes[2].imshow(
    #     np.subtract(dirty_image_1, dirty_image_2),
    #     cmap="jet"
    # )
    #
    # plt.show()
