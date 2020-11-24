import numpy as np
from astropy import constants
from astropy import units as au

import matplotlib.pyplot as plt

from dictionary_utils import *


"""
READE:

i) The moment functions have been tested against the equivalent
functions in the spectral_cube package and the results are the same.


INSTRUCTIONS:

i)

"""

def convert_wavelength_to_frequency(wavelength, units=au.GHz):

    # NOTE: Check that wavelength has units.

    return (constants.c / wavelength).to(units)


def convert_frequencies_to_velocities(frequencies, frequency_0, units=au.km / au.s):
    """

    NOTE: This has been cross-validated against the spectral_cube package

    Parameters
    ----------

    frequencies: [GHz]

    frequency_0: [GHz]

    """

    # TODO: check that frequencies have units and it is actually Hz.

    velocities = constants.c * (1.0 - frequencies / frequency_0)

    return (velocities).to(units).value


def convert_frequency_to_velocity_resolution(frequency_resolution, frequency_0, units=au.km / au.s):
    """

    Parameters
    ----------

    frequency_resolution: [GHz]

    frequency_0: [GHz]

    units: - default [km/s]

    """
    return (constants.c * frequency_resolution / frequency_0).to(units).value


def observed_line_frequency_from_rest_line_frequency(frequency, redshift):
    """

    Parameters
    ----------

    frequency: [GHz]

    redshift:

    """

    return frequency / (redshift + 1.0)


#CII = 1900.537


def observed_C_frequencies(redshift):

    transition_frequencies = {
        "1-0": 492.1607,
        "2-1": 809.3435,
    }

    for transition, frequency in transition_frequencies.items():
        observed_transition_frequency = observed_line_frequency_from_rest_line_frequency(
            frequency=frequency,
            redshift=redshift
        )

        print(
            "For C = {} at z={} the observed frequency is f={} (GHz)".format(
                transition,
                redshift,
                observed_transition_frequency
            )
        )

def observed_H2O_frequencies(redshift):

    transition_frequencies = {
        "1_11-0_00": 1113.343,
        "2_02-1_11": 987.927,
        "2_11-2_02": 752.033,
        "2_20-2_11": 1228.789,
        "3_12-3_03": 1097.365,
        "3_21-3_12": 1162.912,
        "4_22-4_13": 1207.639,
        "5_23-5_12": 1410.618,
    }

    for transition, frequency in transition_frequencies.items():
        observed_transition_frequency = observed_line_frequency_from_rest_line_frequency(
            frequency=frequency,
            redshift=redshift
        )

        print(
            "For H20 = {} at z={} the observed frequency is f={} (GHz)".format(
                transition,
                redshift,
                observed_transition_frequency
            )
        )


def rest_frame_CO_frequencies(transition):

    transition_frequencies = {
        "1-0": 115.271,
        "2-1": 230.538,
        "3-2": 345.796,
        "4-3": 461.041,
        "5-4": 576.268,
        "6-5": 691.473,
        "7-6": 806.652,
        "8-7": 921.800,
        "9-8": 1036.912,
    }

    if transition in transition_frequencies.keys():
        return transition_frequencies[transition]
    else:
        raise ValueError(
            "The transition J={} is not supported".format(transition)
        )

def observed_CO_frequencies(redshift):

    transition_frequencies = {
        "1-0": 115.271,
        "2-1": 230.538,
        "3-2": 345.796,
        "4-3": 461.041,
        "5-4": 576.268,
        "6-5": 691.473,
        "7-6": 806.652,
        "8-7": 921.800,
        "9-8": 1036.912,
    }

    for transition, frequency in transition_frequencies.items():
        observed_transition_frequency = observed_line_frequency_from_rest_line_frequency(
            frequency=frequency,
            redshift=redshift
        )

        print(
            "For J = {} at z={} the observed frequency is f={} (GHz)".format(
                transition,
                redshift,
                observed_transition_frequency
            )
        )

