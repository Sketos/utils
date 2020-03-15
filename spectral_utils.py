from astropy import constants
from astropy import units as au


def convert_frequencies_to_velocities(frequencies, frequency_0):
    """

    Parameters
    ----------

    frequencies: [GHz]

    frequency_0: [GHz]

    """

    # TODO: check that frequencies have units and it is actually Hz.

    velocities = constants.c * (1.0 - frequencies / frequency_0)


def convert_frequency_to_velocity_resolution(frequency_resolution, frequency_0, units=au.km/au.s):
    """

    Parameters
    ----------

    frequency_resolution: [GHz]

    frequency_0: [GHz]

    units: - default [km/s]

    """
    return (constants.c * frequency_resolution / frequency_0).to(units)


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
