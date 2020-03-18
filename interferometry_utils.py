import numpy as np
from astropy import units, constants


def compute_beam_area(bmin, bmaj):
    """

    Parameters
    ----------

    bmin: The FHWM of the minor axis of the beam

    bmax: The FHWM of the major axis of the beam

    """
    beam_area = np.pi / (4.0 * np.log(2.0)) * bmin * bmaj

    return beam_area


def get_header_from_fits(filename, hdu_header=0):

    hdu = fits.open(filename)
    header = hdu[hdu_header].header

    return header


def get_beam_from_fits(filename, hdu_header=0):

    header = get_header_from_fits(
        filename=filename, hdu_header=hdu_header
    )

    # NOTE: Check what are the units of the beam's BMIN, BMAJ parameters in the header.
    bmin = header["BMIN"] * units.deg.to(units.arcsec)
    bmaj = header["BMAJ"] * units.deg.to(units.arcsec)

    return bmin, bmaj


def compute_beam_area_from_fits(filename):

    bmin, bmaj = get_beam_from_fits(
        filename=filename
    )

    beam_area = compute_beam_area(
        bmin=bmin, bmaj=bmaj
    )

    return beam_area