def observed_CO_frequency(redshift, transition="1-0"):

    transitions = {
        "1-0": 115.271,
        "2-1": 230.538,
        "3-2": 345.796,
        "4-3": 461.041,
        "5-4": 576.268,
        "6-5": 691.473,
        "7-6": 806.652,
        "8-7": 921.800,
        "9-8": 1036.912,
    }

    if transition in transitions:
        frequency = transitions[transition]
    else:
        raise ValueError(
            "The CO J = {} transition in not valid".format(transition)
        )

    observed_transition_frequency = observed_line_frequency_from_rest_line_frequency(
        frequency=frequency,
        redshift=redshift
    )

def rest_line_frequency_from_observed_line_frequency(frequency, redshift):
    """

    Parameters
    ----------

    frequency: [GHz]

    redshift:

    """

    return frequency * (redshift + 1.0)


def get_spectrum_from_cube(cube):

    y = np.zeros(
        shape=(cube.shape[0],)
    )
    for i in range(len(y)):
        y[i] = np.nansum(cube[i, :, :])

    return y


def get_line_flux_from_spectrum(y, dv):

    line_flux = np.nansum(y) * dv

    return line_flux


def get_line_flux_from_cube(cube, dv):

    y = get_spectrum_from_cube(
        cube=cube
    )

    line_flux = np.sum(y) * dv

    return line_flux


def compute_line_instensity_from_line_flux():
    pass


def rotation_curve(cube, x, y, velocities):

    #print(velocities.shape, cube.shape);exit()

    y_temp = []
    for i, (x_i, y_i) in enumerate(zip(x, y)):

        i = int(x_i)
        j = int(y_i)

        cube[j, i] = np.nan

    #     spectrum = cube[:, j, i]
    #     #print(i)
    #     #if i == 0:
    #     #plt.plot(velocities, np.abs(spectrum))
    #     y_temp.append(
    #         np.average(velocities, weights=np.abs(cube[:, j, i]))
    #     )
    #
    # plt.plot(y_temp)
    # plt.show()



    exit()


# NOTE: https://www.atnf.csiro.au/computing/software/miriad/userguide/node158.html
def moment_0(cube, velocities, f_min=None, axis=0):

    if f_min is not None:
        cube[np.where(cube < f_min)] = 0.0

    if cube.shape[0] != len(velocities):
        raise ValueError(
            "The # of channels in the cube n_c={} is not equal to the # of elements n_v={} in the velocity array".format(
                cube.shape[0], len(velocities)
            )
        )

    # NOTE: exclude pixels
    # NOTE: exclude channels

    integral = np.trapz(
        y=cube,
        dx=np.abs(velocities[1] - velocities[0]),
        axis=axis
    )

    return integral





def moment_1(cube, velocities, f_min=None, axis=0):

    if f_min is not None:
        cube[np.where(cube < f_min)] = 0.0

    _moment_0 = moment_0(
        cube=cube,
        velocities=velocities,
        axis=axis
    )

    if axis is None:
        raise ValueError("...")
    elif axis == 0:
        y = cube * velocities[:, None, None]
    elif axis == 2:
        y = cube * velocities[None, None, :]
    else:
        raise ValueError("ARE YOU SURE?")

    integral = np.trapz(
        y=y,
        dx=np.abs(velocities[1] - velocities[0]),
        axis=axis
    )

    _moment_1 = integral / _moment_0

    return _moment_1


def moment_2(cube, velocities, f_min=None, axis=0):

    if f_min is not None:
        cube[np.where(cube < f_min)] = 0.0

    m_0 = moment_0(
        cube=cube,
        velocities=velocities,
        axis=axis
    )

    m_1 = moment_1(
        cube=cube,
        velocities=velocities,
        axis=axis
    )

    if axis is None:
        raise ValueError("...")
    elif axis == 0:
        y = cube * (velocities[:, None, None] - m_1)**2.0
    elif axis == 2:
        y = cube * (velocities[None, None, :] - m_1)**2.0
    else:
        raise ValueError("ARE YOU SURE?")


    integral = np.trapz(
        y=y,
        dx=np.abs(velocities[1] - velocities[0]),
        axis=axis
    )

    m_2 = integral / m_0

    return m_2

