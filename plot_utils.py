import numpy as np
import matplotlib.pyplot as plt

from spectral_utils import get_spectrum_from_cube


def plot_cube(cube, ncols, cmin=None, cmax=None, xmin=None, xmax=None, ymin=None, ymax=None, cube_contours=None, figsize=None, imshow_kwargs={}, subplots_kwargs={"wspace":0.01, "hspace":0.01}):
    """

    Parameters
    ----------

    cube:

    ncols:

    figsize: MAKE THIS AN INPUT

    """

    if cmin is None:
        cmin = 0
    if cmax is None:
        cmax = cube.shape[0]

    # ...
    cube = cube[cmin:cmax, :, :]

    # ...
    N = cube.shape[0]

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

    vmin = np.nanmin(cube)
    vmax = np.nanmax(cube)

    k = 0

    for i in range(nrows):
        for j in range(ncols):
            if k < N:
                axes[i, j].imshow(
                    cube[k, :, :],
                    cmap="jet",
                    interpolation="None",
                    vmin=vmin,
                    vmax=vmax,
                    **imshow_kwargs
                )
                if cube_contours is not None:
                    axes[i, j].contour(cube_contours[k, :, :])
                axes[i, j].set_xticks([])
                axes[i, j].set_yticks([])
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
