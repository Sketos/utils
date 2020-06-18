import numpy as np
import matplotlib.pyplot as plt

from astropy import modeling


def Gaussian2D(shape_2d, amplitude, x_mean, y_mean, x_stddev, y_stddev, theta, xy_meshgrids=None):
    # TODO: Do I need both shape_2d

    # if shape_2d:
    #     n_pixels_x, n_pixels_y = shape_2d
    # else:
    #     raise ValueError

    if xy_meshgrids is None:
        xy_meshgrids = np.meshgrid(
            np.arange(shape_2d[0]),
            np.arange(shape_2d[1])
        )

    # ...
    Gaussian2D = modeling.models.Gaussian2D(
        amplitude=amplitude,
        x_mean=x_mean,
        y_mean=y_mean,
        x_stddev=x_stddev,
        y_stddev=y_stddev,
        theta=theta
    )

    return Gaussian2D(*xy_meshgrids)


def Gaussian2D_from_grid_shape():
    pass

def Gaussian2D_from_grid():
    pass


if __name__ == "__main__":

    n_pixels = 30
    shape_2d = (n_pixels, n_pixels)

    n_pixels_x, n_pixels_y = shape_2d
    x = np.arange(n_pixels_x)
    y = np.arange(n_pixels_y)
    x_meshgrid, y_meshgrid = np.meshgrid(x, y)

    # plt.figure()
    # plt.imshow(y_meshgrid)
    # plt.colorbar()
    # plt.show()
    # exit()

    # plt.figure()
    # plt.imshow(y_meshgrid)
    # plt.colorbar()
    # plt.show()
    # exit()

    model = Gaussian2D(
        xy_meshgrids=(x_meshgrid, y_meshgrid),
        shape_2d=(n_pixels, n_pixels),
        amplitude=1.0,
        x_mean=15.0,
        y_mean=10.0,
        x_stddev=0.5,
        y_stddev=0.75,
        theta=45.0
    )

    plt.figure()
    plt.imshow(model, cmap="jet")
    plt.axvline(n_pixels / 2.0, linestyle="--", color="w")
    plt.axhline(n_pixels / 2.0, linestyle="--", color="w")
    plt.show()
