import numpy as np
from astropy import units, constants


def compute_beam_area(bmin, bmax):
    """
    
    Parameters
    ----------

    bmin: The FHWM of the minor axis of the beam

    bmax: The FHWM of the major axis of the beam

    """
    beam_area = np.pi / (4.0 * np.log(2.0)) * bmin * bmax

def get_beam_from_fits(filename):

    return bmin, bmax

def compute_beam_area_from_fits(filename):

    bmin, bmax = get_beam_from_fits(
        filename=filename
    )

    beam_area = compute_beam_area(
        bmin, bmax
    )

    return beam_area
