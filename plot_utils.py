import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.pylab as pl
from mpl_toolkits.axes_grid1 import make_axes_locatable

from spectral_utils import get_spectrum_from_cube


# NOTE
def plot_cube(cube, ncols, z_slices=None, points=None, cmin=None, cmax=None, extent=None, xmin=None, xmax=None, ymin=None, ymax=None, cube_contours=None, figsize=None, imshow_kwargs={}, subplots_kwargs={"wspace":0.01, "hspace":0.01}):

    if cube.shape[0] == len(z_slices):
        pass
    else:
        raise ValueError

    if cmin is None:
        cmin = 0
    if cmax is None:
        cmax = cube.shape[0]

    # ...
    cube = cube[cmin:cmax, :, :]

    # ...
    N, n_pixels_x, n_pixels_y = cube.shape # NOTE: remane N -> number_of_slices

    # ...
    if N % ncols == 0:
        nrows = int(N / ncols)
    else:
        nrows = int(N / ncols) + 1

    # figsize_x = 20
    # if figsize_x == 20:
    #     figsize_y = nrows * 4

    if figsize is not None:
        figsize_x, figsize_y = figsize
    else:
        figsize_x = 16
        figsize_y = 8

    figure, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(
            figsize_x,
            figsize_y
        )
    )

    # vmin = 0.0
    # vmax = 0.00005
    # vmin=vmin,
    # vmax=vmax

    if points is not None:
        plot_points = True
    else:
        plot_points = False

    vmin = np.nanmin(cube)
    vmax = np.nanmax(cube)

    k = 0

    x_text = 5
    y_text = 15
    if extent is not None:
        pass


    for i in range(nrows):
        for j in range(ncols):
            if k < N:
                axes[i, j].imshow(
                    cube[k, :, :],
                    cmap="jet",
                    interpolation="None",
                    extent=extent,
                    vmin=vmin,
                    vmax=vmax,
                    **imshow_kwargs
                )
                if cube_contours is not None:
                    axes[i, j].contour(cube_contours[k, :, :])
                axes[i, j].set_xticks([])
                axes[i, j].set_yticks([])
                axes[i, j].text(x_text, y_text, "{0:.1f} km / s".format(z_slices[k]), color="w")

                if plot_points:
                    axes[i, j].plot(points[:, 0], points[:, 1], color="black")
                k += 1
            else:
                axes[i, j].axis("off")



    plt.subplots_adjust(
        **subplots_kwargs
    )
    plt.show()


def plot_spectrum_from_cube(cube, figsize=(15, 10)):

    y = get_spectrum_from_cube(
        cube=cube
    )

    plt.figure(
        figsize=figsize
    )
    plt.plot(y)
    plt.show()


def plot_visibilities(visibilities, figsize=None, spectral_mask=None):

    #total_number_of_channels = visibilities.shape[0]

    plt.figure(figsize=figsize)

    if len(visibilities.shape) == 1:

        raise ValueError

    elif len(visibilities.shape) == 2:

        if visibilities.shape[-1] == 2:

            plt.plot(
                visibilities[:, 0],
                visibilities[:, 1],
                linestyle="None",
                marker="."
            )

    elif len(visibilities.shape) == 3:

        if visibilities.shape[-1] == 2:


            colors = pl.cm.jet(
                np.linspace(0, 1, visibilities.shape[0])
            )
            for i in range(visibilities.shape[0]):
                plt.plot(
                    visibilities[i, :, 0],
                    visibilities[i, :, 1],
                    linestyle="None",
                    marker=".",
                    color=colors[i]
                )

    else:

        raise ValueError

    plt.xlabel(r"$V_{R}$ (Jy)", fontsize=15)
    plt.ylabel(r"$V_{I}$ (Jy)", fontsize=15)
    plt.show()


def plot_uv_wavelengths(
    uv_wavelengths,
    figsize=None,
    xlim=None,
    ylim=None,
    savefig=False
):

    if figsize is None:
        figsize = (12, 12)

    plt.figure(
        figsize=figsize
    )

    # NOTE:
    if len(uv_wavelengths.shape) == 1:
        raise ValueError
    elif len(uv_wavelengths.shape) == 2:

        if uv_wavelengths.shape[-1] == 2:
            plt.plot(
                uv_wavelengths[:, 0] * 10**-3.0,
                uv_wavelengths[:, 1] * 10**-3.0,
                linestyle="None",
                marker=".",
                color="black"
            )

    elif len(uv_wavelengths.shape) == 3:

        if uv_wavelengths.shape[-1] == 2:
            colors = pl.cm.jet(
                np.linspace(0, 1, uv_wavelengths.shape[0])
            )

            for i in range(uv_wavelengths.shape[0]):
                plt.plot(
                    uv_wavelengths[i, :, 0] * 10**-3.0,
                    uv_wavelengths[i, :, 1] * 10**-3.0,
                    linestyle="None",
                    marker=".",
                    color=colors[i]
                )

    plt.xlabel(r"u (k$\lambda$)", fontsize=15)
    plt.ylabel(r"v (k$\lambda$)", fontsize=15)
    if savefig:
        plt.savefig("uv_wavelengths.png")
    #plt.show()


# def plot_amplitude__vs__uv_distance(visibilities, uv_wavelengths, figsize=None):
#     pass
