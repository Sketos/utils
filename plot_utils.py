import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.pylab as pl
from mpl_toolkits.axes_grid1 import make_axes_locatable

from spectral_utils import get_spectrum_from_cube


class Point:
    def __init__(self, y, x, marker="o", markersize=5, color="black"):

        self.y = y
        self.x = x

        self.marker = marker
        self.markersize = markersize

        self.color = color


# NOTE
def plot_cube(
    cube,
    ncols,
    show=True,
    z_labels=None,
    z_labels_color="black",
    points=None,
    cmin=None,
    cmax=None,
    extent=None,
    vmin=None,
    vmax=None,
    xmin=None,
    xmax=None,
    ymin=None,
    ymax=None,
    xlim=None,
    ylim=None,
    cube_contours=None,
    figsize=None,
    imshow_kwargs={},
    subplots_kwargs={
        "wspace":0.01,
        "hspace":0.01,
        "left":0.025,
        "right":0.975,
        "bottom":0.05,
        "top":0.995
    }
):

    if z_labels is not None:
        if cube.shape[0] == len(z_labels):
            pass
        else:
            raise ValueError(
                "The number of channels must be the same as"
            )

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

    if vmin is None:
        vmin = np.nanmin(cube)
    if vmax is None:
        vmax = np.nanmax(cube)


    x_text = 0.05 * cube.shape[1]
    y_text = 0.10 * cube.shape[2]
    if extent is not None:
        pass

    k = 0
    for i in range(nrows):
        for j in range(ncols):
            if k < N:
                im = axes[i, j].imshow(
                    cube[k, :, :],
                    cmap="jet",
                    interpolation="None",
                    extent=extent,
                    vmin=vmin,
                    vmax=vmax,
                    **imshow_kwargs
                )
                if cube_contours is not None:
                    axes[i, j].contour(
                        cube_contours[k, :, :],
                        colors="black",
                        alpha=0.25
                    )
                axes[i, j].set_xticks([])
                axes[i, j].set_yticks([])

                # if z_labels is not None:
                #     axes[i, j].text(
                #         x_text,
                #         y_text,
                #         "{0:.1f} km / s".format(
                #             z_labels[k]
                #         ),
                #         color=z_labels_color
                #     )

                if xlim is not None and ylim is not None:
                    axes[i, j].set_xlim(xlim)
                    axes[i, j].set_ylim(ylim)

                # if plot_points:
                #     axes[i, j].plot(
                #         points[:, 0],
                #         points[:, 1],
                #         linestyle="None",
                #         marker="+",
                #         markersize=10,
                #         color="black"
                #     )

                # NOTE: under development
                if points:
                    for point in points:
                        if isinstance(point, Point):
                            axes[i, j].plot(
                                point.x,
                                point.y,
                                linestyle="None",
                                marker=point.marker,
                                markersize=point.markersize,
                                color=point.color
                            )


                k += 1
            else:
                axes[i, j].axis("off")



    plt.subplots_adjust(
        **subplots_kwargs
    )

    # cbar = figure.colorbar(
    #     im, ax=axes.ravel().tolist(), location="top", pad=0.01, fraction=0.1, aspect=50)

    if show:
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


def subplots_from_images(images):

    figure, axes = plt.subplots(
        nrows=1, ncols=len(images)
    )
    for i in range(len(images)):
        im = axes[i].imshow(images[i])

        divider = make_axes_locatable(axes[i])
        cax = divider.append_axes('right', size='5%', pad=0.05)
        figure.colorbar(im, cax=cax, orientation='vertical')

    plt.show()

# def plot_amplitude__vs__uv_distance(visibilities, uv_wavelengths, figsize=None):
#     pass
