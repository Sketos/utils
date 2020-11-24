
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import patches


def add_patch_to_imshow():

    N = 100
    pixel_scale = 0.5
    a = np.random.normal(size=(N, N))


    ellipse = patches.Ellipse(
        xy=(N/2.0, N/2.0),
        width=20,
        height=5,
        angle=90
    )

    figure, axes = plt.subplots(nrows=1, ncols=1)

    axes.imshow(a)

    axes.add_artist(ellipse)

    plt.show()


if __name__ == "__main__":


    add_patch_to_imshow()
