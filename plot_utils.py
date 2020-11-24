import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.pylab as pl
from mpl_toolkits.axes_grid1 import make_axes_locatable

from astropy.io import fits

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
    contours=None,
    contour_levels=None,
    masked_slices=None,
    figsize=None,
    origin=None,
    imshow_kwargs={},
    subplots_kwargs={
        "wspace":0.01,
        "hspace":0.01,
        "left":0.025,
        "right":0.975,
        "bottom":0.05,
        "top":0.995
    },
    save=False,
    norm=None
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

    condition = False
    if contours is not None:
        if len(contours.shape) < len(cube.shape):
            condition = True

    if points is not None:
        plot_points = True
    else:
        plot_points = False

    if masked_slices is not None:
        for i in masked_slices:
            cube[i] = np.nan
    else:
        masked_slices = []

    if vmin is None:
        vmin = np.nanmin(cube)
    if vmax is None:
        vmax = np.nanmax(cube)

    # print(
    #     "vmin = ", vmin,
    #     "vmax = ", vmax
    # )
    # exit()

    x_text = 0.05 * cube.shape[1]
    y_text = 0.10 * cube.shape[2]
    if extent is not None:
        pass

    k = 0
    for i in range(nrows):
        for j in range(ncols):
            if k < N:
                if k in masked_slices:
                    axes[i, j].axis("off")
                else:
                    im = axes[i, j].imshow(
                        cube[k, :, :],
                        cmap="jet",
                        aspect="auto",
                        interpolation="None",
                        origin=origin,
                        extent=extent,
                        vmin=vmin,
                        vmax=vmax,
                        norm=norm,
                        **imshow_kwargs
                    )
                    if contours is not None:
                        if condition:
                            axes[i, j].contour(
                                contours,
                                levels=contour_levels,
                                colors="black",
                                alpha=0.5
                            )
                        else:
                            axes[i, j].contour(
                                contours[k, ...],
                                levels=contour_levels,
                                colors="black",
                                alpha=0.5
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

    if save:
        plt.savefig("figure.png")
    elif show:
        plt.show()




# def ff(ncols):
#
#     if N % ncols == 0:
#         nrows = int(N / ncols)
#     else:
#         nrows = int(N / ncols) + 1

def plot_cube_from_axes(cube, axes, cmap="jet"):

    vmin = np.nanmin(cube)
    vmax = np.nanmax(cube)

    k = 0
    for i in range(axes.shape[0]):
        for j in range(axes.shape[1]):

            if k < cube.shape[0]:

                im = axes[i, j].imshow(
                    cube[k, :, :],
                    cmap=cmap,
                    vmin=vmin,
                    vmax=vmax
                )

                axes[i, j].set_xticks([])
                axes[i, j].set_yticks([])

            else:

                axes[i, j].axis("off")

            k += 1





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


def plot_cubes(cube_1, cube_2, nrows, ncols=2, axis=0):


    figure, axes = plt.subplots(
        nrows=nrows, ncols=int(4 * ncols)
    )

    if cube_1.shape[axis] == cube_2.shape[axis]:

        k = 0

        vmin = np.nanmin(cube_1)
        vmax = np.nanmax(cube_1)

        i = 0
        j = 0
        for n in range((nrows * ncols)):

            if k < cube_1.shape[axis]:


                axes[i, j + 0].imshow(
                    cube_1[k, ...],
                    vmin=vmin,
                    vmax=vmax,
                    cmap="jet"
                )
                axes[i, j + 1].imshow(
                    cube_2[k, ...],
                    vmin=vmin,
                    vmax=vmax,
                    cmap="jet"
                )
                axes[i, j + 2].imshow(
                    np.subtract(cube_1[k, ...], cube_2[k, ...]),
                    vmin=vmin,
                    vmax=vmax,
                    cmap="jet"
                )
                axes[i, j + 3].axis("off")

            else:

                axes[i, j + 0].axis("off")
                axes[i, j + 1].axis("off")
                axes[i, j + 2].axis("off")
                axes[i, j + 3].axis("off")

            if (n + 1) % nrows == 0:
                j += 4
                i = 0
            else:
                i += 1



            k += 1
    else:
        raise ValueError("This is not supported")

    for i in range(axes.shape[0]):
        for j in range(axes.shape[1]):
            axes[i, j].set_xticks([])
            axes[i, j].set_yticks([])


    plt.subplots_adjust(wspace=0.0, hspace=0.0, left=0.05, right=0.95, bottom=0.05, top=0.95)
    plt.show()


if __name__ == "__main__":

    # cube = np.zeros(shape=(128, 100, 100))
    #
    # cube[0] = np.nan
    # #print(cube[0])
    #
    # plot_cube(cube=cube, ncols=16, masked_slices=[0, 1, 2, 126, 127])

    # ======================================================================== #

    def z_mask_from_zmin_and_zmax(shape, zmin, zmax):

        mask = np.full(
            shape=shape,
            fill_value=False
        )

        mask[:zmin] = True
        mask[zmax:] = True

        return mask

    def plot_cube_extension(filename, ncols, zmin=None, zmax=None, Nx=None, Ny=None, xmin=None, xmax=None, ymin=None, ymax=None):

        data = fits.getdata(
            filename=filename
        )
        data = np.squeeze(data)

        shape = data.shape

        if Nx is not None and Ny is not None:

            xmin = int(data.shape[1] / 2.0 - Nx)
            xmax = int(data.shape[1] / 2.0 + Nx)
            ymin = int(data.shape[2] / 2.0 - Ny)
            ymax = int(data.shape[2] / 2.0 + Ny)

            data_xy_masked = data[:, ymin:ymax, xmin:xmax]

        elif xmin is not None and xmax is not None and ymin is not None and ymax is not None:

            data_xy_masked = data[:, ymin:ymax, xmin:xmax]

        else:

            data_xy_masked = data

        z_mask = z_mask_from_zmin_and_zmax(
            shape=data.shape[0],
            zmin=zmin,
            zmax=zmax
        )

        data_xy_masked_z_masked = data_xy_masked[~z_mask]

        plot_cube(
            cube=data_xy_masked_z_masked,
            ncols=ncols
        )


    # plot_cube_extension(
    #     filename="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_112.1/ALESS_112.1_spw_23.clean.cube.image.pbcor.fits",
    #     ncols=5,
    #     Nx=32,
    #     Ny=32,
    #     zmin=80,
    #     zmax=110
    # )

    # plot_cube_extension(
    #     filename="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging/ALESS71_spw_0.clean.cube.image.pbcor.fits",
    #     ncols=5,
    #     xmin=512,
    #     xmax=1024,
    #     ymin=0,
    #     ymax=512,
    #     zmin=40,
    #     zmax=60
    # )



    # ======================================================================== #



    cube_1 = np.random.normal(size=(20, 128, 128))
    cube_2 = np.random.normal(size=(20, 128, 128))

    plot_cubes(cube_1=cube_1, cube_2=cube_2, nrows=10, ncols=2)
