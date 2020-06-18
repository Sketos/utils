import numpy as np
from astropy import units, constants


# NOTE:
def compute_beam_area(bmin, bmaj):
    """Short summary.

    Parameters
    ----------
    bmin : type
        The FHWM of the minor axis of the beam.
    bmaj : type
        The FHWM of the major axis of the beam.

    Returns
    -------
    type
        Description of returned object.

    """
    beam_area = np.pi / (4.0 * np.log(2.0)) * bmin * bmaj

    return beam_area



# NOTE: Move this to fits_utils
def get_beam_from_fits(filename, ext=0):

    header = fits.getheader(
        filename=filename,
        ext=ext
    )

    # NOTE: The units of BMIN and BMAJ are in deg.
    # NOTE: Check what are the units of the beam's BMIN, BMAJ parameters in the header.
    # Assume they have the same units as CUNIT1 and CUNIT2 -> Check if they are the same
    if "BMIN" and "BMAJ" in header.keys():
        bmin = header["BMIN"] * units.deg.to(units.arcsec)
        bmaj = header["BMAJ"] * units.deg.to(units.arcsec)
    else:
        raise ValueError("...")

    return bmin, bmaj


# NOTE: Move this to fits_utils
def compute_beam_area_from_fits(filename):

    bmin, bmaj = get_beam_from_fits(
        filename=filename
    )

    return compute_beam_area(
        bmin=bmin,
        bmaj=bmaj
    )



if __name__ == "__main__":
    pass
