import os, sys, copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from astropy import (
    units as au,
    constants
)
from astropy.io import fits
from scipy import (
    ndimage,
    interpolate,
    stats
)

# ---------- #
# NOTE: custom packages
# ---------- #
from dictionary_utils import *
import fitting_utils as fitting_utils
import fits_utils as fits_utils
import mask_utils as mask_utils
import matplotlib_utils as matplotlib_utils
import plot_utils as plot_utils
import spectral_plot_utils as spectral_plot_utils
import spectral_utils as spectral_utils
# ---------- #

"""
READE:

i) The moment functions have been tested against the equivalent
functions in the spectral_cube package and the results are the same.


INSTRUCTIONS:

i)

"""



# NOTE:
CII_line_rest_frequency = 1900.536900

# NOTE:
def observed_line_frequency_from_rest_line_frequency(frequency, redshift):
    """

    Parameters
    ----------

    frequency: [GHz]

    redshift:

    """
    return frequency / (redshift + 1.0)

# NOTE:
def observed_line_wavelength_from_rest_line_wavelength(wavelength, redshift):
    """

    Parameters
    ----------

    frequency: [GHz]

    redshift:

    """
    return wavelength * (redshift + 1.0)

# NOTE:
def rest_line_frequency_from_observed_line_frequency(frequency, redshift):
    """

    Parameters
    ----------

    frequency: [GHz]

    redshift:

    """
    return frequency * (redshift + 1.0)

# NOTE:
def rest_line_wavelength_from_observed_line_wavelength(wavelength, redshift):
    """

    Parameters
    ----------

    frequency: [GHz]

    redshift:

    """
    return wavelength / (redshift + 1.0)

# NOTE:
def CII_observed_line_frequency_from_redshift(
    redshift
):
    return observed_line_frequency_from_rest_line_frequency(
        frequency=1900.536900,
        redshift=redshift
    )

# NOTE:
def z_mask_from_zmin_and_zmax(shape, zmin, zmax, invert=False):

    # NOTE:
    mask = np.full(
        shape=shape,
        fill_value=False
    )

    # NOTE:
    mask[:zmin] = True
    mask[zmax:] = True

    # NOTE:
    if invert:
        raise NotImplementedError()

    return mask

# NOTE: check that 'frequencies' and 'frequency_0' have the same units.
def convert_frequencies_to_velocities(
    frequencies, frequency_0, units=au.km / au.s
):
    """

    NOTE: This has been cross-validated against the spectral_cube package and CASA

    Parameters
    ----------

    frequencies: [GHz]

    frequency_0: [GHz]

    """
    velocities = constants.c * (1.0 - frequencies / frequency_0)

    return (velocities).to(units).value

# NOTE:
def get_velocities_from_header(header, frequency_0=None):

    # if "RESTFRQ" is header.keys():
    #     pass
    # else:
    #     raise ValueError()

    # NOTE:
    frequencies = fits_utils.get_frequencies_from_header(header=header)

    # NOTE:
    if frequency_0 is None:
        try:
            frequency_0 = header["RESTFRQ"] * au.Hz
        except:
            raise NotImplementedError()

    # NOTE:
    velocities = convert_frequencies_to_velocities(
        frequencies=frequencies.to(au.Hz), frequency_0=frequency_0.to(au.Hz)
    )

    return velocities


def get_velocities_from_fits(filename, frequency_0=None):

    header = fits.getheader(filename=filename)

    return get_velocities_from_header(
        header=header, frequency_0=frequency_0
    )



# NOTE: Check that wavelength has units.
def convert_wavelengths_to_frequencies(wavelengths, units=au.GHz):
    return (constants.c / wavelengths).to(units)





def convert_frequency_difference_to_velocity_difference(
    frequency_i,
    frequency_j,
    units=au.km / au.s
):

    velocity = constants.c * (1.0 - frequency_i / frequency_j)

    return (velocity).to(units).value

def convert_wavelength_difference_to_velocity_difference(
    wavelength_i,
    wavelength_j,
    units=au.km / au.s
):

    velocity = constants.c * (1.0 - wavelength_i / wavelength_j)

    return (velocity).to(units).value

def convert_wavelengths_to_velocities(
    wavelengths, wavelength_0, units=au.km / au.s
):
    """

    Parameters
    ----------

    wavelengths: [GHz]

    wavelength_0: [GHz]

    """

    frequencies = spectral_utils.convert_wavelengths_to_frequencies(
        wavelengths=wavelengths, units=au.GHz
    )
    frequency_0 = spectral_utils.convert_wavelengths_to_frequencies(
        wavelengths=wavelength_0, units=au.GHz
    )
    return spectral_utils.convert_frequencies_to_velocities(
        frequencies=frequencies, frequency_0=frequency_0
    )

    # NOTE: THIS IS WRONG
    """
    velocities = constants.c * (1.0 - wavelengths / wavelength_0)

    return (velocities).to(units).value
    """

def convert_frequency_to_velocity_resolution(frequency_resolution, frequency_0, units=au.km / au.s):
    """

    Parameters
    ----------

    frequency_resolution: [GHz]

    frequency_0: [GHz]

    units: - default [km/s]

    """
    return (constants.c * frequency_resolution / frequency_0).to(units).value


def convert_wavelength_to_velocity_resolution(wavelength_resolution, wavelength_0, units=au.km / au.s):

    return (constants.c * wavelength_resolution / wavelength_0).to(units).value











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

