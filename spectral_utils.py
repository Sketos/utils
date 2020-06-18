import numpy as np
from astropy import constants
from astropy import units as au

from dictionary_utils import *


def convert_frequencies_to_velocities(frequencies, frequency_0, units=au.km / au.s):
    """

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


# NOTE: https://www.atnf.csiro.au/computing/software/miriad/userguide/node158.html
def moment_0(cube, velocities, axis=0):

    if cube.shape[0] != len(velocities):
        raise ValueError

    # NOTE: exclude pixels
    # NOTE: exclude channels

    integral = np.trapz(
        y=cube, x=velocities, axis=axis
    )

    return integral





def moment_1(cube, velocities, axis=0):

    _moment_0 = moment_0(
        cube=cube,
        velocities=velocities,
        axis=axis
    )

    if axis is None:
        raise ValueError
    elif axis == 0:
        y = cube * velocities[:, None, None]
    elif axis == 2:
        y = cube * velocities[None, None, :]
    else:
        raise ValueError

    integral = np.trapz(
        y=y, x=velocities, axis=axis
    )

    _moment_1 = integral / _moment_0

    return _moment_1




def compute_moment_0(ndarray, velocities, axis=0):

    if ndarray.shape[0] != len(velocities):
        raise ValueError

    # NOTE: exclude pixels
    # NOTE: exclude channels

    integral = np.trapz(
        y=ndarray,
        x=velocities,
        axis=axis
    )

    return integral


def compute_moment_1(ndarray, velocities, axis=0):

    moment_0 = compute_moment_0(
        ndarray=ndarray,
        velocities=velocities,
        axis=axis
    )

    if axis is None:
        raise ValueError
    elif axis == 0:
        y = np.multiply(
            ndarray,
            velocities.reshape(
                [velocities.size,] + list(np.ones(shape=len(ndarray.shape[1:]), dtype=int))
            )
        )
    else:
        raise ValueError("...")

    integral = np.trapz(
        y=y, x=velocities, axis=axis
    )

    return integral / moment_0

if __name__ == "__main__":





    molecular_lines = {
        "CII":{"restfreq":1900.536900}
    }

    molecular_lines["CII"]["restfreq"]

    redshift = 4.342



    obsfreq = observed_line_frequency_from_rest_line_frequency(
        frequency=get_output_from_nested_dictionary(
            molecular_lines,
            "CII",
            "restfreq"
        ),
        redshift=redshift
    )

    print(obsfreq)
