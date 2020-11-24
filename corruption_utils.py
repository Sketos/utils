import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from astropy import units, \
                    constants

import autolens as al


sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)

import reshape_utils as reshape_utils


def corrupt_visibilities_from_f_matrix_and_stochastic_phase_errors(
    visibilities,
    f_T,
    stochastic_phase_errors,
    n_b,
    format="autolens"
):

    def plot_stochastic_phase_errors(stochastic_phase_errors):

        plt.figure()
        for i in range(stochastic_phase_errors.shape[0]):
            plt.plot(stochastic_phase_errors[i, :])

        plt.show()


    def reshape(a, n_b):

        if len(a.shape) > 1:
            return a.reshape(
                (int(a.shape[0] / n_b), n_b, -1)
            )
        else:
            return a.reshape(
                (int(a.shape[0] / n_b), n_b)
            )

    phases_reshaped = reshape(
        a=visibilities.phases,
        n_b=n_b
    )

    # NOTE: We can instead pass the (n_b, n_a) f_T matrix instead of having to reshape it
    f_T_reshaped = reshape(
        a=f_T,
        n_b=n_b
    )

    phases_corrupted_reshaped = np.zeros(
        shape=phases_reshaped.shape
    )
    for i in range(phases_reshaped.shape[0]):
        phases_corrupted_reshaped[i, :] = np.add(
            phases_reshaped[i, :],
            np.matmul(
                f_T_reshaped[i, :, :],
                stochastic_phase_errors[:, i]
            )
        )

    phases_corrupted = phases_corrupted_reshaped.reshape(visibilities.shape[0])

    return al.Visibilities(
        visibilities_1d=np.stack(
            arrays=(
                np.multiply(
                    visibilities.amplitudes,
                    np.cos(phases_corrupted)
                ),
                np.multiply(
                    visibilities.amplitudes,
                    np.sin(phases_corrupted)
                )
            ),
            axis=-1
        )
    )


def amplitudes(array):
    return np.hypot(
        array[..., 0],
        array[..., 1]
    )


def phases(array):
    return np.arctan2(
        array[..., 1],
        array[..., 0]
    )