def observed_frame_CO_frequencies(transition, redshift):

    frequency = rest_frame_CO_frequencies(
        transition=transition
    )

    return observed_line_frequency_from_rest_line_frequency(
        frequency=frequency,
        redshift=redshift
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

    return observed_transition_frequency



# NOTE:
def get_spectrum_from_cube(cube):

    y = np.zeros(
        shape=(cube.shape[0],)
    )
    for i in range(len(y)):
        y[i] = np.nansum(cube[i, :, :])

    return y

# NOTE:
def spectrum_from_cube_and_mask(cube, mask=None, invert=False):

    cube_copy = copy.deepcopy(cube)

    # NOTE:
    spectrum = np.zeros(shape=cube_copy.shape[0])

    # # NOTE:
    # figure, axes = plot_utils.plot_cube(cube=cube, ncols=10)
    # # for ax in np.ndarray.flatten(axes):
    # #     ax.set_xlim(205, 305)
    # #     ax.set_ylim(200, 300)
    # plt.show()
    # exit()

    # NOTE:
    for i in range(cube_copy.shape[0]):

        slice_masked = cube_copy[i, ...]

        if mask is not None:
            if invert:
                slice_masked[~mask] = np.nan
            else:
                slice_masked[mask] = np.nan

        # # NOTE:
        # plt.figure()
        # plt.imshow(slice_masked)
        # plt.show()

        spectrum[i] = np.nansum(slice_masked)

    # plt.figure()
    # plt.plot(spectrum)
    # plt.show()
    # exit()

    return spectrum


def get_line_flux_from_spectrum(y, dv):

    line_flux = np.nansum(y) * dv

    return line_flux


def get_line_flux_from_cube(cube, dv):

    y = get_spectrum_from_cube(
        cube=cube
    )

    line_flux = np.sum(y) * dv

    return line_flux







def moments_with_spectral_fitting_and_binning(
    cube,
    velocities,
    bins=[2, 3, 4, 5],
    p0_0=100.0,
    SNR_min=5.0,
    mask=None,
    show=True,
    debug=False
):

    def chi_squared_from(y, y_model, sigma):

        return np.sum(
            (y - y_model)**2.0 / sigma**2.0
        )

    shape = cube.shape

    if mask is None:
        mask = np.ones(shape=shape[1:], dtype=bool)

    moment_0 = np.zeros(shape=shape[1:])
    moment_1 = np.zeros(shape=shape[1:])
    moment_2 = np.zeros(shape=shape[1:])

    SNR_from = np.zeros(shape=shape[1:])

    for i in range(shape[1]):
        for j in range(shape[2]):
            print(i, j)

            y = cube[:, i, j]

            if mask[i, j]:

                condition = False
                for n, bin in enumerate(bins):
                    if condition:
                        break

                    print("n =", n)

                    i_min = i - bin
                    i_max = i + bin
                    j_min = j - bin
                    j_max = j + bin

                    if i_min <= 0:
                        i_min = 0
                    if i_max > shape[1]:
                        i_max = shape[1]
                    if j_min <= 0:
                        j_min = 0
                    if j_max >= shape[2]:
                        j_max = shape[2]

                    y_with_binning = np.zeros(shape[0])
                    for i_n in range(i_min, i_max):
                        for j_n in range(j_min, j_max):
                            y_with_binning += cube[:, i_n, j_n]
                    y_with_binning /= ((i_min - i_max) * (j_min - j_max))


                    if np.nansum(y_with_binning) != 0:

                        #median = np.median(spectrum)

                        sigma = np.multiply(
                            np.std(y_with_binning), np.ones(shape=y_with_binning.shape)
                        )

                        # plt.figure()
                        # plt.plot(
                        #     velocities,
                        #     y_with_binning
                        # )
                        # plt.show()

                        try:
                            p, _ = fitting_utils.fit_gaussian(
                                x=velocities,
                                y=y_with_binning,
                                p0=(p0_0, velocities[np.argmax(y_with_binning)], 50.0),
                                sigma=sigma
                            )
                        except:
                            p = None


                        # if i == int(shape[1] / 2.0) and j == int(shape[2] / 2.0):
                        #     plt.figure()
                        #     plt.plot(
                        #         velocities,
                        #         y,
                        #         marker="o"
                        #     )
                        #     plt.plot(
                        #         velocities,
                        #         y_with_binning,
                        #         marker="o"
                        #     )
                        #     plt.plot(
                        #         velocities,
                        #         fitting_utils.gaussian(velocities, *p),
                        #         color="black"
                        #     )
                        #     plt.show()
                        #     exit()

                        chi_squared = chi_squared_from(
                            y=y_with_binning,
                            y_model=np.zeros(shape=y_with_binning.shape),
                            sigma=sigma
                        )

                        if p is None:
                            chi_squared_from_gaussian = np.inf
                        else:
                            chi_squared_from_gaussian = chi_squared_from(
                                y=y_with_binning,
                                y_model=fitting_utils.gaussian(velocities, *p),
                                sigma=sigma
                            )


                        SNR = (chi_squared - chi_squared_from_gaussian)**0.5
                        SNR_from[i, j] = SNR

                        #print("HERE", SNR, chi_squared, chi_squared_from_gaussian, p)

                        if SNR > SNR_min and p is not None:
                            print("bin =", bin)
                            condition = True

                            moment_0[i, j] = p[0]
                            moment_1[i, j] = p[1]
                            moment_2[i, j] = p[2]

                            """
                            plt.figure()
                            # plt.plot(
                            #     velocities,
                            #     y,
                            #     marker="o"
                            # )
                            plt.plot(
                                velocities,
                                y_with_binning,
                                marker="o"
                            )
                            plt.plot(
                                velocities,
                                fitting_utils.gaussian(velocities, *p),
                                color="black"
                            )
                            plt.show()
                            #exit()
                            """
    if debug:

        plt.figure()
        plt.imshow(SNR_from, cmap="jet")
        plt.colorbar()

    return moment_0, moment_1, moment_2







# NOTE: https://www.atnf.csiro.au/computing/software/miriad/userguide/node158.html
def moment_0(cube, velocities, f_min=None, axis=0):

    cube = copy.copy(cube)

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

def moment_0_from_cube_and_mask(
    cube: np.ndarray,
    velocities: np.ndarray,
    mask=None,
    axis=0
):

    cube_copy = copy.copy(cube)

    if mask is not None:
        cube_copy[mask] = 0.0

    return np.trapz(
        y=cube_copy,
        dx=np.abs(velocities[1] - velocities[0]),
        axis=axis
    )




def moment_0_from_cube(cube, dx, f_min=None, axis=0):

    if f_min is not None:
        cube[np.where(cube < f_min)] = 0.0



    # NOTE: exclude pixels
    # NOTE: exclude channels

    integral = np.trapz(
        y=cube,
        dx=dx,
        axis=axis
    )

    return integral




def moment_1_from_cube_and_mask(
    cube,
    velocities,
    mask=None,
    axis=0
):

    cube_copy = copy.copy(cube)

    if mask is not None:
        cube_copy[mask] = 0.0

    shape = cube.shape

    _moment_0 = moment_0_from_cube_and_mask(
        cube=cube_copy,
        velocities=velocities,
        mask=mask,
        axis=axis
    )


    if axis is None:
        raise ValueError("...")
    elif axis == 0:
        if len(shape) == 2:
            y = cube_copy * velocities[:, None]
        elif len(shape) == 3:
            y = cube_copy * velocities[:, None, None]
        else:
            raise ValueError("This has not been implemented before")
    elif axis == 2:
        y = cube_copy * velocities[None, None, :]
    else:
        raise ValueError("ARE YOU SURE?")

    integral = np.trapz(
        y=y,
        dx=np.abs(velocities[1] - velocities[0]),
        axis=axis
    )

    _moment_1 = integral / _moment_0

    return _moment_1


def moment_1(
    cube,
    velocities,
    f_min=None,
    axis=0,
    figure_1_for_debugging=False
):

    cube = copy.copy(cube)

    if f_min is not None:
        cube[np.where(cube < f_min)] = 0.0

    if figure_1_for_debugging:
        plt.figure()
        plot_utils.plot_cube(cube, ncols=12)
        plt.show()


    shape = cube.shape

    _moment_0 = moment_0(
        cube=cube,
        velocities=velocities,
        axis=axis
    )


    if axis is None:
        raise ValueError("...")
    elif axis == 0:
        if len(shape) == 2:
            y = cube * velocities[:, None]
        elif len(shape) == 3:
            y = cube * velocities[:, None, None]
        else:
            raise ValueError("This has not been implemented before")
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


def moment_2(
    cube,
    velocities,
    f_min=None,
    axis=0
):

    cube = copy.copy(cube)

    if f_min is not None:
        cube[np.where(cube < f_min)] = 0.0

    shape = cube.shape

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
        if len(shape) == 2:
            y = cube * (velocities[:, None] - m_1)**2.0
        if len(shape) == 3:
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

    m_2 = np.sqrt(integral / m_0)

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
        frequency = convert_wavelengths_to_frequencies(
            wavelengths=wavelength * au.micron, units=au.GHz
        )

        print(
            "The frequency corresponding to a wavelength of {} is {}".format(wavelength, frequency)
        )

# NOTE: \'z_step_kms\' is needed to produce kinematical models (e.g. rotating disk).
def compute_z_step_kms(frequencies, frequency_0=None):

    # NOTE: In case the shape of the \'frequencies\' array is (n_c, 1), where
    # n_c is the number of channels.
    frequencies = np.squeeze(frequencies)

    # NOTE:
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

    return np.abs(
        convert_frequency_to_velocity_resolution(
            frequency_resolution=frequency_resolution,
            frequency_0=frequency_0,
        )
    )


def convert_frequencies_to_velocities_from_z_centre(frequencies, z_centre):

    # NOTE: If instead I use "frequency_0 = np.average(frequencies)" there is a
    # shift in the rotation curve ...

    frequencies_interp = interpolate.interp1d(
        x=np.arange(len(frequencies)),
        y=frequencies,
        kind="linear"
    )

    frequency_0 = frequencies_interp(z_centre)
    print("f_center =", frequency_0)

    # NOTE:
    # plt.figure()
    # for frequency in frequencies:
    #     plt.axvline(frequency, linewidth=4, color="b", alpha=0.5)
    # plt.axvline(frequency_0, color="black")
    # plt.axvline(np.average(frequencies), color="purple")
    # plt.show()
    # exit()

    return convert_frequencies_to_velocities(
        frequencies=frequencies,
        frequency_0=frequency_0,
    )



# NOTE: THIS WILL BE MOVED
def major_axis(phi, centre, xmin, xmax, pixel_scale=None, n=50):
    """
    The centre is given in arcsec
    """

    a = np.tan((90.0 - phi) * au.deg.to(au.rad))

    x1 = centre[1]
    y1 = centre[0]

    # # NOTE: When plotting reconstructions of a cube model generated with galpak there is an offset.
    # x1 = centre[1] + pixel_scale / 2.0
    # y1 = centre[0] - pixel_scale / 2.0

    x = np.linspace(xmin, xmax, n)
    y = y1 + a * (x - x1)

    # idx = np.logical_and(
    #     np.logical_and(y > 0, y < n_pixels),
    #     np.logical_and(x > 0, x < n_pixels)
    # )

    # x = x[idx]
    # y = y[idx]

    return x, y#, x1, y1


def major_axis_in_pixels(phi, centre, xmin, xmax, n=50):
    pass

def major_axis_updated(phi, centre, dx, n=50):
    """
    The centre is given in arcsec
    """

    phi_1 = 90.0 - phi
    phi_2 = 90.0 - phi + 180.0

    a1 = np.tan(phi_1 * au.deg.to(au.rad))
    a2 = np.tan(phi_2 * au.deg.to(au.rad))

    x_cen = centre[1] #/ pixel_scale + n_pixels / 2.0
    y_cen = centre[0] #/ pixel_scale + n_pixels / 2.0

    x1 = np.linspace(0, dx, n)
    y1 = a1 * x1

    x2 = np.linspace(-dx, 0, n)
    y2 = a2 * x2

    x1 += x_cen
    y1 += y_cen
    x2 += x_cen
    y2 += y_cen

    x = np.concatenate((x2[:-1], x1[1:]))
    y = np.concatenate((y2[:-1], y1[1:]))


    # idx = np.logical_and(
    #     np.logical_and(y > 0, y < n_pixels),
    #     np.logical_and(x > 0, x < n_pixels)
    # )

    # x = x[idx]
    # y = y[idx]

    r = np.sqrt(
        (x - x_cen)**2.0 + (y - y_cen)**2.0
    )
    r[x < x_cen] *= -1.0
    #r[x > x_cen] *= -1.0

    return x, y, r


def major_axis_from_model_and_grid(
    model,
    grid,
    with_shift=True,
    dphi=0.0
):

    if with_shift:
        centre=(
            model.centre[0] - grid.pixel_scale,
            model.centre[1] - grid.pixel_scale,
        )
    else:
        centre=(
            model.centre[0],
            model.centre[1],
        )

    return spectral_plot_utils.major_axis_(
        phi=model.phi + dphi,
        centre=centre,
        pixel_scale=grid.pixel_scale,
        n_pixels=grid.n_pixels,
        xmin=0,
        xmax=grid.n_pixels - 1.0,
        dx=2,
        n=50
    )

# def major_axis_arcsec_from_angle_and_centre(
#     angle,
#     centre,
#     pixel_scale,
#     n_pixels,
#     xmin,
#     xmax,
#     dx=None,
#     n=50
# ):
#     """
#     The centre is given in arcsec
#     """
#
#
#     a = np.tan((angle - 90.0) * units.deg.to(units.rad))
#     a_rot = np.tan((angle - 270.0) * units.deg.to(units.rad))
#
#     x1 = centre[1] / pixel_scale + n_pixels / 2.0
#     y1 = -centre[0] / pixel_scale + n_pixels / 2.0
#
#     # NOTE: This is the correct conversion so that the major-axis is aligned
#     # properly with the centre. This definition is appropriate for how the
#     # "convert_centre_from_arcsec_to_pixels" function is defined in the
#     # "light_profile" (i.e. includes a pixel shift).
#     #x1 = (centre[1] - pixel_scale / 2.0) / pixel_scale + n_pixels / 2.0
#     #y1 = -(centre[0] + pixel_scale / 2.0) / pixel_scale + n_pixels / 2.0
#
#     """
#     if dx is None:
#         x = np.linspace(xmin, xmax, n)
#     else:
#         x = np.arange(xmin, xmax, dx)
#     y = y1 + a * (x - x1)
#
#     idx = np.logical_and(
#         np.logical_and(y > 0, y < n_pixels),
#         np.logical_and(x > 0, x < n_pixels)
#     )
#
#     x = x[idx]
#     y = y[idx]
#
#     print(x, y)
#
#     r = np.sqrt((x - x1)**2.0 + (y - y1)**2.0)
#     r[x < x1] *= -1.0
#
#     return x, y, x1, y1, r
#     """
#
#     if dx is None:
#         x_from_xmax = np.linspace(x1, xmax, n)
#         x_from_xmin = np.linspace(xmin, x1, n)[:-1]
#     else:
#         n = 1
#         x_pos = [x1]
#         x_neg = []
#         while True:
#             x_pos_value = x1 + n * dx
#             x_neg_value = x1 - n * dx
#             print(x_neg_value, x_pos_value)
#             if x_pos_value > xmax or x_neg_value < xmin:
#                 break
#             x_pos.append(x_pos_value)
#             x_neg.append(x_neg_value)
#             n += 1
#
#         # print(x_neg[::-1])
#         # print(x_pos)
#         # exit()
#
#         x = np.concatenate((x_neg[::-1], x_pos))
#
#     y = y1 + a * (x - x1)
#
#     #print(x, y, x1, y1, a);exit()
#
#     idx = np.logical_and(
#         np.logical_and(y > 0, y < n_pixels),
#         np.logical_and(x > 0, x < n_pixels)
#     )
#
#     x = x[idx]
#     y = y[idx]
#
#     #print(x, y)
#
#     r = np.sqrt((x - x1)**2.0 + (y - y1)**2.0)
#     r[x < x1] *= -1.0
#
#     return x, y, x1, y1, r

def major_axis_in_pixels_from_angle_and_centre(
    angle,
    centre,
    n_pixels,
    dx=1,
    angle_offset=90.0
):
    """
    The centre is given in arcsec
    """


    a = np.tan((angle - angle_offset) * au.deg.to(au.rad))

    x1 = centre[0]
    y1 = centre[1]

    # NOTE:
    if dx is None:
        raise NotImplementedError()
    else:
        n = 1
        x_pos = [x1]
        x_neg = []
        while True:
            x_pos_value = x1 + n * dx
            x_neg_value = x1 - n * dx
            if x_pos_value > n_pixels or x_neg_value < 0:
                break
            x_pos.append(x_pos_value)
            x_neg.append(x_neg_value)
            n += 1

        x = np.concatenate((x_neg[::-1], x_pos))

    # NOTE:
    y = y1 + a * (x - x1)

    # NOTE:
    idx = np.logical_and(
        np.logical_and(y > 0, y < n_pixels),
        np.logical_and(x > 0, x < n_pixels)
    )
    x = x[idx]
    y = y[idx]

    # NOTE:
    r = np.sqrt((x - x1)**2.0 + (y - y1)**2.0)
    r[x < x1] *= -1.0

    return x, y, r


def minor_axis_in_pixels_from_angle_and_centre(
    angle,
    centre,
    n_pixels,
    dx=1,
    angle_offset=180.0
):
    """
    The centre is given in arcsec
    """


    a = np.tan((angle - angle_offset) * au.deg.to(au.rad))

    x1 = centre[0]
    y1 = centre[1]

    # NOTE:
    if dx is None:
        raise NotImplementedError()
    else:
        n = 1
        x_pos = [x1]
        x_neg = []
        while True:
            x_pos_value = x1 + n * dx
            x_neg_value = x1 - n * dx
            if x_pos_value > n_pixels or x_neg_value < 0:
                break
            x_pos.append(x_pos_value)
            x_neg.append(x_neg_value)
            n += 1

        x = np.concatenate((x_neg[::-1], x_pos))

    # NOTE:
    y = y1 + a * (x - x1)

    # NOTE:
    idx = np.logical_and(
        np.logical_and(y > 0, y < n_pixels),
        np.logical_and(x > 0, x < n_pixels)
    )
    x = x[idx]
    y = y[idx]

    # NOTE:
    r = np.sqrt((x - x1)**2.0 + (y - y1)**2.0)
    r[x < x1] *= -1.0

    return x, y, r


def extract_from_image_tests(
    image,
    x,
    y,
    show_test_1=True,
    show_test_2=True,
):

    if show_test_1:
        figure, axes = plt.subplots(
            nrows=1, ncols=2
        )
        axes[0].imshow(image, cmap="jet")

        image_temp = copy.copy(image)
        for i, (y_i, x_i) in enumerate(
            zip(np.round(y), np.round(x))
        ):

            image_temp[int(y_i), int(x_i)] = np.nan
        axes[1].imshow(image_temp, cmap="jet")

        axes[0].plot(
            x, y, marker="o", color="black",
        )
        axes[1].plot(
            x, y, marker="o", color="black",
        )

    if show_test_2:
        plt.clf()
        n = 2
        for i, (y_i, x_i) in enumerate(
            zip(np.round(y), np.round(x))
        ):
            image_temp = copy.copy(image)
            for y_ii in np.arange(y_i - n, y_i + n + 1, 1):
                for x_ii in np.arange(x_i - n, x_i + n + 1, 1):
                    image_temp[int(y_ii), int(x_ii)] = np.nan
            figure, axes = plt.subplots(
                nrows=1, ncols=2
            )
            axes[0].imshow(image, cmap="jet")
            axes[0].plot(
                x, y, marker="o", color="black",
            )
            axes[1].imshow(image_temp, cmap="jet")
            axes[1].plot(
                x, y, marker="o", color="black",
            )
            axes[1].plot(
                [x_i], [y_i], marker="*", color="gray",
            )
            plt.show()

    plt.show()
    exit()

def extract_from_image(
    image,
    x,
    y,
    order=1,
    method="1"
):

    if method == "1":

        plt.figure()
        plt.imshow(image, cmap="jet")
        plt.contour(image, levels=[0.0], colors="gray")
        plt.plot(x, y, linestyle="-", marker="o", color="black")
        #plt.show()
        #exit()

        return ndimage.map_coordinates(
            image,
            [y, x],
            order=order,
            cval=np.nan,
        )
    elif method == "2":
        a = np.zeros(shape=(len(x, )))
        for i, (y_i, x_i) in enumerate(
            zip(np.round(y), np.round(x))
        ):

            a[i] = image[int(y_i), int(x_i)]
        return a
    elif method == "3":
        n = 3
        a = np.zeros(shape=(len(x, )))
        for i, (y_i, x_i) in enumerate(
            zip(np.round(y), np.round(x))
        ):
            values = []
            for y_ii in np.arange(y_i - n, y_i + n + 1, 1):
                for x_ii in np.arange(x_i - n, x_i + n + 1, 1):
                    value = image[int(y_ii), int(x_ii)]
                    if not np.isnan(value):
                        values.append(value)
            a[i] = np.average(values)
        return a
    else:
        raise NotImplementedError()


def extract_from_image_with_errors(
    image,
    x,
    y,
    order=1,
    method="1"
):

    a = ndimage.map_coordinates(
        image,
        [y, x],
        order=order,
        cval=np.nan,
    )

    shape_y, shape_x = image.shape

    a_error = np.zeros(shape=(len(x, )))

    method = "2"
    if method == "1":
        n = 3
        for i, (y_i, x_i) in enumerate(
            zip(np.round(y), np.round(x))
        ):
            values = []
            for y_ii in np.arange(y_i - n, y_i + n + 1, 1):
                if y_ii > 0 and y_ii < shape_y:
                    for x_ii in np.arange(x_i - n, x_i + n + 1, 1):
                        if x_ii > 0 and x_ii < shape_x:
                            value = image[int(y_ii), int(x_ii)]
                            if not np.isnan(value):
                                values.append(value)
            a_error[i] = np.nanstd(values)
    if method == "2":
        n = 3
        for i, (y_i, x_i) in enumerate(
            zip(np.round(y), np.round(x))
        ):
            values = []
            for n_i in range(-n, n):
                y_ii = y_i - n_i
                x_ii = x_i + n_i
                if np.logical_and.reduce((
                    y_ii > 0,
                    y_ii < shape_y,
                    x_ii > 0,
                    x_ii < shape_x,
                )):
                    value = image[int(y_ii), int(x_ii)]
                    if not np.isnan(value):
                        values.append(value)

            a_error[i] = np.std(values)#;print(a_error[i])


    return a, a_error

def extract_from_image_with_binning(
    image,
    x,
    y,
    bin=2
):

    a = np.zeros(shape=(len(x, )))
    for i, (y_i, x_i) in enumerate(
        zip(np.round(y), np.round(x))
    ):
        a[i] = np.nanmean(
            np.ndarray.flatten(image[int(y_i - bin):int(y_i + bin + 1), int(x_i - bin):int(x_i + bin + 1)])
        )

    return a


def extract(cube, x, y, order=1):

    nz = cube.shape[0]
    nx = len(x)
    ny = len(y)

    zi = np.outer(
        np.arange(nz, dtype=int),
        np.ones(nx)
    )

    xi = np.outer(
        np.ones(nz),
        x
    )

    yi = np.outer(
        np.ones(nz),
        y
    )

    return ndimage.map_coordinates(
        cube,
        [zi, yi, xi],
        order=order,
        cval=np.nan
    )


def rotation_curve_from(
    velocities,
    pv,
    p0=None,
    bounds=(-np.inf, np.inf),
    vmax=1000.0,
    SNR_limit=3.0,
    limit=None,
    debug=False
):

    def chi_squared_from(y, y_model, sigma):

        return np.sum(
            (y - y_model)**2.0 / sigma**2.0
        )

    def log_likelihood(y, y_model, sigma):

        # if sigma is None:
        #     sigma = np.ones(shape=y.shape)

        chi_squared = chi_squared_from(y=y, y_model=y_model, sigma=sigma)

        return -chi_squared + np.sum(np.log(2 * np.pi * sigma**2.0))

    def BIC(k, n, y, y_model, sigma):

        return k * np.log(n) - log_likelihood(y=y, y_model=y_model, sigma=sigma)

    rotation_curve = np.zeros(
        shape=pv.shape[-1]
    )

    idx = np.where(abs(velocities) > vmax)
    #idx = abs(velocities) > vmax


    x_from = np.linspace(-vmax, vmax, 200)

    if limit is None:
        masks = [
            None for i in range(pv.shape[-1])
        ]
    else:
        pass

    labels = []
    sucess = []
    list_of_p_from_gaussian_x1 = []
    list_of_p_error = []
    list_of_p_from_gaussian_x2 = []
    SNR = np.zeros(shape=pv.shape[-1])
    for i in range(pv.shape[-1]):
        print("i =", i)

        mask = masks[i]

        y = copy.copy(pv[:, i])

        y_normalized = y / np.nanmax(abs(y))

        sigma_from = fitting_utils.fit_gaussian_with_fixed_x0_from_data(
            data=y_normalized,
            x0=0.0,
            bins=5,
            #p0=(10, 0.5),
            #debug=True
        )[-1]

        # NOTE: This is not working great ...
        # _, _, sigma_from = stats.sigmaclip(
        #     y_normalized, low=1.0, high=1.0
        # )
        # #print(sigma_from, lower, upper)
        # #exit()

        sigma = np.multiply(
            abs(sigma_from), np.ones(shape=y_normalized.shape)
        )

        y_normalized[idx] = 0.0



        p0 = (1.0, velocities[np.argmax(y_normalized)], 50.0)
        #print(p0)

        p0_for_gaussian_x2 = (
            1.0, velocities[np.argmax(y_normalized)], 50.0, 1.0, 0.0, 50.0
        )

        if np.isnan(y_normalized).any():
            list_of_p_from_gaussian_x1.append(None)

            rotation_curve[i] = np.nan
        else:
            try:
                p, p_cov = fitting_utils.fit_gaussian(
                    x=velocities,
                    y=y_normalized,
                    p0=p0,
                    bounds=bounds,
                    sigma=sigma
                )

                list_of_p_from_gaussian_x1.append(p)
                list_of_p_error.append(np.sqrt(np.diag(p_cov)))

                #rotation_curve[i] = p[1]
            except:
                list_of_p_from_gaussian_x1.append(None)
                list_of_p_error.append(None)

                #rotation_curve[i] = np.nan

            try:
                p_from_gaussian_x2, _ = fitting_utils.fit_gaussian_x2(
                    x=velocities,
                    y=y_normalized,
                    p0=p0_for_gaussian_x2,
                    bounds=bounds,
                    sigma=sigma,
                    maxfev=10000,
                )

                list_of_p_from_gaussian_x2.append(p_from_gaussian_x2)
            except:
                list_of_p_from_gaussian_x2.append(None)

            # y_model = fitting_utils.gaussian(velocities, *p)
            # likelihood_from_fit = likelihood(
            #     y=y,
            #     y_model=y_model,
            #     sigma=np.multiply(abs(sigma), np.ones(shape=y.shape))
            # )
            # likelihood_from = likelihood(
            #     y=y,
            #     y_model=np.zeros(shape=y.shape),
            #     sigma=np.multiply(abs(sigma), np.ones(shape=y.shape))
            # )
            # print(i, likelihood_from_fit, likelihood_from, "HERE")

            chi_squared_from_line = chi_squared_from(
                y=y_normalized,
                y_model=np.zeros(shape=y_normalized.shape),
                sigma=sigma
            )



            if list_of_p_from_gaussian_x1[i] is None:
                SNR_from_gaussian_x1 = -np.inf
                BIC_for_p_from_gaussian_x1 = np.inf
            elif np.isnan(list_of_p_from_gaussian_x1[i]).any():
                SNR_from_gaussian_x1 = -np.inf
                BIC_for_p_from_gaussian_x1 = np.inf
            else:
                y_model_for_p_from_gaussian_x1 = fitting_utils.gaussian(
                    velocities, *list_of_p_from_gaussian_x1[i]
                )

                chi_squared_from_gaussian_x1 = chi_squared_from(
                    y=y_normalized,
                    y_model=y_model_for_p_from_gaussian_x1,
                    sigma=sigma
                )

                SNR_from_gaussian_x1 = (chi_squared_from_line - chi_squared_from_gaussian_x1)**0.5

                BIC_for_p_from_gaussian_x1 = BIC(
                    k=len(list_of_p_from_gaussian_x1[i]),
                    n=len(y_normalized),
                    y=y_normalized,
                    y_model=y_model_for_p_from_gaussian_x1,
                    sigma=sigma
                )

            if list_of_p_from_gaussian_x2[i] is None:
                SNR_from_gaussian_x2 = -np.inf
                BIC_for_p_from_gaussian_x2 = np.inf
            elif np.isnan(list_of_p_from_gaussian_x2[i]).any():
                SNR_from_gaussian_x2 = -np.inf
                BIC_for_p_from_gaussian_x2 = np.inf
            else:
                y_model_for_p_from_gaussian_x2 = fitting_utils.gaussian_x2(
                    velocities, *list_of_p_from_gaussian_x2[i]
                )

                chi_squared_from_gaussian_x2 = chi_squared_from(
                    y=y_normalized,
                    y_model=y_model_for_p_from_gaussian_x2,
                    sigma=sigma
                )

                SNR_from_gaussian_x2 = (chi_squared_from_line - chi_squared_from_gaussian_x2)**0.5

                BIC_for_p_from_gaussian_x2 = BIC(
                    k=len(list_of_p_from_gaussian_x2[i]),
                    n=len(y_normalized),
                    y=y_normalized,
                    y_model=y_model_for_p_from_gaussian_x2,
                    sigma=sigma
                )

            if SNR_from_gaussian_x1 < SNR_limit and SNR_from_gaussian_x2 < SNR_limit:
                rotation_curve[i] = np.nan
                sucess.append(False)
                labels.append(None)
            else:
                sucess.append(True)

                print(
                    i,
                    SNR_from_gaussian_x1,
                    SNR_from_gaussian_x2,
                    list_of_p_from_gaussian_x1[i],
                    list_of_p_from_gaussian_x2[i],
                    "BIC (x1) =", BIC_for_p_from_gaussian_x1,
                    "BIC (x2) =", BIC_for_p_from_gaussian_x2,
                    "x1" if BIC_for_p_from_gaussian_x1 < BIC_for_p_from_gaussian_x2 else "x2"
                )

                if BIC_for_p_from_gaussian_x1 < BIC_for_p_from_gaussian_x2:
                    p = list_of_p_from_gaussian_x1[i]
                    rotation_curve[i] = p[1]
                    SNR[i] = SNR_from_gaussian_x1
                    labels.append("x1")
                else:
                    p = list_of_p_from_gaussian_x2[i]
                    rotation_curve[i] = p[1] if p[0] > p[3] else p[4]
                    SNR[i] = SNR_from_gaussian_x2
                    labels.append("x2")

                    # NOTE: THIS IS NOT WHAT I WANT
                    # y_model_for_p_from_gaussian_1 = fitting_utils.gaussian(
                    #     velocities, *list_of_p_from_gaussian_x2[i][:3]
                    # )
                    # y_model_for_p_from_gaussian_2 = fitting_utils.gaussian(
                    #     velocities, *list_of_p_from_gaussian_x2[i][3:]
                    # )
                    # chi_squared_from_gaussian_1 = chi_squared_from(
                    #     y=y_normalized,
                    #     y_model=y_model_for_p_from_gaussian_1,
                    #     sigma=sigma
                    # )
                    # chi_squared_from_gaussian_2 = chi_squared_from(
                    #     y=y_normalized,
                    #     y_model=y_model_for_p_from_gaussian_2,
                    #     sigma=sigma
                    # )
                    #
                    # if chi_squared_from_gaussian_1 < chi_squared_from_gaussian_2:
                    #     rotation_curve[i] = p[1]
                    # else:
                    #     rotation_curve[i] = p[4]

    # NOTE: ...
    if debug:

        ncols = 8
        nrows = int(np.ceil(float(pv.shape[-1]) / ncols))

        figure_for, axes_for = plt.subplots(
            nrows=nrows, ncols=ncols
        )
        for i, ax in enumerate(
            matplotlib_utils.axes_iterable(axes=axes_for)
        ):
            if i < pv.shape[-1]:
                y = pv[:, i]
                y_normalized = y / np.nanmax(abs(y))

                ax.hist(y_normalized, bins=5)

                ax.axvline(0.0, linestyle=":", color="black")

                ax.set_yticks([])
                ax.set_xlim(-1.0, 1.0)

        figure, axes = plt.subplots(nrows=nrows, ncols=ncols)
        for i, ax in enumerate(
            matplotlib_utils.axes_iterable(axes=axes)
        ):
            if i < pv.shape[-1]:
                print("i =", i)
                y = pv[:, i]
                y_normalized = y / np.nanmax(abs(y))

                # NOTE:
                sigma = fitting_utils.fit_gaussian_with_fixed_x0_from_data(
                    data=y_normalized,
                    x0=0.0,
                    bins=20,
                )[-1]

                ax.plot(velocities, y_normalized, marker="o", color="b", alpha=0.75)

                y_normalized[idx] = 0.0

                #ax.axvline(velocities[np.argmax(y_normalized)], linestyle="-", color="purple")

                ax.axhline(
                    +abs(sigma), linestyle="--", color="black"
                )
                ax.axhline(
                    -abs(sigma), linestyle="--", color="black"
                )
                ax.axhspan(
                    ymin=sigma, ymax=-sigma, color="black", alpha=0.25
                )

                ax.axvline(0.0, linestyle=":", color="black")
                ax.axhline(0.0, linestyle=":", color="black")


                if sucess[i]:

                    if list_of_p_from_gaussian_x1[i] is not None:
                        y_from_fit = fitting_utils.gaussian(
                            x_from, *list_of_p_from_gaussian_x1[i]
                        )
                        ax.plot(
                            x_from,
                            y_from_fit,
                            linewidth=2,
                            color="black",
                            #label=r"$\mu = {}$".format(int(p[1]))
                            label="fit" if labels[i] == "x1" else ""
                        )

                    if list_of_p_from_gaussian_x2[i] is not None:
                        y_from_fit_with_gaussian_x2 = fitting_utils.gaussian_x2(
                            x_from, *list_of_p_from_gaussian_x2[i]
                        )

                        ax.plot(
                            x_from,
                            y_from_fit_with_gaussian_x2,
                            linewidth=4,
                            color="yellow",
                            alpha=0.5,
                            label="fit" if labels[i] == "x2" else ""
                        )

                    #ax.axvline(p[1], linestyle=":", color="r")

                ax.set_xlim(-2.0 * vmax, 2.0 * vmax)
                ax.set_ylim(-1.25, 1.25)

                if i == pv.shape[-1] - 1:
                    ax.yaxis.tick_right()
                    ax.set_xlabel("v (km / s)", fontsize=15)
                else:
                    ax.set_xticks([])
                    ax.set_yticks([])

                ax.legend(loc=0, fontsize=5)

            else:
                ax.axis("off")

        plt.subplots_adjust(wspace=0.0, hspace=0.0, left=0.05, right=0.95, bottom=0.2, top=0.95)
        #plt.show()

    return rotation_curve, list_of_p_from_gaussian_x1, list_of_p_error



def pv_with_binning(dirty_cube, x_ma, y_ma, radius=1):

    pv_from_dirty_cube = np.zeros(
        shape=(dirty_cube.shape[0], x_ma.shape[0])
    )

    y_indeces, x_indeces = np.indices(dimensions=dirty_cube.shape[1:])

    x_ma = np.round(x_ma)
    y_ma = np.round(y_ma)
    for j, (x_n, y_n) in enumerate(
        zip(x_ma, y_ma)
    ):

        r = np.sqrt(
            np.add(
                (x_indeces - x_n)**2.0,
                (y_indeces - y_n)**2.0
            )
        )
        idx = r < radius

        for i in range(dirty_cube.shape[0]):

            pv_from_dirty_cube[i, j] = np.mean(dirty_cube[i, idx])

    return pv_from_dirty_cube


def plot_pv_as(pv, velocities=None, normalization=False, nrows=None, ncols=None, axes=None, return_axes=False):

    if axes is None:


        figure, axes = plt.subplots(
            nrows=nrows, ncols=ncols
        )

    for i, ax in enumerate(
        matplotlib_utils.axes_iterable(axes=axes)
    ):

        if i < pv.shape[-1]:
            #y = pv[i, :]
            y = pv[:, i]

            if normalization:
                y /= np.nanmax(y)

            ax.plot(y, color="black")
        else:
            ax.axis("off")

    if return_axes:
        return axes




def line_rest_frequency(line):

    lines = {
        "CO 1-0": 115.271,
        "CO 2-1": 230.538,
        "CO 3-2": 345.796,
        "CO 4-3": 461.041,
        "CO 5-4": 576.268,
        "CO 6-5": 691.473,
        "CO 7-6": 806.652,
        "CO 8-7": 921.800,
        "CO 9-8": 1036.912,
    }

    if line in lines.keys():
        return lines[line]




def sigma_real_space_from_cube(
    cube: np.ndarray,
    figure_1_for_debugging=False
):

    sigma_real_space_per_slice = noise_from_cube(
        cube=cube
    )

    # if figure_1_for_debugging:
    #     pass

    sigma_real_space_per_slice_clipped, _, _ = stats.sigmaclip(
        a=sigma_real_space_per_slice,
        low=3.0,
        high=3.0
    )

    return np.mean(sigma_real_space_per_slice_clipped)


def rms_from_cube(
    cube,
):

    rms = np.zeros(shape=cube.shape[0])

    for i, cube_slice in enumerate(cube):
        idx = np.isnan(cube_slice)
        values = cube_slice[~idx]

        rms[i] = np.sqrt(np.mean(np.power(values, 2.0)))

    return rms


def noise_from_image(
    image: np.ndarray,
    p0=None,
    bins=25,
    x0=None,
    sigma_clipping=True,
    low_for_sigma_clipping=5.0,
    high_for_sigma_clipping=5.0,
    figure_0_for_debugging=False,
    show_figures=False
):


    data = np.ndarray.flatten(image)

    xmax = np.nanmax(data)
    xmin = np.nanmin(data)

    data_indexed = data[~np.isnan(data)]

    if sigma_clipping:
        data_indexed = stats.sigmaclip(
            data_indexed,
            low=low_for_sigma_clipping,
            high=high_for_sigma_clipping
        ).clipped

    if p0 is None:
        # plt.figure()
        # plt.hist(data_indexed, bins=50)
        # plt.show()

        y, x = np.histogram(
            a=data_indexed,
            bins=bins,
            density=1.0
        )

        x = (x[:-1] + x[1:]) / 2.0

        if x0 is None:
            p = fitting_utils.fit_gaussian(
                x=x,
                y=y,
                p0=(np.max(y), np.mean(data_indexed), np.std(data_indexed)),
                return_cov=False
            )
        elif x0 == 0.0:
            p = fitting_utils.fit_gaussian_with_fixed_x0(
                x=x,
                y=y,
                x0=0.0,
                p0=(np.max(y), np.std(data_indexed)),
                return_cov=False
            )
        else:
            raise NotImplementedError()

    else:
        p, x = fitting_utils.fit_gaussian_with_fixed_x0_from_data(
            data=data_indexed,
            x0=0.0,
            bins=bins,
            density=1.0,
            p0=p0,
            return_x=True
        )

    print("p =", p)

    if figure_0_for_debugging:

        plt.figure()
        plt.hist(data_indexed, bins=bins, density=1.0, histtype="stepfilled", color="b")


        x_for_plotting = np.linspace(
            np.min(x),
            np.max(x),
            500
        )
        if x0 is None:
            y_for_plotting = fitting_utils.gaussian(
                x=x_for_plotting,
                A=p[0],
                x0=p[1],
                sigma=p[2]
            )
        elif x0 == 0.0:
            y_for_plotting = fitting_utils.gaussian(
                x=x_for_plotting,
                A=p[0],
                x0=0.0,
                sigma=p[1]
            )
        else:
            raise NotImplementedError()

        plt.plot(x_for_plotting, y_for_plotting, color="black")

        if show_figures:
            plt.show()

    return p

def noise_from_cube(
    cube,
    bins=25,
    p0=None,#p0=(0.005, 100),
    figure_1_for_debugging=False,
    nrows=None,
    ncols=None,
    zmin_for_plotting=None,
    zmax_for_plotting=None,
):

    xmin = +np.infty
    xmax = -np.infty

    list_of_p = []
    for i, slice in enumerate(cube):
        #print(i)
        data = np.ndarray.flatten(slice)#;print(data)
        if np.nanmax(data) > xmax:
            xmax = np.nanmax(data)
        if np.nanmin(data) < xmin:
            xmin = np.nanmin(data)

        if xmin == 0.0 and xmax == 0.0:
            list_of_p.append(None)
            #print(i, "None")
        else:
            idx = np.isnan(data)
            data_indexed = data[~idx]
            #print(data_indexed)
            #print(i, xmin, xmax)

            if p0 is None:
                y, x = np.histogram(
                    a=data_indexed,
                    bins=bins,
                    density=1.0
                )
                x = (x[:-1] + x[1:]) / 2.0

                p0_temp = (np.max(y), np.std(data_indexed)); print("p0:", p0_temp)
                p = fitting_utils.fit_gaussian_with_fixed_x0(
                    x=x,
                    y=y,
                    x0=0.0,
                    p0=(np.max(y), np.std(data_indexed)),
                    return_cov=False
                )
                print("p:", p)
            else:
                p, x = fitting_utils.fit_gaussian_with_fixed_x0_from_data(
                    data=data_indexed,
                    x0=0.0,
                    bins=bins,
                    density=1.0,
                    p0=p0,
                    return_x=True
                )
            #print(p)

            list_of_p.append(p)

            # NOTE: Visualization ->
            # figure, axes = plt.subplots()
            #
            # y_model = fitting_utils.gaussian(
            #     x=x, A=p[0], x0=0.0, sigma=p[1]
            # )
            #
            # _, _, _ = axes.hist(
            #     data,
            #     bins=bins,
            #     density=1.0,
            #     color="b",
            #     alpha=0.5
            # )
            # axes.plot(
            #     x,
            #     y_model,
            #     linewidth=2,
            #     color="black",
            #     alpha=0.75,
            #     label="fit"
            # )
            #
            # axes.axvline(0.0, linestyle="--", color="black")
            # axes.set_xlim(xmin, xmax)
            #
            # axes.set_xticks([])
            # axes.set_yticks([])
            #
            # plt.show()

    # NOTE: FIGURE 0
    if figure_1_for_debugging:

        if zmin_for_plotting is None:
            j = 0
        else:
            j = zmin_for_plotting

        if nrows is None:
            nrows = 4
        if ncols is None:
            ncols = 10

        figure, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols
        )

        # n = len(np.ndarray.flatten(axes))
        # print(n)
        # exit()

        xmin_for_plotting = +np.infty
        xmax_for_plotting = -np.infty
        ymax_for_plotting = -np.infty
        x = np.linspace(xmin, xmax, 100)
        for i, ax in enumerate(
            np.ndarray.flatten(axes)
        ):
            n = i + j

            if n < cube.shape[0]:
                if list_of_p[n] is not None:

                    data = np.ndarray.flatten(cube[n, ...])

                    if np.nanmax(data) > xmax_for_plotting:
                        xmax_for_plotting = np.nanmax(data)
                    if np.nanmin(data) < xmin_for_plotting:
                        xmin_for_plotting = np.nanmin(data)

                    idx = np.isnan(data)
                    data_indexed = data[~idx]

                    bin_values, _, _ = ax.hist(
                        data_indexed,
                        bins=bins,
                        density=1.0,
                        color="b",
                        alpha=0.5
                    )

                    if np.max(bin_values) > ymax_for_plotting:
                        ymax_for_plotting = np.max(bin_values)

                    p = list_of_p[n]
                    print(p)

                    y_model = fitting_utils.gaussian(
                        x=x,
                        A=p[0],
                        x0=0.0,
                        sigma=p[1]
                    )

                    ax.plot(
                        x,
                        y_model,
                        linewidth=2,
                        color="black",
                        alpha=0.75,
                        label="fit"
                    )
                else:
                    ax.axis("off")
            else:
                ax.axis("off")

        for i, ax in enumerate(np.ndarray.flatten(axes)):
            ax.set_xlim(
                xmin_for_plotting,
                xmax_for_plotting
            )
            ax.set_ylim(0.0, ymax_for_plotting)

        axes[0, -1].set_xlabel("(Jy)", fontsize=15)


        plt.figure()
        plt.plot(
            [abs(p[1]) for p in list_of_p if p is not None],
            marker="o"
        )
        plt.xlabel("# of channels", fontsize=15)
        plt.ylabel("$\sigma$ (mJy)", fontsize=15)

        #plt.show()

    # return np.array([
    #     abs(p[1]) for p in list_of_p
    #     if p is not None
    # ])

    def sanitize(a):
        if a == 0.0:
            return np.nan
        else:
            return a

    return np.array([
        sanitize(a=abs(p[1]))
        if p is not None else np.nan
        for p in list_of_p
    ])



