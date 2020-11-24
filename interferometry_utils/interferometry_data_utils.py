import numpy as np
import matplotlib.pyplot as plt


def SNR_from_interferomter(interferometer):
    return SNR(
        visibilities=interferometer.visibilities,
        sigma=interferometer.noise_map,
        uv_wavelengths=interferometer.uv_wavelengths
    )

def SNR(visibilities, sigma, uv_wavelengths):
    """
    Powell et al 2020

    """

    amplitudes = np.hypot(visibilities[:, 0], visibilities[:, 1])

    sigma_amplitudes = np.sqrt(
        (visibilities[:, 0]**2.0 * sigma[:, 0]**2.0 + visibilities[:, 1]**2.0 * sigma[:, 1]**2.0) / amplitudes**2.0
    )

    snr = np.sqrt(
        np.sum(amplitudes**2.0 / sigma_amplitudes**2.0)
    )

    # uv_distance = np.hypot(uv_wavelengths[:, 0], uv_wavelengths[:, 1])
    #
    # plt.figure()
    # plt.plot(uv_distance, amplitudes**2.0 / sigma_amplitudes**2.0, linestyle="None", marker="o")
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.show()
    # exit()

    # print(
    #     "SNR (scaled) = {}".format(snr / visibilities.shape[0])
    # )
    # print(
    #     "SNR = {}".format(snr)
    # )

    #values = np.hypot(visibilities[..., 0], visibilities[..., 1])

    #np.sqrt(np.sum())

    return snr


def SNR_from_dataset(dataset):
    pass

def SNR_from_visibilities_and_sigma(visibilities, sigma):
    pass
