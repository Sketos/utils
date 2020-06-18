import os
import numpy as np
from astropy import constants, units as au
from astropy.io import fits



# NOTE: THIS ONLY WORKS WHEN THE NUMBER OF CHANNELS IS EVEN NUMBER.
def generate_frequencies(central_frequency, n_channels, bandwidth):

    df = (bandwidth / n_channels).to(au.Hz).value

    frequencies = np.arange(
        central_frequency.to(au.Hz).value - int(n_channels / 2.0) * df,
        central_frequency.to(au.Hz).value + int(n_channels / 2.0) * df,
        df
    )

    return frequencies


def convert_array_to_wavelengths(array, frequency):

    array_converted = (
        (array * au.m) * (frequency * au.Hz) / constants.c
    ).decompose()

    return array_converted.value




def convert_uv_coords_from_meters_to_wavelengths(uv, frequencies):

    if np.shape(frequencies):

        u_wavelengths, v_wavelengths = np.zeros(
            shape=(
                2,
                len(frequencies),
                uv.shape[1]
            )
        )

        for i in range(len(frequencies)):
            u_wavelengths[i, :] = convert_array_to_wavelengths(array=uv[0, :], frequency=frequencies[i])
            v_wavelengths[i, :] = convert_array_to_wavelengths(array=uv[1, :], frequency=frequencies[i])

    else:

        u_wavelengths = convert_array_to_wavelengths(array=uv[0, :], frequency=frequencies)
        v_wavelengths = convert_array_to_wavelengths(array=uv[1, :], frequency=frequencies)

    return np.stack(
        arrays=(u_wavelengths, v_wavelengths),
        axis=-1
    )
# --------------------------------------------------------------------------- #

def load_configuration_file(filename):

    if filename.endswith(".cfg"):

        if os.path.isfile(filename):
            x, y, z = np.loadtxt(
                filename,
                usecols=(0, 1, 2),
                unpack=True
            )
        else:
            raise IOError(
                "The file {} does not exist".format(filename)
            )

    else:
        raise ValueError(
            "The input filename is not a .cfg file"
        )

    return np.array([x, y, z])





def compute_number_of_baselines_from_number_of_antennas(number_of_antennas):

    number_of_baselines = int(
        number_of_antennas * (number_of_antennas - 1.0) / 2.0
    )

    return number_of_baselines


def compute_baselines(x, y, z, number_of_antennas):
    if len(x) != number_of_antennas or len(y) != number_of_antennas or len(z) != number_of_antennas:
        raise ValueError

    number_of_baselines = compute_number_of_baselines_from_number_of_antennas(
        number_of_antennas=number_of_antennas
    )

    baselines = np.zeros(
        shape=(number_of_baselines)
    )

    n = 0
    for i in np.arange(0, number_of_antennas):
        for j in np.arange(i + 1, number_of_antennas):
            baselines[n] = np.sqrt((x[i] - x[j])**2.0 + (y[i] - y[j])**2.0 + (z[i] - z[j])**2.0)
            n += 1

    return baselines


def compute_baselines_from_configuration_file(filename):

    antenna_positions = load_configuration_file(
        filename=filename
    )

    baselines = compute_baselines(
        x=antenna_positions[0, :],
        y=antenna_positions[1, :],
        z=antenna_positions[2, :],
        number_of_antennas=antenna_positions.shape[-1]
    )

    return baselines


def uvcontsub(visibilities, antennas, baseline_lengths):

    antenna1, antenna2 = antennas
    antenna1_unique = np.unique(antenna1)
    antenna2_unique = np.unique(antenna2)

    visibilities_uvcontsub = np.zeros(
        shape=visibilities.shape
    )

    for ant1 in antenna1_unique:
        for ant2 in antenna2_unique:
            if ant1 < ant2:
                idx = np.logical_and(
                    antenna1==ant1,
                    antenna2==ant2
                )

                # baseline_length = baseline_lengths[
                #     "{}-{}".format(
                #         antenna_names[ant1],
                #         antenna_names[ant2]
                #     )
                # ]
                # x_temp_plot.append(baseline_length)

                x_temp = np.tile(x, (np.sum(idx), 1)).T


                y_real = visibilities[:, idx, 0]
                y_imag = visibilities[:, idx, 1]
                polyfit_parameters_y_real = np.polyfit(
                    np.ndarray.flatten(x_temp[x_idx, :]),
                    np.ndarray.flatten(y_real[x_idx, :]),
                    0
                )
                polyfit_parameters_y_imag = np.polyfit(
                    np.ndarray.flatten(x_temp[x_idx, :]),
                    np.ndarray.flatten(y_imag[x_idx, :]),
                    0
                )

                y_real_temp_plot.append(polyfit_parameters_y_real[0])
                y_imag_temp_plot.append(polyfit_parameters_y_imag[0])

                poly1d_y_real = np.poly1d(polyfit_parameters_y_real)
                poly1d_y_imag = np.poly1d(polyfit_parameters_y_imag)
                #print(polyfit_parameters_y_real);exit()

                visibilities_uvcontsub[:, idx, 0] = y_real - np.array([poly1d_y_real(x), ] * np.sum(idx)).T
                visibilities_uvcontsub[:, idx, 1] = y_imag - np.array([poly1d_y_imag(x), ] * np.sum(idx)).T


if __name__ == "__main__":

    directory = "/Users/ccbh87/Desktop/GitHub/simobserve"
    filename = "alma.cycle5.6.cfg"
    #filename = "/Users/ccbh87/Desktop/GitHub/simobserve/alma.cycle5.8.cfg"
    #baselines = compute_baselines_from_configuration_file(filename=filename)
    #print(np.max(baselines))

    x, y, z = load_configuration_file(
        filename="{}/{}".format(directory, filename)
    )

    #R = np.zeros(shape=coords.shape[-1])
    R = x**2.0 + y**2.0 + z**2.0

    import string_utils as string_utils

    fits.writeto(
        filename="{}/{}_distances.fits".format(
            directory,
            string_utils.remove_substring_from_end_of_string(
                string=filename,
                substring=".cfg"
            )
        ),
        data=R,
        overwrite=True
    )
