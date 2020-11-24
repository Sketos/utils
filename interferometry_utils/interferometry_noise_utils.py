import os
import sys
import copy
import random

import numpy as np

import matplotlib.pyplot as plt

sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)

import reshape_utils as reshape_utils


def estimate_sigma_from_visibilities_rms(visibilities, pol=False):

    rms = visibilities_rms(visibilities=visibilities, pol=pol)

    sigma = np.ones(shape=visibilities.shape)

    if len(visibilities.shape) == 2:

        sigma[:, 0] *= rms[0]
        sigma[:, 1] *= rms[1]

    return sigma

# NOTE: This is only the case for simulation. In real observations the noise
# is likely to change with time
def visibilities_rms(visibilities, pol=False):

    def rms(a, axis=0):

        return np.sqrt(np.mean(a=a**2.0, axis=axis))


    if len(visibilities.shape) == 2:

        if pol:
            raise ValueError("This case is not possible")

        rms_real = rms(a=visibilities[:, 0], axis=0)
        rms_imag = rms(a=visibilities[:, 1], axis=0)

        _visibilities_rms = np.stack(
            arrays=(rms_real, rms_imag), axis=-1
        )

    if len(visibilities.shape) == 3:

        if pol:
            # NOTE: The output array should have a shape of (2, 2)

            if not visibilities.shape[0] == 2:
                raise ValueError("This case is not possible")
            else:

                visibilities_pol_0 = visibilities[0, ...]
                visibilities_pol_1 = visibilities[0, ...]

                rms_pol_0_real = rms(a=visibilities_pol_0[:, 0], axis=0)
                rms_pol_0_imag = rms(a=visibilities_pol_0[:, 1], axis=0)
                rms_pol_1_real = rms(a=visibilities_pol_1[:, 0], axis=0)
                rms_pol_1_imag = rms(a=visibilities_pol_1[:, 1], axis=0)

                rms_real = np.stack(arrays=(rms_pol_0_real, rms_pol_1_real), axis=0)
                rms_imag = np.stack(arrays=(rms_pol_0_imag, rms_pol_1_imag), axis=0)

                _visibilities_rms = np.stack(
                    arrays=(rms_real, rms_imag), axis=-1
                )

        else:
            # NOTE: The output array should have a shape of (n_c, 2)

            _visibilities_rms = np.zeros(
                shape=(visibilities.shape[0], 2)
            )
            for i in range(visibilities.shape[0]):
                _visibilities_rms[i, 0] = rms(
                    a=visibilities[i, :, 0], axis=0
                )
                _visibilities_rms[i, 1] = rms(
                    a=visibilities[i, :, 1], axis=0
                )

    if len(visibilities.shape) == 4:

        if pol:

            if not visibilities.shape[0] == 2:
                raise ValueError("This case is not possible")
            else:

                visibilities_pol_0 = visibilities[0, ...]
                visibilities_pol_1 = visibilities[0, ...]

                visibilities_rms_pol_0 = np.zeros(
                    shape=(visibilities.shape[1], 2)
                )
                visibilities_rms_pol_1 = np.zeros(
                    shape=(visibilities.shape[1], 2)
                )
                for i in range(visibilities.shape[1]):
                    visibilities_rms_pol_0[i, 0] = rms(
                        a=visibilities_pol_0[i, :, 0], axis=0
                    )
                    visibilities_rms_pol_0[i, 1] = rms(
                        a=visibilities_pol_0[i, :, 1], axis=0
                    )
                    visibilities_rms_pol_1[i, 0] = rms(
                        a=visibilities_pol_1[i, :, 0], axis=0
                    )
                    visibilities_rms_pol_1[i, 1] = rms(
                        a=visibilities_pol_1[i, :, 1], axis=0
                    )

                _visibilities_rms = np.stack(
                    arrays=(visibilities_rms_pol_0, visibilities_rms_pol_1), axis=0
                )

        else:
            raise ValueError("This has not been implemented yet")

    return _visibilities_rms


