import numpy as np
import matplotlib.pyplot as plt

from astropy import units


def get_central_frequency(band):

    if band in [3, 4, 5, 6, 7, 8, 9, 10]:
        pass
    else:
        raise ValueError(
            "The ALMA band {} does not exist".format(band)
        )

def compute_resolution_from_wavelength_and_maximum_baseline(wavelength, maximum_baseline):
    """Short summary.

    Parameters
    ----------
    wavelength : type
        The wavelength of the observation (in units of meters).
    maximum_baseline : type
        The maximum baseline of an interferometric array (in units of meters).

    Returns
    -------
    type
        The approximate resolution of an interferometric array (in units of radians).

    """



    return wavelength / maximum_baseline


# # NOTE: In progress ...
# def uvw(HA, dec, antenna_positions):
#
#     def transformation_matrix(HA, dec):
#
#         transformation_matrix = np.zeros(
#             shape=(3, 3)
#         )
#
#         transformation_matrix[0, 0] = np.sin(HA)
#         transformation_matrix[0, 1] = np.cos(HA)
#         transformation_matrix[0, 2] = 0.0
#         transformation_matrix[1, 0] = -np.sin(dec) * np.cos(HA)
#         transformation_matrix[1, 1] = np.sin(dec) * np.sin(HA)
#         transformation_matrix[1, 2] = np.cos(dec)
#         transformation_matrix[2, 0] = np.cos(dec) * np.cos(HA)
#         transformation_matrix[2, 1] = -np.cos(dec) * np.sin(HA)
#         transformation_matrix[2, 2] = np.sin(dec)
#
#         return transformation_matrix
#
#     #HA = HA * units.deg.to(units.rad)
#     dec = dec * units.deg.to(units.rad)
#
#     for HA in np.linspace(45.0, 360.0, 100):
#
#         HA = HA * units.deg.to(units.rad)
#
#         T = transformation_matrix(HA=HA, dec=dec)
#
#
#         u, v, w = np.dot(T, antenna_positions)
#
#
#         plt.plot(u, v, linestyle="None", marker="o", color="black")
#
#     plt.show()

if __name__ == "__main__":
    pass