def masked_cube_from_z_mask(cube, mask):

    masked_cube = copy.deepcopy(cube)

    masked_cube[mask] = 0.0

    return masked_cube


def masked_cube_from_fmin(cube, fmin):

    masked_cube = copy.deepcopy(cube)

    masked_cube[masked_cube < fmin] = 0.0

    return masked_cube

def masked_cube_from_z_mask_and_fmin(
    cube: np.ndarray,
    mask,
    fmin,
    figure_1_for_debugging=False
):

    masked_cube = masked_cube_from_z_mask(
        cube=cube,
        mask=mask
    )

    if figure_1_for_debugging:
        plot_utils.plot_cube(cube=masked_cube, ncols=10)

    return masked_cube_from_fmin(
        cube=masked_cube,
        fmin=fmin
    )



def major_axis_(
    phi,
    centre,
    pixel_scale,
    n_pixels,
    xmin,
    xmax,
    dx=None,
    n=50
):
    """
    The centre is given in arcsec
    """


    a = np.tan((phi - 90.0) * au.deg.to(au.rad))
    a_rot = np.tan((phi - 270.0) * au.deg.to(au.rad))

    x1 = centre[1] / pixel_scale + n_pixels / 2.0
    y1 = -centre[0] / pixel_scale + n_pixels / 2.0

    # NOTE: This is the correct conversion so that the major-axis is aligned
    # properly with the centre. This definition is appropriate for how the
    # "convert_centre_from_arcsec_to_pixels" function is defined in the
    # "light_profile" (i.e. includes a pixel shift).
    #x1 = (centre[1] - pixel_scale / 2.0) / pixel_scale + n_pixels / 2.0
    #y1 = -(centre[0] + pixel_scale / 2.0) / pixel_scale + n_pixels / 2.0

    """
    if dx is None:
        x = np.linspace(xmin, xmax, n)
    else:
        x = np.arange(xmin, xmax, dx)
    y = y1 + a * (x - x1)

    idx = np.logical_and(
        np.logical_and(y > 0, y < n_pixels),
        np.logical_and(x > 0, x < n_pixels)
    )

    x = x[idx]
    y = y[idx]

    print(x, y)

    r = np.sqrt((x - x1)**2.0 + (y - y1)**2.0)
    r[x < x1] *= -1.0

    return x, y, x1, y1, r
    """

    if dx is None:
        x_from_xmax = np.linspace(x1, xmax, n)
        x_from_xmin = np.linspace(xmin, x1, n)[:-1]
    else:
        n = 1
        x_pos = [x1]
        x_neg = []
        while True:
            x_pos_value = x1 + n * dx
            x_neg_value = x1 - n * dx
            print(x_neg_value, x_pos_value)
            if x_pos_value > xmax or x_neg_value < xmin:
                break
            x_pos.append(x_pos_value)
            x_neg.append(x_neg_value)
            n += 1

        # print(x_neg[::-1])
        # print(x_pos)
        # exit()

        x = np.concatenate((x_neg[::-1], x_pos))

    y = y1 + a * (x - x1)

    #print(x, y, x1, y1, a);exit()

    idx = np.logical_and(
        np.logical_and(y > 0, y < n_pixels),
        np.logical_and(x > 0, x < n_pixels)
    )

    x = x[idx]
    y = y[idx]

    #print(x, y)

    r = np.sqrt((x - x1)**2.0 + (y - y1)**2.0)
    r[x < x1] *= -1.0

    return x, y, x1, y1, r