# def compute_moment_0(ndarray, velocities, axis=0):
#
#     if ndarray.shape[0] != len(velocities):
#         raise ValueError
#
#     # NOTE: exclude pixels
#     # NOTE: exclude channels
#
#     integral = np.trapz(
#         y=ndarray,
#         x=velocities,
#         axis=axis
#     )
#
#     return integral
#
#
# def compute_moment_1(ndarray, velocities, axis=0):
#
#     moment_0 = compute_moment_0(
#         ndarray=ndarray,
#         velocities=velocities,
#         axis=axis
#     )
#
#     if axis is None:
#         raise ValueError
#     elif axis == 0:
#         y = np.multiply(
#             ndarray,
#             velocities.reshape(
#                 [velocities.size,] + list(np.ones(shape=len(ndarray.shape[1:]), dtype=int))
#             )
#         )
#     else:
#         raise ValueError("...")
#
#     integral = np.trapz(
#         y=y, x=velocities, axis=axis
#     )
#
#     return integral / moment_0


def Reuter_et_al_2020():

    wavelengths = [
        3000,
        2000,
        1400,
        870,
        500,
        350,
        250,
        160,
        100
    ]

    for wavelength in wavelengths:
        frequency = convert_wavelength_to_frequency(
            wavelength=wavelength * au.micron, units=au.GHz
        )

        print(
            "The frequency corresponding to a wavelength of {} is {}".format(wavelength, frequency)
        )


def compute_z_step_kms(frequencies, frequency_0=None):

    if frequency_0 is None:

        frequency_0 = np.mean(
            a=frequencies,
            axis=0
        )

    frequency_resolution = np.divide(
        np.subtract(
            frequencies[-1], frequencies[0]
        ),
        len(frequencies) - 1
    )

    return convert_frequency_to_velocity_resolution(
        frequency_resolution=frequency_resolution,
        frequency_0=frequency_0,
    )



if __name__ == "__main__":
    pass

    # Reuter_et_al_2020()
    # exit()

    source_redshifts = {
        "ALESS6.1":2.3338,
        "ALESS41.1":2.5460,
        "ALESS49.1":2.9417,
        "ALESS75.1":2.5450,
        "ALESS65.1":4.4445,
        "ALESS66.1":2.5542,
        "ALESS34.1":2.5115,
        "ALESS17.1":1.5397,
        "ALESS88.1":1.2679,
        "ALESS101.1":2.7999,
        "ALESS71.1":3.7072348210731896,
        "ALESS61.1":4.404619745761362,
        "ALESS98.1":1.3739182340970815,
        "ALESS31.1":3.7123788087268546,
        "ALESS35.1":2.973724833177655,
        "ALESS101.1":2.353081402886241,
        "J142413":4.243,
        "SDP.81":3.042,
        "ALESS035.1":2.9737,

    }

    #source = "ALESS41.1"
    # source = "ALESS49.1"
    # source = "ALESS75.1"
    # source = "ALESS65.1"
    # source = "ALESS34.1"
    # source = "ALESS17.1"
    # source = "ALESS88.1"
    # source = "ALESS66.1"
    # source = "ALESS101.1"
    # source = "ALESS6.1"
    #source = "ALESS71.1"
    #source = "ALESS61.1"
    #source = "ALESS98.1"
    #source = "ALESS31.1"
    #source = "ALESS101.1"
    #source = "ALESS35.1"
    #source = "J142413"
    #source = "SDP.81"
    source = "ALESS035.1"

    observed_CO_frequencies(
        redshift=source_redshifts[source]
    )

    observed_H2O_frequencies(
        redshift=source_redshifts[source]
    )

    observed_C_frequencies(
        redshift=source_redshifts[source]
    )

    # frequency = observed_CO_frequency(
    #     redshift=source_redshifts[source], transition="3-2"
    # )



    # molecular_lines = {
    #     "CII":{"restfreq":1900.536900}
    # }
    #
    # molecular_lines["CII"]["restfreq"]
    #
    # redshift = 3.042
    #
    #
    #
    # obsfreq = observed_line_frequency_from_rest_line_frequency(
    #     frequency=get_output_from_nested_dictionary(
    #         molecular_lines,
    #         "CII",
    #         "restfreq"
    #     ),
    #     redshift=redshift
    # )
    #
    # print(obsfreq)