def noise_plot(visibilities, sigma, filename=None, zmin=None, zmax=None):


    visibilities_rms = np.zeros(
        shape=(visibilities.shape[0], 2)
    )
    for i in range(visibilities.shape[0]):
        visibilities_rms[i, 0] = np.sqrt(np.mean(visibilities[i, :, 0]**2.0))
        visibilities_rms[i, 1] = np.sqrt(np.mean(visibilities[i, :, 1]**2.0))

    sigma_mean = np.mean(
        a=sigma, axis=1
    )

    plt.figure()

    plt.plot(
        visibilities_rms[:, 0],
        linestyle="-",
        marker="o",
        color="b"
    )
    plt.plot(
        visibilities_rms[:, 1],
        linestyle="-",
        marker="o",
        color="r"
    )
    plt.plot(sigma_mean[:, 0], linestyle="--", color="b")
    plt.plot(sigma_mean[:, 1], linestyle="--", color="b")



    sigma_normalized = copy.copy(sigma)

    for i in range(sigma_normalized.shape[0]):

        sigma_normalized[i, :, 0] *= visibilities_rms[i, 0] / sigma_mean[i, 0]
        sigma_normalized[i, :, 1] *= visibilities_rms[i, 1] / sigma_mean[i, 1]

    sigma_normalized_mean = np.mean(
        a=sigma_normalized, axis=1
    )

    plt.plot(sigma_normalized_mean[:, 0], linestyle="--", color="g")
    plt.plot(sigma_normalized_mean[:, 1], linestyle="--", color="g")

    if zmin is not None:
        plt.axvline(zmin, linestyle="--", color="black")
    if zmax is not None:
        plt.axvline(zmax, linestyle="--", color="black")

    if filename is not None:
        pass
    else:
        plt.show()
    #plt.savefig(filename, overwrite=True)


# NOTE: This function is used for the noise map generated from simobserve (simulations)
def shuffle_noise(noise):

    def shuffle(a):

        a_copy = copy.deepcopy(a)
        random.shuffle(a_copy)

        return a_copy

    noise_shuffled = np.zeros(
        shape=noise.shape
    )

    if len(noise.shape) == 4:

        if noise.shape[0] == 2:
            for i in range(noise_shuffled.shape[0]):
                for j in range(noise_shuffled.shape[1]):
                    noise_shuffled[i, j, : , :] = shuffle(
                        a=noise[i, j, :, :]
                    )
        else:
            raise ValueError("This has not been implemented yet")

    else:
        raise ValueError("This has not been implemented yet")

    return noise_shuffled

if __name__ == "__main__":

    from astropy.io import fits

    filename_visibilities="/Volumes/Elements_v1/2013.1.00358.S/science_goal.uid___A001_X13e_X47/group.uid___A001_X13e_X48/member.uid___A001_X13e_X49/calibrated/width_128/uid___A002_Xa6c1df_X70f_field_GAMA15-1/visibilities_spw_0.fits"
    filename_sigma="/Volumes/Elements_v1/2013.1.00358.S/science_goal.uid___A001_X13e_X47/group.uid___A001_X13e_X48/member.uid___A001_X13e_X49/calibrated/width_128/uid___A002_Xa6c1df_X70f_field_GAMA15-1/sigma_spw_0.fits"
    visibilities = fits.getdata(filename=filename_visibilities)
    sigma = fits.getdata(filename=filename_sigma)

    print(visibilities.shape, sigma.shape)

    # # NOTE: Plot
    # plt.figure()
    # plt.plot(
    #     np.ndarray.flatten(visibilities[:, :, 0]),
    #     np.ndarray.flatten(visibilities[:, :, 1]),
    #     linestyle="None",
    #     marker="."
    # )
    # #plt.show()
    #
    # rms_real = np.sqrt(np.mean(np.ndarray.flatten(visibilities[0, :, 0]**2.0)))
    # rms_imag = np.sqrt(np.mean(np.ndarray.flatten(visibilities[0, :, 1]**2.0)))
    #
    # plt.axvline(rms_real, linestyle="--", color="black")
    # plt.axvline(-rms_real, linestyle="--", color="black")
    # plt.axhline(rms_imag, linestyle="--", color="black")
    # plt.axhline(-rms_imag, linestyle="--", color="black")
    #
    # # NOTE: Plot
    # plt.figure()
    # plt.hist(
    #     np.ndarray.flatten(sigma[:, :, 0]),
    #     bins=50,
    #     alpha=0.5
    # )
    # plt.hist(
    #     np.ndarray.flatten(sigma[:, :, 1]),
    #     bins=50,
    #     alpha=0.5
    # )
    # plt.show()
    # exit()