def velocities_from_frequencies_transition_and_redshift(
    frequencies: np.ndarray,
    transition,
    redshift: np.float
):

    frequency_0 = observed_line_frequency_from_rest_line_frequency(
        frequency=rest_frame_CO_frequencies(
            transition=transition
        ),
        redshift=redshift
    ) * au.GHz.to(au.Hz)

    return convert_frequencies_to_velocities(
        frequencies=frequencies, frequency_0=frequency_0,
    )

def masking_non_contigeous_with_multiple_components(
    a, n_components=2, value=np.nan, return_mask=False
):

    if np.isnan(value):
        idx = np.isnan(a)
    else:
        idx = a == value


    a_sanitized = np.zeros(shape=a.shape)
    a_sanitized[~idx] = 1.0

    # figure, axes = plt.subplots(nrows=1, ncols=2)
    # axes[0].imshow(a)
    # axes[1].imshow(a_sanitized)
    # plt.show()
    # exit()



    a_labeled, n_labels = ndimage.label(a_sanitized)
    # print("N (labels) =", n_labels)
    # plt.figure()
    # plt.imshow(a_labeled)
    # plt.show()
    # exit()

    labels = np.arange(
        1, n_labels + 1
    )

    n_for_label = [
        np.sum(a_labeled == label)
        for label in labels
    ]

    mask = np.zeros(shape=a.shape)
    for i, (n, label) in enumerate(
        sorted(
            zip(n_for_label, labels),
            key=lambda x: x[0],
            reverse=True
        )
    ):
        if i < n_components:
            idx = a_labeled == label

            mask[idx] = 1.0

    mask = mask.astype(bool)

    a_copy = copy.copy(a)
    a_copy[~mask] = np.nan

    if return_mask:
        return a_copy, mask
    else:
        return a_copy


