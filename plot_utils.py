import matplotlib.pyplot as plt


def plot_cube(cube, ncols):
    """

    Parameters
    ----------

    cube:

    ncols:

    figsize: MAKE THIS AN INPUT

    """

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

    figsize_x = 20
    figsize_y = 10

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

    k = 0
    for i in range(nrows):
        for j in range(ncols):
            if k < N:
                axes[i, j].imshow(
                    cube[k, :, :]
                )
                axes[i, j].set_xticks([])
                axes[i, j].set_yticks([])
                k += 1
            else:
                axes[i, j].axis("off")

    plt.subplots_adjust(wspace=0.01, hspace=0.01)
    plt.show()
