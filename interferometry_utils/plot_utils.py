import numpy as np
import pylab as pl
import matplotlib.pyplot as plt


def plot_uv_wavelengths(uv_wavelengths):

    #plt.figure()

    if len(uv_wavelengths.shape) == 1:
        raise ValueError
    elif len(uv_wavelengths.shape) == 2:
        u_wavelengths = uv_wavelengths[:, 0]
        v_wavelengths = uv_wavelengths[:, 1]

        plt.plot(
            u_wavelengths,
            v_wavelengths,
            linestyle="None",
            marker="."
        )

    elif len(uv_wavelengths.shape) == 3:
        u_wavelengths = uv_wavelengths[:, :, 0]
        v_wavelengths = uv_wavelengths[:, :, 1]

        colors = pl.cm.jet(
            np.linspace(0, 1, uv_wavelengths.shape[0])
        )
        for i in range(uv_wavelengths.shape[0]):
            plt.plot(
                u_wavelengths[i, :],
                v_wavelengths[i, :],
                linestyle="None",
                marker=".",
                color=colors[i]
            )


    #plt.show()
