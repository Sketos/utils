import os
import numpy as np
from astropy import units as au


# NOTE: THIS ONLY WORKS WHEN THE NUMBER OF CHANNELS IS EVEN NUMBER.
def generate_frequencies(central_frequency, n_channels, bandwidth):

    df = (bandwidth / n_channels).to(au.Hz).value

    frequencies = np.arange(
        central_frequency.to(au.Hz).value - int(n_channels / 2.0) * df,
        central_frequency.to(au.Hz).value + int(n_channels / 2.0) * df,
        df
    )

    return frequencies


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
            raise IOError("...")

    else:
        raise ValueError(
            "The input filename is not a .cfg file"
        )

    return x, y, z


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