def masking_non_contigeous(
    a, value=np.nan, return_mask=False
):


    # plt.figure()
    # plt.imshow(a)
    # plt.show()
    # exit()

    if np.isnan(value):
        idx = np.isnan(a)
    else:
        idx = a == value

    a_sanitized = copy.copy(a)

    a_sanitized[idx] = 0.0
    a_sanitized[~idx] = 1.0
    # plt.figure()
    # plt.imshow(a_sanitized)
    # plt.show()
    # exit()

    a_labeled, n_labels = ndimage.label(a_sanitized.astype(int))
    #print("n (labels) =", n_labels)

    # plt.figure()
    # plt.imshow(a_labeled)
    # plt.show()
    # exit()

    if n_labels == 1:
        return a

    n_total = 0
    n = 0
    for label in range(1, n_labels + 1):
        idx = a_labeled == label

        #print(label, np.sum(idx))
        if np.sum(idx) > n_total:
            n_total = np.sum(idx)
            n = label

    mask = a_labeled == n

    a_copy = copy.copy(a)
    a_copy[~mask] = np.nan

    if return_mask:
        return a_copy, mask
    else:
        return a_copy

def masked_slices_from_z_mask(z_mask):

    return [
        i for i, z in enumerate(z_mask) if z
    ]


def ALESS(id):

    if id == "ALESS_071.1":
        filename = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/cube_data_ALESS71.fits"
        frequencies = fits.getdata(filename="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/frequencies_ALESS71.fits")

        dx=2
        zmin_for_sigma = 8
        zmax_for_sigma = 120
        zmin_for_z_mask = 40
        zmax_for_z_mask = 58

        centre = (2.889, 3.051)
        phi = 139.971
        z_centre = 47.799

        moment_1_vmin = -300
        moment_1_vmax = 300
        r_min = -2.0
        r_max = 2.0

        redshift = 3.7072  # NOTE: z-spec (CO)
        transition = "4-3"

        pixel_scale = 0.1
        n_pixels = 128

    if id == "ALESS_075.1":
        filename = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/cube_data_ALESS75.fits"

        dx=5
        moment_1_vmin = -275
        moment_1_vmax = 275
        r_min = -2.5
        r_max = 2.5

        zmin_for_sigma = 8
        zmax_for_sigma = 120
        # z_mask =

        zmin_for_z_mask = 36
        zmax_for_z_mask = 58

        frequencies = fits.getdata(filename="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/frequencies_ALESS75.fits")
        redshift = 2.5521  # NOTE: z-spec (CO)
        transition = "3-2"

        pixel_scale = 0.1
        n_pixels = 256

        phi = 114.574
        centre = (-4.107, -0.694)
        z_centre = 45.772

        BMAJ = 4.163157277637E-04
        BMIN = 3.204851349195E-04
        BPA = -8.561631011963E+01

    if id == "ALESS_041.1":
        filename = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/cube_data_ALESS41.fits"

        frequencies = fits.getdata(filename="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/frequencies_ALESS41.fits")
        redshift = 2.5473
        transition = "3-2"

        centre = (-2.027, 1.432)
        z_centre = 55.118
        phi = 255.234

        moment_1_vmin = -350
        moment_1_vmax = 350
        r_min = -2.0
        r_max = 2.0

        zmin_for_sigma = 8
        zmax_for_sigma = 120
        # z_mask =

        zmin_for_z_mask = 44
        zmax_for_z_mask = 68

        pixel_scale = 0.1
        n_pixels = 256
        dx = 5

    width = BMAJ * au.deg.to(au.arcsec) / pixel_scale
    height = BMIN * au.deg.to(au.arcsec) / pixel_scale
    # ellipse = patches.Ellipse(
    #     xy=(width, height),
    #     width=width,
    #     height=height,
    #     angle=90. + BPA
    # )
    #exit()

    x_major_axis, y_major_axis, x_centre, y_centre, r = major_axis_(
        phi=phi,
        centre=centre,
        pixel_scale=pixel_scale,
        n_pixels=n_pixels,
        xmin=0,
        xmax=n_pixels - 1.0,
        dx=dx,
        n=20
    )

    dirty_cube = fits.getdata(filename)#;print(dirty_cube.shape);exit()

    # velocities = velocities_from_frequencies_transition_and_redshift(
    #     frequencies=frequencies,
    #     transition=transition,
    #     redshift=redshift,
    # )
    velocities = convert_frequencies_to_velocities_from_z_centre(
        frequencies=frequencies, z_centre=z_centre
    )

    sigma_dirty_cube = np.mean(
        a=noise_from_cube(
            cube=dirty_cube[zmin_for_sigma:zmax_for_sigma]
        )
    )

    z_mask = z_mask_from_zmin_and_zmax(
        shape=(dirty_cube.shape[0], ),
        zmin=zmin_for_z_mask,
        zmax=zmax_for_z_mask
    )

    dirty_cube_masked = masked_cube_from_z_mask(
        cube=dirty_cube, mask=z_mask
    )

    f_min = 3.0 * sigma_dirty_cube
    # dirty_cube_masked[dirty_cube < f_min] = 0.0
    # plot_utils.plot_cube(cube=dirty_cube_masked, ncols=10)
    # plt.show()

    # moment_0_from_dirty_cube = moment_0(
    #     cube=dirty_cube_masked,
    #     velocities=velocities,
    #     f_min=f_min,
    # )
    moment_1_from_dirty_cube = moment_1(
        cube=dirty_cube_masked,
        velocities=velocities,
        f_min=f_min,
    )

    moment_1_from_dirty_cube = masking_non_contigeous(
        a=moment_1_from_dirty_cube
    )

    # gradient_of_moment_1_from_dirty_cube_y, gradient_of_moment_1_from_dirty_cube_x = np.gradient(moment_1_from_dirty_cube)
    # print(gradient_of_moment_1_from_dirty_cube_y.shape)
    # plt.figure()
    # plt.imshow(
    #     #gradient_of_moment_1_from_dirty_cube_x
    #     np.sqrt(gradient_of_moment_1_from_dirty_cube_y**2.0 + gradient_of_moment_1_from_dirty_cube_x**2.0),
    #     vmin=0.0,
    #     vmax=20.
    # )
    # plt.colorbar()
    # plt.show()
    # exit()

    figure, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5.5))

    #plt.figure()
    axes[0].imshow(
        moment_1_from_dirty_cube,
        cmap="jet",
        vmin=moment_1_vmin,
        vmax=moment_1_vmax,
        aspect="auto"
    )
    axes[0].plot(x_major_axis, y_major_axis, marker="o", color="black")
    axes[0].set_xlim(x_centre - 25, x_centre + 25)
    axes[0].set_ylim(y_centre - 25, y_centre + 25)
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    #plt.colorbar()
    #plt.show()

    xy_ellipse = (x_centre - 25 + width - width / 3., y_centre - 25 + height - height / 3.0)
    ellipse = patches.Ellipse(
        xy=xy_ellipse,
        width=width,
        height=height,
        angle=90. + BPA
    )
    ellipse.set_facecolor("black")
    ellipse_1 = patches.Ellipse(
        xy=xy_ellipse,
        width=2.0 * dx,
        height=2.0 * dx,
        angle=0.0
    )
    axes[0].add_artist(ellipse)
    axes[0].add_artist(ellipse_1)


    #plt.figure()
    for bin in [1]:
        moment_1_1d = extract_from_image_with_binning(
            image=moment_1_from_dirty_cube,
            x=x_major_axis,
            y=y_major_axis,
            bin=bin
        )

        axes[1].plot(r * pixel_scale, moment_1_1d, marker="o", color="black")
    axes[1].set_xlim(r_min, r_max)
    axes[1].set_ylim(moment_1_vmin, moment_1_vmax)
    axes[1].axvline(0.0, linestyle="--", color="black")
    axes[1].axhline(0.0, linestyle="--", color="black")
    axes[1].set_xlabel(r"$\mathbf{r}$ (arcsec)", fontsize=15)
    axes[1].set_ylabel(r"$\mathbf{V}(r)$ (km / s)", fontsize=15)
    plt.show()





def fit_spectrum_with_gaussian_x2(
    spectrum,
    x=None,
    p0=None,
):

    p, _ = fitting_utils.fit_gaussian_x2(
        x=np.arange(len(spectrum)) if x is None else x,
        y=spectrum,
        p0=p0,
        #return_cov=True
    )
    print(p)

    return p


def integrated_spectra_from_mask(
    cube,
    mask,
    x=None,
    xlabel="$\lambda$ (um)",
    min_value=None,
    max_value=None,
    xlim=None,
    ylim=None,
    visualization=False,
    marker="o",
    color="black",
    filename=None,
    figure=None,
    axes=None
):

    if min_value is not None:
        cube[cube < min_value] = np.nan
    if max_value is not None:
        cube[cube > max_value] = np.nan
    if x is None:
        x = np.arange(cube.shape[0])

    nz, ny, nx = cube.shape
    if mask.shape == (ny, nx):
        pass
    else:
        raise NotImplementedError()

    # --- #

    spectrum = np.zeros(shape=(nz, ))
    for i in range(nz):
        slice = cube[i, :, :]
        slice[mask] = np.nan

        # NOTE:
        # plt.figure()
        # plt.imshow(slice)
        # plt.show()
        # exit()

        spectrum[i] = np.nansum(slice)

    if filename is not None:
        np.save(filename, [x, spectrum]);exit()

    if visualization:
        if not np.logical_and(
            figure, axes
        ):
            figure, axes = plt.subplots(
                figsize=(18, 5)
            )
        axes.plot(
            x,
            spectrum,
            marker=marker,
            color=color,
        )
        axes.set_ylim(ylim)
        axes.set_xlabel(
            xlabel,
            fontsize=15
        )
        # axes.set_ylabel(
        #     "$F_{\lambda}$ (units)",
        #     fontsize=15
        # )

        return figure, axes
    # --- #


def get_rest_frequency(line):

    if line == "CII":
        return 1900.536900
    elif line == "CO(5-4)":
        return rest_frame_CO_frequencies(transition="5-4")
    elif line == "CO(6-5)":
        return rest_frame_CO_frequencies(transition="6-5")
    elif line == "CO(7-6)":
        return rest_frame_CO_frequencies(transition="7-6")
    elif line == "CO(8-7)":
        return rest_frame_CO_frequencies(transition="8-7")
    elif line == "CI(1-0)":
        return 492.1607
    elif line == "CI(2-1)":
        return 809.3435
    else:
        raise NotImplementedError()


def averages_within_circles_from_image_and_centres(image, x, y, radius=2):

    y_indices, x_indices = np.indices(image.shape)

    array = []
    for x_i, y_i in zip(x, y):
        x_i = int(x_i)
        y_i = int(y_i)

        r = np.hypot(x_indices - x_i, y_indices - y_i)

        # idx = r < radius
        # plt.figure()
        # plt.imshow(r)
        # plt.show()
        # exit()
        values = image[r < radius]
        if np.any(values):
            v_averaged = np.average(values[~np.isnan(values)])
        else:
            v_averaged = None
        array.append(v_averaged)

    return np.array(array)


def redshift_from_rest_and_observed_frequecies(rest_frequency, observed_frequency):

    return rest_frequency / observed_frequency - 1.0

