import os
import numpy as np
from astropy.io import fits


def load_data_from_filename(filename):

    if os.path.isfile(filename):
        data = fits.getdata(filename=filename)
    else:
        raise IOError(
            "{} does not exist".format(filename)
        )

    return data


def load_visibilities_from_fits(filename, stacked=False, stacked_axis=-1):

    data = load_data_from_filename(
        filename=filename
    )

    # NOTE: The shape of the data array is (2, n_channels, n_visibilities), where n_visibilities is ...
    if len(data.shape) == 3:
        # NOTE:
        if data.shape[-1] == 1:
            raise ValueError
        elif data.shape[-1] == 2:
            real_visibilities, imag_visibilities = data
        elif data.shape[-1] == 3:
            raise ValueError
        else:
            raise ValueError
    else:
        raise ValueError

    # NOTE:
    if stacked:
        return np.stack(
            arrays=(real_visibilities, imag_visibilities), axis=-1
        )
    return np.array(
        object=[real_visibilities, imag_visibilities]
    )


def load_uv_wavelengths_from_fits(filename, stacked=False, stacked_axis=-1):

    data = load_data_from_filename(
        filename=filename
    )

    # NOTE: The shape of the data array is (3, n_channels, n_visibilities), where n_visibilities is ...
    if len(data.shape) == 3:
        # NOTE:
        if data.shape[0] == 1:
            raise ValueError
        elif data.shape[0] == 2:
            u_wavelengths, v_wavelengths = data
        elif data.shape[0] == 3:
            u_wavelengths, v_wavelengths, w_wavelengths = data
        else:
            raise ValueError
    else:
        raise ValueError

    # NOTE: ...
    if stacked:
        return np.stack(
            arrays=(u_wavelengths, v_wavelengths), axis=-1
        )
    return np.array(
        object=[u_wavelengths, v_wavelengths]
    )
