import numpy as np

from astropy import units
from astropy import constants



def convert_array_in_units_of_meters_to_units_of_wavelengths(array_meters, frequency):

    return (array_meters * frequency.to(units.Hz) / constants.c.to(units.m/units.s)).decompose()


def compute_uv_wavelengths(u_meters, v_meters, frequency):

    # u_wavelengths = convert_array_in_units_of_meters_to_units_of_wavelengths(
    #     array_meters=u_meters, frequency=frequency
    # )
    # v_wavelengths = convert_array_in_units_of_meters_to_units_of_wavelengths(
    #     array_meters=v_meters, frequency=frequency
    # )

    u_wavelengths = u_meters * frequency * units.GHz.to(units.Hz) / constants.c.to(units.m/units.s).value
    v_wavelengths = v_meters * frequency * units.GHz.to(units.Hz) / constants.c.to(units.m/units.s).value

    return u_wavelengths, v_wavelengths


def rms(visibilities):

    if len(visibilities.shape) == 3:
        N = visibilities.shape[0]
    else:
        raise ValueError("Not implemented yet...")

    rms_real = np.zeros(shape=(N, ))
    rms_imag = np.zeros(shape=(N, ))
    for i in range(N):
        rms_real[i] = np.sqrt(
            np.mean(
                np.square(visibilities[i, :, 0])
            )
        )
        rms_imag[i] = np.sqrt(
            np.mean(
                np.square(visibilities[i, :, 1])
            )
        )

    return rms_real, rms_imag


if __name__ == "__main__":

    array = convert_array_in_units_of_meters_to_units_of_wavelengths(
        array_meters=[0.0, 1.0, 2.0] * units.m, frequency=230 * units.GHz
    )
    print(array)