if __name__ == "__main__":

    # NOTE: PJ0116
    print(
        observed_CO_frequency(
            redshift=2.125, transition="7-6"
        )
    );exit()

    # NOTE: 9io9
    print(
        observed_CO_frequency(
            redshift=2.554, transition="3-2"
        )
    );exit()

    # NOTE: J0331-0741 (2019.1.01587.S; Lelli F.)
    print(
        #observed_line_frequency_from_rest_line_frequency(frequency=1900.536900, redshift=4.73678)
        #observed_line_frequency_from_rest_line_frequency(frequency=1900.536900, redshift=4.67850)
        observed_line_frequency_from_rest_line_frequency(frequency=1900.536900, redshift=2.9345)
        #observed_line_frequency_from_rest_line_frequency(frequency=1251.360635, redshift=2.583)
    );exit()

    # # NOTE: SPT-2147 (lens)
    # print(
    #     rest_line_wavelength_from_observed_line_wavelength(wavelength=3.56, redshift=0.845) * au.micron.to(au.nm),
    # );exit()

    # # NOTE: SGP38326
    # print(
    #     observed_line_frequency_from_rest_line_frequency(frequency=1900.536900, redshift=4.4237)
    # )
    # exit()

    # NOTE: jwst proposal
    print(
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.6, redshift=2.0) * au.micron.to(au.nm),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.6, redshift=5.0) * au.micron.to(au.nm),
    );exit()
    print(
        rest_line_wavelength_from_observed_line_wavelength(wavelength=4.44, redshift=3.0),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=4.44, redshift=4.0),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=4.44, redshift=5.0),
    )
    print(
        rest_line_wavelength_from_observed_line_wavelength(wavelength=2.00, redshift=3.0),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=2.00, redshift=4.0),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=2.00, redshift=5.0),
    )
    exit()

    # frequency = observed_line_frequency_from_rest_line_frequency(
    #     frequency=1900.536900,
    #     redshift=3.63 # G09v1.97
    # )
    # print(frequency);exit()

    # print(
    #     rest_line_wavelength_from_observed_line_wavelength(wavelength=3.0, redshift=3.760) * au.mm.to(au.micron),
    # );exit()

    print(
        rest_line_wavelength_from_observed_line_wavelength(wavelength=2.0, redshift=3.760) * au.micron.to(au.nm),
        #rest_line_wavelength_from_observed_line_wavelength(wavelength=2.0, redshift=2.136) * au.micron.to(au.nm),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=4.4, redshift=3.762) * au.micron.to(au.nm),
    );exit()

    # print(
    #     redshift_from_rest_and_observed_frequecies(
    #         rest_frequency=1900.536900,
    #         #observed_frequency=363.932781  # NOTE: SPT-0418 (companion)
    #         observed_frequency=363.755614 # NOTE: SPT-0418 (primary)
    #     )
    # )
    # exit()
    print(
        'z = 2:',
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.25, redshift=2.) * au.micron.to(au.nm),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.55, redshift=2.) * au.micron.to(au.nm),
    );exit()
    print(
        'z = 2:',
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.25, redshift=2.) * au.micron.to(au.nm),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.55, redshift=2.) * au.micron.to(au.nm),
    )
    print(
        'z = 3:',
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.25, redshift=3.) * au.micron.to(au.nm),
        rest_line_wavelength_from_observed_line_wavelength(wavelength=1.55, redshift=3.) * au.micron.to(au.nm),
    )
    exit()

    print(
        rest_line_wavelength_from_observed_line_wavelength(wavelength=351, redshift=4.2248),
        #rest_line_wavelength_from_observed_line_wavelength(wavelength=2.0, redshift=3.7602)
    );exit()

    # NOTE: CII
    #redshift = 4.70030 # J1341 -> spw = 23
    #redshift = 4.6915 # BR1202-0725 -> spw =
    redshift = 3.399 # SPT-0532
    CII_frequency = 1900.536900
    frequency = observed_line_frequency_from_rest_line_frequency(
        frequency=CII_frequency,
        redshift=redshift
    )
    print(frequency);exit()







    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X35/product/member.uid___A001_X894_X35.SPT-0532_sci.spw25.cube.I.pbcor.fits"
    # filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X35/product/member.uid___A001_X894_X35.SPT-0532_sci.spw27.cube.I.pbcor.fits"

    filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2f/product/member.uid___A001_X894_X2f.SPT-0418_sci.spw25.cube.I.pbcor.fits"
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2f/product/member.uid___A001_X894_X2f.SPT-0418_sci.spw27.cube.I.pbcor.fits"

    cube = fits.getdata(filename=filename)
    cube = np.squeeze(cube)

    # redshift = 2.7817
    # transition = "9-8"
    # frequency_0 = observed_CO_frequency(
    #     redshift=redshift, transition=transition
    # )
    #
    # velocities = get_velocities_from_fits(
    #     filename=filename, frequency_0=frequency_0 * au.GHz.to(au.Hz)
    # )
    #
    # moment_1_from = moment_1(cube=cube, velocities=velocities, f_min=8.0 * 10.0**-4.0)

    moment_0_from = moment_0(cube=cube, velocities=np.linspace(0.0, 1.0, cube.shape[0])) #, f_min=100.0 * 10.0**-4.0

    plt.figure()
    plt.imshow(moment_0_from, cmap="jet")
    plt.show()

    # filename = "/Users/ccbh87/Desktop/ALMA_data/2019.1.00663.S/science_goal.uid___A001_X146a_X85/group.uid___A001_X146a_X86/member.uid___A001_X146a_X87/product/member.uid___A001_X146a_X87._J053816-5030.8__sci.spw17.cube.I.pbcor.fits"
    # cube = fits.getdata(filename=filename)
    # cube = np.squeeze(cube)
    #
    # redshift = 2.7817
    # transition = "9-8"
    # frequency_0 = observed_CO_frequency(
    #     redshift=redshift, transition=transition
    # )
    #
    # velocities = get_velocities_from_fits(
    #     filename=filename, frequency_0=frequency_0 * au.GHz.to(au.Hz)
    # )
    #
    # moment_1_from = moment_1(cube=cube, velocities=velocities, f_min=8.0 * 10.0**-4.0)
    #
    # plt.figure()
    # plt.imshow(moment_1_from, vmin=200, vmax=700, cmap="jet")
    # plt.show()

    exit()


    def ALESS_moments(
        source="ALESS_017.1"
    ):

        if source=="ALESS_017.1":
            directory = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X127/group.uid___A001_X1288_X128/member.uid___A001_X1288_X129/imaging/ALESS_017.1"
            filename = "{}/ALESS_017.1_spw_17.clean.cube.image.pbcor.fits".format(directory)
            outpout_filename = "{}/ALESS_017.1_spw_17_moment_0.clean.cube.image.pbcor.fits".format(directory)
            hdu = fits.open(filename)
            cube = np.squeeze(hdu[0].data)
            header = hdu[0].header;
            frequencies = fits_utils.get_frequencies_from_header(
                header=header
            )
            frequency_0 = observed_line_frequency_from_rest_line_frequency(
                frequency=rest_frame_CO_frequencies(transition="2-1"),
                redshift=1.5382506587318503
            )
            velocities = convert_frequencies_to_velocities(
                frequencies=frequencies,
                frequency_0=frequency_0 * au.GHz.to(au.Hz)
            )



            zmin = 58
            zmax = 66
            z_mask = mask_utils.z_mask_from_zmin_and_zmax(
                shape=cube.shape[0],
                zmin=zmin,
                zmax=zmax
            )

            cube[z_mask] = 0.0

            # axes = plot_utils.plot_cube(
            #     cube=cube,
            #     ncols=12,
            #     vmin=-5.0 * 10**-4.0,
            #     vmax=0.00125,
            # )
            # for ax in np.ndarray.flatten(axes):
            #     ax.set_xlim(256 - 50, 256 + 50)
            #     ax.set_ylim(256 - 50, 256 + 50)
            # plt.show()
            # exit()

            moment_0_from_cube = moment_0(
                cube=cube,
                velocities=velocities,
                f_min=0.0,
                axis=0
            )

            fits.writeto(
                outpout_filename,
                data=moment_0_from_cube,
                header=fits_utils.extract_keys_from_header_for_2d(
                    header=header
                )
            )

            # plt.figure()
            # plt.imshow(moment_0_from_cube)
            # plt.show()

        if source=="049.1":


            filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/imaging/ALESS49_spw_1.clean.cube.image.pbcor.fits"
            cube = np.squeeze(fits.getdata(filename))
            # plot_utils.plot_cube(cube=cube, ncols=12)
            # plt.show()

            z_mask = mask_utils.z_mask_from_zmin_and_zmax(
                shape=cube.shape[0], zmin=51, zmax=67
            )
            # cube[z_mask, ...] = np.nan
            # plot_utils.plot_cube(cube=cube, ncols=12)
            # plt.show()
            # exit()

            header = fits.getheader(filename=filename)
            frequencies = fits_utils.get_frequencies_from_header(
                header=header
            )

            frequencies_interp = interpolate.interp1d(
                np.arange(len(frequencies)), frequencies
            )
            z_centre = 59
            velocities = convert_frequencies_to_velocities(
                frequencies=frequencies,
                frequency_0=frequencies_interp(z_centre)
            )

            # frequency_0 = observed_line_frequency_from_rest_line_frequency(
            #     frequency=rest_frame_CO_frequencies(transition="3-2"),
            #     redshift=2.9451
            # )
            # velocities = convert_frequencies_to_velocities(
            #     frequencies=frequencies,
            #     frequency_0=frequency_0 * au.GHz.to(au.Hz)
            # )


            # noise_from_cube(
            #     cube=cube,
            #     figure_1_for_debugging=True
            # )

            #sigma = 8.0 * 10**-5.

            # moment_0_from_cube = moment_0(
            #     cube=cube,
            #     velocities=velocities,
            #     f_min=3.0 * 10**-4.0,
            #     axis=0
            # )
            moment_1_from_cube = moment_1(
                cube=cube[~z_mask],
                velocities=velocities[~z_mask],
                f_min=3.0 * 10**-4.0,
                axis=0
            )
            plt.figure()
            plt.imshow(
                moment_1_from_cube,
                cmap="jet",
                #vmin=-250,
                #vmax=125
            )
            plt.colorbar()
            plt.xlim(300, 550)
            plt.ylim(175, 425)
            plt.show()

            # xy_mask = mask_utils.circular_mask(
            #     shape=cube.shape[1:],
            #     centre=(290, 425),
            #     radius=100.,
            #     invert=True
            # )
            #
            # cube_masked = copy.deepcopy(cube)
            # cube_masked[:, xy_mask] = np.nan
            # # plot_utils.plot_cube(
            # #     cube=cube_masked, ncols=12
            # # )
            # # plt.show();exit()
            #
            # spectrum_from_cube_masked = spectral_utils.spectrum_from_cube_and_mask(
            #     cube=cube_masked
            # )
            # plt.figure()
            # plt.step(
            #     np.arange(len(spectrum_from_cube_masked)),
            #     spectrum_from_cube_masked
            # )
            # plt.show()
            exit()

            filename_data = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/cube_data__ALESS49.fits"
            filename_model = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata/cube_model__ALESS49.fits"
            cube = fits.getdata(filename=filename_data)
            cube_model = fits.getdata(filename=filename_model)

            xy_mask = mask_utils.circular_mask(
                shape=cube.shape[1:],
                centre=(85, 112),
                radius=15.,
                invert=True
            )

            cube[:, xy_mask] = np.nan
            cube_model[:, xy_mask] = np.nan

            plot_utils.plot_cube(cube, ncols=6)
            #plt.show()

            spectrum_from_cube = spectral_utils.spectrum_from_cube_and_mask(
                cube=cube
            )
            spectrum_from_cube_model = spectral_utils.spectrum_from_cube_and_mask(
                cube=cube_model
            )
            plt.figure()
            plt.plot(spectrum_from_cube)
            plt.plot(spectrum_from_cube_model)
            plt.show()
            exit()

        if source == "087.1":

            filename_data = "/Volumes/MyPassport_red/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa9/group.uid___A001_X87a_Xaa/member.uid___A001_X87a_Xab/product/member.uid___A001_X87a_Xab.ALESS87_CO.clean.image.pbcor.fits"
            cube = np.squeeze(
                fits.getdata(filename=filename_data)
            )

            header = fits.getheader(filename=filename_data)
            frequencies = fits_utils.get_frequencies_from_header(
                header=header
            )

            frequencies_interp = interpolate.interp1d(
                np.arange(len(frequencies)), frequencies
            )
            z_centre = 11
            velocities = convert_frequencies_to_velocities(
                frequencies=frequencies,
                frequency_0=frequencies_interp(z_centre)
            )

            xy_mask_init_centre = (230, 220)
            xy_mask_init_radius = 50
            xy_mask_init = mask_utils.circular_mask(
                shape=cube.shape[1:],
                centre=xy_mask_init_centre,
                radius=xy_mask_init_radius,
                invert=True
            )

            cube[:, xy_mask_init] = np.nan

            z_mask = mask_utils.z_mask_from_zmin_and_zmax(
                shape=cube.shape[0],
                zmin=8,
                zmax=13,
            )

            # noise_from_cube(
            #     cube=cube,
            #     figure_1_for_debugging=True
            # )
            # exit()
            moment_0_from_cube = moment_0(
                cube=cube,
                velocities=velocities,
                f_min=0.0,
                axis=0
            )
            moment_1_from_cube = moment_1(
                cube=cube[~z_mask],
                velocities=velocities[~z_mask],
                f_min=3.0 * 10**-4.0,
                axis=0
            )
            plt.figure()
            plt.imshow(
                moment_1_from_cube,
                cmap="jet",
                #vmin=-250,
                #vmax=125
            )
            plt.xlim(
                xy_mask_init_centre[1] - xy_mask_init_radius,
                xy_mask_init_centre[1] + xy_mask_init_radius,
            )
            plt.ylim(
                xy_mask_init_centre[0] - xy_mask_init_radius,
                xy_mask_init_centre[0] + xy_mask_init_radius,
            )
            plt.show()
            exit()

            axes = plot_utils.plot_cube(cube=cube, ncols=10)
            for ax in np.ndarray.flatten(axes):

                ax.set_xlim(
                    xy_mask_init_centre[1] - xy_mask_init_radius,
                    xy_mask_init_centre[1] + xy_mask_init_radius,
                )
                ax.set_ylim(
                    xy_mask_init_centre[0] - xy_mask_init_radius,
                    xy_mask_init_centre[0] + xy_mask_init_radius,
                )
            plt.show()

    ALESS_moments(
        source="049.1"
    )
    exit()


    """
    cube = fits.getdata(filename="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/dirty_cube_ALESS_112.1__Npix_128__PixScale_0.05.fits")
    velocities = fits.getdata(filename="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/velocities_ALESS_112.1.fits")
    xy_mask = mask_utils.circular_mask(shape=cube.shape[1:], centre=(64, 64), radius=25)
    z_mask = mask_utils.z_mask_from_zmin_and_zmax(shape=cube.shape[0], zmin=82, zmax=105)
    cube[:, ~xy_mask] = 0.0
    cube[z_mask, :] = 0.0
    # plot_utils.plot_cube(cube=cube, ncols=12)
    # plt.show()

    f_min=1.25 * 10**3.
    moment_1_from_cube = moment_1(
        cube=cube,
        velocities=velocities,
        f_min=f_min,
    )
    moment_2_from_cube = moment_2(
        cube=cube,
        velocities=velocities,
        f_min=f_min,
    )
    vmin=0.0
    vmax=250.
    plt.figure()
    plt.imshow(moment_1_from_cube, cmap="jet")
    plt.colorbar()
    plt.figure()
    plt.imshow(moment_2_from_cube, cmap="jet")
    plt.colorbar()
    plt.show()
    exit()
    """

    source = "101.1"
    filename_i = "/Users/ccbh87/Desktop/ALMA_data/imaging_from/ALESS_101.1/ALESS_101.1_spw_23.clean.cube.image.pbcor.fits"
    filename_j = "/Users/ccbh87/Desktop/ALMA_data/imaging_from/ALESS_101.1/ALESS_101.1_spw_23_from_model.clean.cube.image.pbcor.fits"
    z_centre = 17
    # source = "112.1"
    # filename_i = "/Users/ccbh87/Desktop/ALMA_data/imaging_from/ALESS_112.1__imsize_512/ALESS_112.1_spw_23.clean.cube.image.pbcor.fits"
    # filename_j = "/Users/ccbh87/Desktop/ALMA_data/imaging_from/ALESS_112.1__imsize_512/ALESS_112.1_spw_23_from_model.clean.cube.image.pbcor.fits"
    # z_centre = 92

    frequencies = fits_utils.get_frequencies_from_fits(
        filename=filename_i,
    )
    frequencies_interp = interpolate.interp1d(np.arange(len(frequencies)), frequencies)

    frequency_0 = frequencies_interp(z_centre)

    velocities = convert_frequencies_to_velocities(
        frequencies=frequencies,
        frequency_0=frequency_0
    )

    cube_i = np.squeeze(fits.getdata(filename=filename_i))
    cube_j = np.squeeze(fits.getdata(filename=filename_j))


    # noise_from_cube(
    #     cube=cube_i,
    #     figure_1_for_debugging=True
    # )
    # exit()

    if source == "101.1":
        z_mask = mask_utils.z_mask_from_zmin_and_zmax(
            shape=cube_i.shape[0],
            zmin=10,
            zmax=25,
        )
        radius_main = 30
        radius_small = 10
    if source == "112.1":
        z_mask = mask_utils.z_mask_from_zmin_and_zmax(
            shape=cube_i.shape[0],
            zmin=80,
            zmax=105,
        )
        radius_main = 15
        radius_small = 10
    cube_i_copy = copy.deepcopy(cube_i)
    cube_i_copy = cube_i_copy[~z_mask]
    #cube_i_copy[z_mask] = np.nan
    #plot_utils.plot_cube(cube=cube_i_copy, ncols=12);plt.show();exit()

    if source == "101.1":
        xy_mask_1_centre = (262, 240)
        xy_mask_2_centre = (252, 256)
        xy_mask_3_centre = (241, 271)
        xy_mask_centre = (252, 256)
    if source == "112.1":
        xy_mask_1_centre = (256, 246)
        xy_mask_2_centre = (256, 256)
        xy_mask_3_centre = (256, 266)
        xy_mask_centre = (256, 256)
    xy_mask_1 = mask_utils.circular_mask(
        shape=cube_i.shape[1:],
        centre=xy_mask_1_centre,
        radius=radius_small,
        invert=True
    )
    xy_mask_2 = mask_utils.circular_mask(
        shape=cube_i.shape[1:],
        centre=xy_mask_2_centre,
        radius=radius_small,
        invert=True
    )
    xy_mask_3 = mask_utils.circular_mask(
        shape=cube_i.shape[1:],
        centre=xy_mask_3_centre,
        radius=radius_small,
        invert=True
    )

    xy_mask = mask_utils.circular_mask(
        shape=cube_i.shape[1:],
        centre=xy_mask_centre,
        radius=radius_main,
        invert=True
    )

    moment_0_from = moment_0(
        cube=cube_i_copy,
        velocities=velocities[~z_mask],
        f_min=0.0,
        #axis=0,
        #figure_1_for_debugging=False
    )

    axes = plot_utils.plot_cube(
        cube=cube_i_copy,
        ncols=5,
    )
    x_text = 215
    y_text = 285
    for (ax, label) in zip(
        np.ndarray.flatten(axes), velocities[~z_mask]
    ):
        ax.set_xlim(205, 305)
        ax.set_ylim(200, 300)
        # ax.contour(
        #     moment_0_from,
        #     levels=[0.75 * fraction
        #         for fraction in np.linspace(0.25, 1.0, 10)
        #     ],
        #     colors="black",
        #     alpha=0.5
        # )

        ax.text(
            x_text,
            y_text,
            "{0:.1f} km / s".format(
                label
            ),
            color="black",
            weight="bold"
        )

        circle_for_xy_mask = plt.Circle(
            xy_mask_centre[::-1], radius_main, facecolor="None", edgecolor='grey', linewidth=2,
        )
        ax.add_patch(circle_for_xy_mask)

        for i, centre in enumerate([
            xy_mask_1_centre,
            xy_mask_2_centre,
            xy_mask_3_centre,
        ]):
            circle_for_xy_mask = plt.Circle(
                centre[::-1], radius_small, facecolor="None", edgecolor='black'
            )
            ax.add_patch(circle_for_xy_mask)

    # plt.show()
    # exit()

    # NOTE: FIGURE -> ...
    # cube_i_copy[:, xy_mask] = np.nan
    #
    # axes = plot_utils.plot_cube(cube=cube_i_copy, ncols=5)
    # for ax in np.ndarray.flatten(axes):
    #     ax.set_xlim(205, 305)
    #     ax.set_ylim(200, 300)
    # plt.show()
    # exit()

    # NOTE: FIGURE -> ...
    # moment_0_from = moment_0(
    #     cube=cube_i_copy,
    #     velocities=velocities[~z_mask],
    #     f_min=0.0,
    #     #axis=0,
    #     #figure_1_for_debugging=False
    # )
    # moment_1_from = moment_1(
    #     cube=cube_i_copy,
    #     velocities=velocities[~z_mask],
    #     f_min=0.0002 * 3.,
    #     #axis=0,
    #     #figure_1_for_debugging=False
    # )
    # moment_1_from_copy = copy.deepcopy(moment_1_from)
    # moment_1_from[xy_mask_1] = -100000.
    # moment_1_from[xy_mask_2] = -200000.
    # moment_1_from[xy_mask_3] = -200000.
    # #moment_1_from[mask] = -200000.
    #
    # # figure, axes = plt.subplots(nrows=1, ncols=2)
    # # axes[0].imshow(moment_1_from_copy, cmap="jet", vmin=-250, vmax=250.)
    # # axes[1].imshow(moment_1_from, cmap="jet", vmin=-250, vmax=250.)
    # # for centre in [xy_mask_1_centre, xy_mask_2_centre, xy_mask_3_centre]:
    # #
    # #     circle_axes_0 = plt.Circle(centre[::-1], 10, facecolor="None", edgecolor='black')
    # #     circle_axes_1 = plt.Circle(centre[::-1], 10, facecolor="None", edgecolor='black')
    # #     axes[0].add_patch(circle_axes_0)
    # #     axes[1].add_patch(circle_axes_1)
    # figure, axes = plt.subplots(nrows=1, ncols=2)
    # im0 = axes[0].imshow(moment_0_from, cmap="jet", aspect="auto")
    # im = axes[1].imshow(moment_1_from_copy, cmap="jet", aspect="auto", vmin=-250, vmax=250.)
    #
    # for i, centre in enumerate([
    #     xy_mask_1_centre,
    #     xy_mask_2_centre,
    #     xy_mask_3_centre
    # ]):
    #     circle_for_axes_0 = plt.Circle(centre[::-1], 10, facecolor="None", edgecolor='black')
    #     circle_for_axes_1 = plt.Circle(centre[::-1], 10, facecolor="None", edgecolor='black')
    #     axes[0].add_patch(circle_for_axes_0)
    #     axes[1].add_patch(circle_for_axes_1)
    #     axes[1].text(centre[1], centre[0], "{}".format(i + 1), fontsize=15)
    # matplotlib_utils.add_colorbar_to_axes(
    #     figure=figure,
    #     im=im,
    #     axes=axes[1],
    # )
    #
    # circle_main_axes_0 = plt.Circle(xy_mask_centre[::-1], 30, facecolor="None", edgecolor='grey', linewidth=2,)
    # circle_main_axes_1 = plt.Circle(xy_mask_centre[::-1], 30, facecolor="None", edgecolor='grey', linewidth=2,)
    # axes[0].add_patch(circle_main_axes_0)
    # axes[1].add_patch(circle_main_axes_1)
    #
    # axes[0].set_xlim(200 + 5, 300 + 5)
    # axes[0].set_ylim(200, 300)
    # axes[0].set_xticks([])
    # axes[0].set_yticks([])
    # axes[1].set_xlim(200 + 5, 300 + 5)
    # axes[1].set_ylim(200, 300)
    # axes[1].set_xticks([])
    # axes[1].set_yticks([])
    # plt.show()
    # exit()

    plt.figure()
    for i, mask in enumerate([
        xy_mask_1,
        xy_mask_2,
        xy_mask_3,
    ]):
        cube_i_copy = copy.deepcopy(cube_i)
        cube_i_copy[:, mask] = np.nan
        spectrum_from_cube_i_temp = spectrum_from_cube_and_mask(
            cube=cube_i_copy
        )
        plt.step(
            velocities,#np.arange(len(spectrum_from_cube_i_temp)),
            spectrum_from_cube_i_temp,# / np.max(spectrum_from_cube_i_temp),
            linewidth=2,
            label="{}".format(i + 1)
        )




    cube_i[:, xy_mask] = np.nan
    cube_j[:, xy_mask] = np.nan

    #plot_utils.plot_cube(cube=cube_j, ncols=12);plt.show();exit()

    spectrum_from_cube_i = spectrum_from_cube_and_mask(
        cube=cube_i
    )
    spectrum_from_cube_j = spectrum_from_cube_and_mask(
        cube=cube_j
    )
    plt.step(
        velocities,#np.arange(len(spectrum_from_cube_i)),
        spectrum_from_cube_i,# / np.max(spectrum_from_cube_i),
        linewidth=2,
        color="black",
        label="data"
    )
    plt.legend()
    plt.xlim(-500.0, 500)
    plt.xlabel("velocity (km / s)", fontsize=15)
    plt.ylabel(r"$F_{\rm \nu}$ (mJy / beam)", fontsize=15)
    plt.show()
    exit()

    p = fit_spectrum_with_gaussian_x2(
        spectrum=spectrum_from_cube_i,
        p0=(1.0, 85., 2., 1.0, 95., 2.),
    )

    x_from_fit = np.linspace(0.0, len(spectrum_from_cube_i), 250)
    x_from_fit_for_residuals = np.arange(len(spectrum_from_cube_i))
    y_from_fit = fitting_utils.gaussian_x2(
        x_from_fit,
        *p
    )
    y_from_fit_for_residuals = fitting_utils.gaussian_x2(
        x_from_fit_for_residuals,
        *p
    )

    # figure, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 5))
    # axes[0].step(np.arange(len(spectrum_from_cube_i)), spectrum_from_cube_i, linewidth=2, color="black")
    #
    # axes[0].plot(x_from_fit, y_from_fit, linewidth=2, color="grey")
    #
    # residuals = spectrum_from_cube_i - spectrum_from_cube_j
    # residuals_from_fit = spectrum_from_cube_i - y_from_fit_for_residuals
    #
    # axes[0].step(np.arange(len(spectrum_from_cube_j)), spectrum_from_cube_j, linewidth=2, color="b")
    #
    # axes[1].step(x_from_fit_for_residuals, residuals_from_fit, linewidth=2, color="grey")
    # axes[1].step(x_from_fit_for_residuals, residuals, linewidth=2, color="b")
    #
    # axes[1].axhline(0.0, linestyle="--", color="black")
    #
    # xlim = (70, 110)
    # axes[0].set_xlim(xlim)
    # axes[1].set_xlim(xlim)

    plt.figure(figsize=(15, 5))
    plt.step(np.arange(len(spectrum_from_cube_i)), spectrum_from_cube_i, linewidth=2, color="black", label="data")
    plt.plot(x_from_fit, y_from_fit, linewidth=2, color="grey")
    plt.step(np.arange(len(spectrum_from_cube_j)), spectrum_from_cube_j, linewidth=2, color="b", label="model; Galpak3D")

    xlim = (60, 120)
    #plt.xlim(xlim)

    plt.xlabel("# of channel", fontsize=15)
    plt.ylabel(r"$F_{\nu}$ (mJy / beam)", fontsize=15)
    plt.legend(fontsize=15)
    plt.show()
    exit()






    # ALESS(id="ALESS_075.1")
    # exit()

    #observed_CO_frequencies(redshift=2.3049)
    # exit()

    # get_velocities_from_fits(
    #     filename="/Users/ccbh87/Desktop/ALMA_data/imaging_from/ALESS_112.1/ALESS_112.1_spw_23.clean.cube.image.pbcor.fits",
    #     frequency_0=104.35974045571149 * au.GHz.to(au.Hz)
    # )
    # exit()

    CII = 1900.536900

    ALMA_bands = {
        "1":[35, 50],
        "2":[65, 90],
        "3":[84, 116],
        "4":[125, 163],
        "5":[163, 211],
        "6":[211, 275],
        "7":[275, 373],
        "8":[385, 500],
        "9":[602, 720],
        "10":[787, 950]
    }

    CO_transition_frequencies = {
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

    CI_transition_frequencies = {
        "1-0": 492.1607,
        "2-1": 809.3435,
    }

    # redshift = 3.399
    # frequency = observed_CO_frequency(
    #     redshift=redshift, transition="6-5"
    # )
    # print(frequency);exit()

    ################################################
    """
    z_min = 2.0
    z_max = 3.0
    #z_max = 6.5

    redshift_array = np.linspace(z_min, z_max, 100)

    a = np.zeros(shape=(len(CO_transition_frequencies.keys()), len(redshift_array)))
    a_CI = np.zeros(shape=(len(CI_transition_frequencies.keys()), len(redshift_array)))

    a_CII = np.zeros(shape=(len(redshift_array)))

    for i, redshift in enumerate(redshift_array):
        for j, (transition, frequency) in enumerate(CO_transition_frequencies.items()):
            observed_line_frequency = observed_line_frequency_from_rest_line_frequency(
                frequency=frequency, redshift=redshift
            )

            a[j, i] = observed_line_frequency

        for j, (transition, frequency) in enumerate(CI_transition_frequencies.items()):
            observed_line_frequency = observed_line_frequency_from_rest_line_frequency(
                frequency=frequency, redshift=redshift
            )

            a_CI[j, i] = observed_line_frequency

        a_CII[i] = observed_line_frequency_from_rest_line_frequency(
            frequency=CII, redshift=redshift
        )

    figure, axes = plt.subplots(figsize=(18, 4))

    # transitions = list(CO_transition_frequencies.keys())
    # for i in range(a.shape[0]):
    #     if transitions[i] in ["4-3", "5-4", "6-5"]:
    #         axes.plot(a[i, :], redshift_array, label="CO ({})".format(transitions[i]))

    # transitions = list(CI_transition_frequencies.keys())
    # for i in range(a_CI.shape[0]):
    #     if transitions[i] in ["1-0"]:
    #         axes.plot(a_CI[i, :], redshift_array, label="CI ({})".format(transitions[i]))

    axes.plot(a_CII, redshift_array, color="black", label="CII")

    colors = random_utils.generate_list_of_random_colors(length_of_list=10)
    for k, (band, range) in enumerate(ALMA_bands.items()):
        f_min, f_max = range

        if band in ["4", "5", "6", "7", "8", "9", "10"]:
            axes.axvspan(f_min, f_max, alpha=0.5, color=colors[k])

            axes.text(f_min + 5, 2.0, "band {}".format(band))

    redshifts = [2.3010, 2.3049, 2.2024] #2.4024,
    for redshift in redshifts:
        plt.axhline(redshift, color="black", linestyle="--")

    plt.legend()
    axes.set_xlabel(r"$f_{\rm obs}$ (GHz)", fontsize=15)
    axes.set_ylabel("redshift", fontsize=15)
    plt.subplots_adjust(left=0.05, right=0.995, bottom=0.15)
    plt.show()

    print("OK")
    exit()
    """
    ################################################


    # source_redshifts = {
    #     "ALESS003.1":3.3749897478568363,
    #     "ALESS6.1":2.3338,
    #     "ALESS41.1":2.5460,
    #     "ALESS49.1":2.9417,
    #     "ALESS75.1":2.5450,
    #     "ALESS65.1":4.4445,
    #     "ALESS66.1":2.5542,
    #     "ALESS34.1":2.5115,
    #     "ALESS17.1":1.5397,
    #     "ALESS88.1":1.2679,
    #     "ALESS101.1":2.7999,
    #     "ALESS71.1":3.7072348210731896,
    #     "ALESS61.1":4.404619745761362,
    #     "ALESS98.1":1.3739182340970815,
    #     "ALESS31.1":3.7123788087268546,
    #     "ALESS35.1":2.973724833177655,
    #     "ALESS101.1":2.353081402886241,
    #     "J142413":4.243,
    #     "SDP.81":3.042,
    #     "ALESS035.1":2.9737,
    #     "G09v1.40":2.089,
    #     "Gal3":2.9342,
    #     "SPT0538-50":2.78
    # }
    #
    # #source = "ALESS003.1"
    # #source = "ALESS41.1"
    # # source = "ALESS49.1"
    # # source = "ALESS75.1"
    # # source = "ALESS65.1"
    # # source = "ALESS34.1"
    # # source = "ALESS17.1"
    # # source = "ALESS88.1"
    # # source = "ALESS66.1"
    # # source = "ALESS101.1"
    # # source = "ALESS6.1"
    # #source = "ALESS71.1"
    # #source = "ALESS61.1"
    # #source = "ALESS98.1"
    # #source = "ALESS31.1"
    # #source = "ALESS101.1"
    # #source = "ALESS35.1"
    # #source = "J142413"
    # #source = "SDP.81"
    # #source = "ALESS035.1"
    # #source = "G09v1.40"
    # source = "Gal3"
    # source = "SPT0538-50"
    #
    # observed_CO_frequencies(
    #     redshift=source_redshifts[source]
    # )
    #
    # observed_H2O_frequencies(
    #     redshift=source_redshifts[source]
    # )
    #
    # observed_C_frequencies(
    #     redshift=source_redshifts[source]
    # )
    #
    # # frequency = observed_CO_frequency(
    # #     redshift=source_redshifts[source], transition="3-2"
    # # )



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

    """
    #filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/product/member.uid___A001_X87a_Xa7.ALESS71_COJ4-3.clean.image.pbcor.fits"
    filename = "/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging/ALESS71_spw_0.clean.cube.image.pbcor.fits"
    filename = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/ALESS71_plotter_lite.fits"
    cube = np.squeeze(
        a=fits.getdata(filename=filename)
    )



    frequencies = fits_utils.get_frequencies_from_fits(filename=filename)

    velocities = convert_frequencies_to_velocities(
        frequencies=frequencies * au.Hz.to(au.GHz),
        frequency_0=observed_line_frequency_from_rest_line_frequency(
            frequency=CO_transition_frequencies["4-3"],
            redshift=3.6967
        )
    )

    zmin = 40
    zmax = 58

    #zmin = 8
    #zmax = 120

    cube[:zmin] = np.zeros(shape=cube.shape[1:])
    cube[zmax:] = np.zeros(shape=cube.shape[1:])

    moment_0_from_cube = moment_0(cube=cube, velocities=velocities, f_min=0.0)
    # plt.figure()
    # plt.imshow(moment_0_from_cube, cmap="jet")
    # # plt.xlim((600, 1000))
    # # plt.ylim((0, 400))
    # plt.show()
    fits.writeto("./ALESS71_moment_0.fits", data=moment_0_from_cube, header=fits.getheader(filename=filename), overwrite=True)
    exit()
    """

    """
    filename = "/Users/ccbh87/Desktop/ALMA_data/2017.1.01677.S/science_goal.uid___A001_X1284_X207e/group.uid___A001_X1284_X207f/member.uid___A001_X1284_X2080/product/member.uid___A001_X1284_X2080.Gal3_sci.spw25.cube.I.pbcor.fits"
    cube = fits.getdata(filename=filename)
    cube = np.squeeze(cube)
    # print(cube.shape);exit()

    zmin = 80
    zmax = 130

    N = 25
    dx = 5
    dy = 5

    shape = cube.shape

    cube = cube[
        zmin:zmax,
        int(shape[1] / 2.0 - N + dy):int(shape[1] / 2.0 + N + dy),
        int(shape[2] / 2.0 - N + dx):int(shape[2] / 2.0 + N + dx)
    ]



    frequencies = fits_utils.get_frequencies_from_fits(filename=filename)

    velocities = convert_frequencies_to_velocities(
        frequencies=frequencies * au.Hz.to(au.GHz),
        frequency_0=observed_line_frequency_from_rest_line_frequency(
            frequency=CO_transition_frequencies["5-4"],
            redshift=2.9342
        )
    )

    velocities = velocities[zmin:zmax]

    f_min=6.0 * 10**-4.0
    vmin_moment_1 = -250
    vmax_moment_1 = 250
    vmin_moment_2 = 25
    vmax_moment_2 = 150
    moment_0_from_cube = moment_0(cube=cube, velocities=velocities, f_min=f_min)
    moment_1_from_cube = moment_1(cube=cube, velocities=velocities, f_min=f_min)
    moment_2_from_cube = moment_2(cube=cube, velocities=velocities, f_min=f_min)

    plot_utils.plot_cube(cube=cube, ncols=10, contours=moment_0_from_cube, contour_levels=np.array([0.25, 0.5, 0.75, 1.0]) * np.nanmax(moment_0_from_cube), origin="lower", show=False)
    #plt.show()
    #exit()

    figure, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
    im0 = axes[0].imshow(moment_0_from_cube, cmap="jet", origin="lower")
    im1 = axes[1].imshow(moment_1_from_cube, cmap="jet", origin="lower", vmin=vmin_moment_1, vmax=vmax_moment_1)
    im2 = axes[2].imshow(moment_2_from_cube, cmap="jet", origin="lower", vmin=vmin_moment_2, vmax=vmax_moment_2)

    matplotlib_utils.add_colorbar_to_axes(figure=figure, im=im0, axes=axes[0])
    matplotlib_utils.add_colorbar_to_axes(figure=figure, im=im1, axes=axes[1])
    matplotlib_utils.add_colorbar_to_axes(figure=figure, im=im2, axes=axes[2])
    for i in range(axes.shape[0]):
        axes[i].set_xticks([])
        axes[i].set_yticks([])
    plt.show()
    """


    """
    # # hdu = fits.open("/Users/ccbh87/Downloads/disk.alma.out02.noisy.31kmps.fits")
    # # title = "disk"
    # # f_min = 1.35 * 10**-3.0
    # hdu = fits.open("/Users/ccbh87/Downloads/merger.alma.out02.noisy.31kmps.fits")
    # title = "merger"
    # f_min = 1.35 * 10**-3.0
    #
    # frequencies = fits_utils.get_frequencies_from_header(header=hdu[0].header)
    #
    # velocities = convert_frequencies_to_velocities(
    #     frequencies=frequencies * au.Hz.to(au.GHz),
    #     frequency_0=observed_line_frequency_from_rest_line_frequency(
    #         frequency=CII,
    #         redshift=4.5
    #     )
    # )
    #
    # cube = np.squeeze(hdu[0].data)
    #
    # dz = 6
    # z_i = 0 + dz
    # z_j = 36 - dz
    #
    # cube = cube[z_i:z_j, ...]
    # velocities = velocities[z_i:z_j]
    # print(velocities)
    #
    # moment_1_from = moment_1(cube=cube, velocities=velocities, f_min=f_min, axis=0)
    #
    # figure, axes = plt.subplots()
    # vmin = -250
    # vmax = 250
    # im = axes.imshow(moment_1_from, cmap="jet", vmin=vmin, vmax=vmax)
    # x0 = 65
    # y0 = 65
    # dx = 10
    # dy = 10
    # axes.set_xlim(x0 - dx, x0 + dx)
    # axes.set_ylim(y0 - dy, y0 + dy)
    # axes.set_xticks([])
    # axes.set_yticks([])
    #
    # matplotlib_utils.add_colorbar_to_axes(figure=figure, im=im, axes=axes)
    #
    # figure.suptitle(title, fontsize=16)
    # plt.show()
    """

    # NOTE: THIS IS NOT WORKING
    # hdu = fits.open("/Users/ccbh87/Desktop/Proposals/for_Amvrosiadis/serra_00_snap_23_h1842_45_degrees_w_jy-pixel_1d2e9_lsun.fits")
    # #title = "merger"
    # #f_min = 1.35 * 10**-3.0
    #
    # frequencies = fits_utils.get_frequencies_from_header(header=hdu[0].header)
    # #print(frequencies * au.Hz.to(au.GHz));exit()
    #
    # frequency_0 = observed_line_frequency_from_rest_line_frequency(
    #     frequency=CII,
    #     redshift=4.5
    # )
    #
    # print(frequencies * au.Hz.to(au.GHz), frequency_0);exit()
    # velocities = convert_frequencies_to_velocities(
    #     frequencies=frequencies * au.Hz.to(au.GHz),
    #     frequency_0=frequency_0
    # )
    # print(velocities);exit()
    #
    # cube = np.squeeze(hdu[0].data)
    #
    # moment_1_from = moment_1(cube=cube, velocities=velocities)
    #
    # figure, axes = plt.subplots()
    # vmin = -250
    # vmax = 250
    # im = axes.imshow(moment_1_from, cmap="jet", vmin=vmin, vmax=vmax)
    # x0 = 65
    # y0 = 65
    # dx = 10
    # dy = 10
    # axes.set_xlim(x0 - dx, x0 + dx)
    # axes.set_ylim(y0 - dy, y0 + dy)
    # axes.set_xticks([])
    # axes.set_yticks([])
    #
    # matplotlib_utils.add_colorbar_to_axes(figure=figure, im=im, axes=axes)
    #
    # #figure.suptitle(title, fontsize=16)
    # plt.show()

    """
    source = "ALESS_112.1"
    filename = "/Users/ccbh87/Desktop/ALMA_data/imaging_from/{}/{}_spw_23.clean.cube.image.pbcor.fits".format(source, source)
    cube = fits.getdata(filename=filename)
    cube = np.squeeze(cube)

    redshift = 2.3135
    transition = "3-2"
    frequency_0 = observed_CO_frequency(
        redshift=redshift, transition=transition
    )

    velocities = get_velocities_from_fits(
        filename=filename, frequency_0=frequency_0 * au.GHz.to(au.Hz)
    )

    moment_0_from_dirty_cube_binning, \
    moment_1_from_dirty_cube_binning, \
    moment_2_from_dirty_cube_binning = moments_with_spectral_fitting_and_binning(
        cube=cube,
        velocities=velocities,
        p0_0=0.0001,
        SNR_min=10.0,
        debug=True
    )

    figure, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))

    axes[0].imshow(moment_0_from_dirty_cube_binning, cmap="jet")
    axes[1].imshow(moment_1_from_dirty_cube_binning, cmap="jet")
    axes[2].imshow(moment_2_from_dirty_cube_binning, cmap="jet")
    plt.show()
    exit()
    """