def corrupt_visibilities_from_f_matrix_and_phase_errors(
    visibilities,
    phase_errors,
    f_T=None,
):
    """
    The shape of \' phases \' must be (n_c, n_a, n_t) or (n_a, n_t)
    """

    def reshape_phases(a, n_b):

        # NOTE: This function assumes that the shape of a is of the form (..., n_v, 2)

        shape = (int(a.shape[-1] / n_b), n_b)

        return reshape_utils.reshape(
            a=a, axis=len(a.shape) - 1, shape=shape
        )

    def reshape_f_matrix(a, n_b, transpose=True):

        if transpose:
            return a.reshape(
                (int(a.shape[0] / n_b), n_b, -1)
            )
        else:
            raise ValueError("This has not been implemented yet.")

    def corrupt_helper_len_shape_3(visibilities, phase_errors, f_T):

        _, _, n_a = phase_errors.shape

        n_b = int(n_a * (n_a - 1) / 2.0)

        # NOTE: The shape of the array should be (n_c, n_t * n_b)
        _phases = phases(
            array=visibilities
        )

        # NOTE: This is temporary until the Visibilities class is updated.
        # NOTE: The shape of the array should be (n_c, n_t, n_b)
        phases_reshaped = reshape_phases(
            a=_phases,
            n_b=n_b
        )

        # NOTE: The shape of the "f_T" array should be (n_t * n_b, n_a)
        # NOTE: The shape of the "phase_errors" array should be (n_c, n_t, n_a)

        # NOTE: I can save memory by passing only a sloce of the f_T matrix since it is repeated...
        # NOTE: The shape of the array should be (n_t, n_b, n_a)
        f_T_reshaped = reshape_f_matrix(
            a=f_T, n_b=n_b
        )

        # NOTE: This is very time consuming ...
        phases_corrupted_reshaped = np.zeros(
            shape=phases_reshaped.shape
        )
        for i in range(phases_reshaped.shape[0]):
            for j in range(phases_reshaped.shape[1]):
                print(i, j)
                time_i = time.time()
                phases_corrupted_reshaped[i, :] = np.add(
                    phases_reshaped[i, j, :],
                    np.matmul(
                        f_T_reshaped[j, :, :], phase_errors[i, j, :]
                    )
                )
                time_j = time.time()
                print("It took t = {}".format(time_j - time_i))

        return phases_corrupted_reshaped

    def corrupt_helper_len_shape_4(visibilities, phase_errors, f_T=f_T):
        """For the specific case where the visibilities of the
        # 2 polarizations are equal.

        Parameters
        ----------
        visibilities : type
            Description of parameter `visibilities`.
        phase_errors : type
            Description of parameter `phase_errors`.

        Returns
        -------
        type
            Description of returned object.

        """

        visibilities_temp = visibilities[0, ...]

        phases_corrupted_reshaped = corrupt_helper_len_shape_3(
            visibilities=visibilities_temp, phase_errors=phase_errors, f_T=f_T
        )

        return np.stack(
            arrays=(phases_corrupted_reshaped, phases_corrupted_reshaped), axis=0
        )

    #print(visibilities.shape, phase_errors.shape, f_T.shape);exit()

    if len(visibilities.shape) == 4:
        # NOTE: visibilities are of the form (2, n_c, n_v, 2), phase_errors
        # are of the form (n_c, n_t, n_a) and f_t is of the form (n_v, n_a).

        if visibilities.shape[0] == 2:

            if phase_errors.shape[0] == visibilities.shape[1]:


                # NOTE: For the specific case where the visibilities of the
                # 2 polarizations are equal.
                # if np.array_equal(visibilities[0, ...], visibilities[1, ...]):
                #     print("THEY ARE EQUAL")
                phases_corrupted_reshaped = corrupt_helper_len_shape_4(
                    visibilities=visibilities, phase_errors=phase_errors, f_T=f_T
                )

            else:
                raise ValueError("This has not been implemented yet.")
        else:
            raise ValueError("This has not been implemented yet.")

    elif len(visibilities.shape) == 3:

        # NOTE: IN THE CASE WE AVERAGED OVER THE CHANNELS

        if phase_errors.shape[0] == visibilities.shape[0]:

            phases_corrupted_reshaped = corrupt_helper_len_shape_3(
                visibilities=visibilities, phase_errors=phase_errors, f_T=f_T
            )

        else:

            raise ValueError(
                "This is not implemented yet..."
            )

    elif len(visibilities.shape) == 2:

        if phases.shape == visibilities.shape:

            raise ValueError(
                "This is not implemented yet..."
            )

        else:

            raise ValueError(
                "This is not implemented yet..."
            )
    else:

        raise ValueError(
            "This is not implemented yet..."
        )

    phases_corrupted = phases_corrupted_reshaped.reshape(visibilities.shape[:-1])

    _amplitudes = amplitudes(array=visibilities)

    return np.stack(
        arrays=(
            np.multiply(
                _amplitudes,
                np.cos(phases_corrupted)
            ),
            np.multiply(
                _amplitudes,
                np.sin(phases_corrupted)
            )
        ),
        axis=-1
    )


def convert_phases_to_radians(phases, frequencies, phase_units=units.micron):
    # NOTE: This function assumes that the input phase errors are in units of microns.

    phases *= phase_units

    if np.shape(frequencies):

        phases_in_radians = np.zeros(
            shape=(
                (len(frequencies), ) + phases.shape
            )
        )

        for i, f in enumerate(frequencies):

            phases_in_radians[i, ...] = (phases * f / constants.c * 2.0 * np.pi * units.rad).to(units.rad).value

    else:
        raise ValueError(
            "This has not been implemented yet."
        )

    return phases_in_radians

# def corrupt_visibilities_from_antennas_and_phases(
#     visibilities,
#     antennas,
#     phases,
# ):
#     pass
