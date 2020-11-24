import numpy as np
import pylab as pl

import matplotlib.pyplot as plt


def plot_list_of_visibilities_subplots():
    pass


def plot_list_of_visibilities(
    list_of_visibilities,
    figure=None,
    show=False,
    save=False
):

    for i, visibilities in enumerate(list_of_visibilities):
        plot_visibilities(
            visibilities=visibilities, figure=None, show=False, save=False
        )

    plt.xlabel(r"$R(V_{ij})$", fontsize=15)
    plt.ylabel(r"$I(V_{ij})$", fontsize=15)

    if show:
        plt.show()


def plot_visibilities_and_noise_map(
    visibilities,
    noise_map,
    pol=False,
    figure=None,
    show=False,
    save=False,
    directory="./"
):

    if len(visibilities.shape) == 1:

        raise ValueError(
            "This has not beem implemented yet"
        )

    elif len(visibilities.shape) == 2:

        visibilities_real = visibilities[:, 0]
        visibilities_imag = visibilities[:, 1]

        plt.plot(
            visibilities_real,
            visibilities_imag,
            linestyle="None",
            marker=".",
            color="b"
        )

        visibilities_real_rms = np.sqrt(np.mean(visibilities_real**2.0))
        visibilities_imag_rms = np.sqrt(np.mean(visibilities_imag**2.0))

        plt.axvline(visibilities_real_rms, linestyle="--", color="black")
        plt.axhline(visibilities_imag_rms, linestyle="--", color="black")


        noise_map_real = np.mean(noise_map[:, 0],)
        noise_map_imag = np.mean(noise_map[:, 1],)

        plt.axvline(noise_map_real, linestyle="--", color="r")
        plt.axhline(noise_map_imag, linestyle="--", color="r")

    else:
        raise ValueError("Not implemented yet.")

    plt.xlabel(r"$R(V_{ij})$", fontsize=15)
    plt.ylabel(r"$I(V_{ij})$", fontsize=15)

    if save:
        plt.savefig(
            "{}/visibilities.png".format(directory),
            overwtite=True
        )
    if show:
        plt.show()
    exit()


def plot_visibilities(
    visibilities,
    show_rms=True,
    pol=True,
    figure=None,
    show=False,
    save=False,
    directory="./"
):

    if len(visibilities.shape) == 1:
        raise ValueError(
            "This has not beem implemented yet"
        )

    elif len(visibilities.shape) == 2:

        visibilities_real = visibilities[:, 0]
        visibilities_imag = visibilities[:, 1]

        plt.plot(
            visibilities_real,
            visibilities_imag,
            linestyle="None",
            marker="."
        )

        if show_rms:
            visibilities_real_rms = np.sqrt(np.mean(visibilities_real**2.0))
            visibilities_imag_rms = np.sqrt(np.mean(visibilities_imag**2.0))

            plt.axvline(visibilities_real_rms, linestyle="--", color="black")
            plt.axhline(visibilities_imag_rms, linestyle="--", color="black")

    elif len(visibilities.shape) == 3:

        if pol:
            visibilities_pol_0 = visibilities[0, ...]
            visibilities_pol_1 = visibilities[1, ...]

            print(visibilities_pol_0.shape)

            plt.plot(
                visibilities_pol_0,
                visibilities_pol_1,
                linestyle="None",
                marker="."
            )

        else:
            raise ValueError(
                "This has not beem implemented yet"
            )

    elif len(visibilities.shape) == 4:

        # plt.plot(
        #     np.ndarray.flatten(visibilities[0, ..., 0]),
        #     np.ndarray.flatten(visibilities[..., 1]),
        #     linestyle="None",
        #     marker=".",
        #     color="b"
        # )

        plt.plot(
            np.ndarray.flatten(visibilities[0, :, :, 0]),
            np.ndarray.flatten(visibilities[0, :, :, 1]),
            linestyle="None",
            marker=".",
            color="b"
        )
        plt.plot(
            np.ndarray.flatten(visibilities[1, :, :, 0]),
            np.ndarray.flatten(visibilities[1, :, :, 1]),
            linestyle="None",
            marker=".",
            color="r"
        )

    plt.xlabel(r"$R(V_{ij})$", fontsize=15)
    plt.ylabel(r"$I(V_{ij})$", fontsize=15)

    if save:
        plt.savefig("{}/visibilities.png".format(directory), overwtite=True)
    if show:
        plt.show()


def plot_uv_wavelengths(uv_wavelengths):


    if len(uv_wavelengths.shape) == 1:
        raise ValueError(
            "This has not beem implemented yet"
        )

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
