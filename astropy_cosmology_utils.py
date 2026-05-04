"""Small convenience wrappers around Astropy cosmology helpers."""

from astropy import constants, cosmology
from astropy import units as au


DEFAULT_H0 = 70.0
DEFAULT_OM0 = 0.3
DEFAULT_TCMB0 = 2.725
DEFAULT_COSMOLOGY = cosmology.FlatLambdaCDM(
    H0=DEFAULT_H0,
    Om0=DEFAULT_OM0,
    Tcmb0=DEFAULT_TCMB0,
)


def _resolve_cosmology(cosmo=None):
    """Return the provided cosmology or the module's default flat LCDM model."""
    if cosmo is None:
        return DEFAULT_COSMOLOGY
    return cosmo


def Planck15():
    """Return Astropy's built-in Planck15 cosmology."""
    return cosmology.Planck15


def FlatLambdaCDM(H0=DEFAULT_H0, Om0=DEFAULT_OM0, Tcmb0=DEFAULT_TCMB0):
    """Construct a flat LCDM cosmology with the requested parameters."""
    return cosmology.FlatLambdaCDM(H0=H0, Om0=Om0, Tcmb0=Tcmb0)


def kpc_proper_per_arcmin(z, cosmo=None):
    """Return the proper kpc-per-arcmin scale at redshift `z`."""
    return _resolve_cosmology(cosmo).kpc_proper_per_arcmin(z)


def kpc_proper_per_arcsec(
    z,
    cosmo=None,
    units=au.kpc / au.arcsec,
    return_value=True,
):
    """Return the proper kpc-per-arcsec scale at redshift `z`."""
    value = kpc_proper_per_arcmin(z=z, cosmo=cosmo).to(units)
    if return_value:
        return value.value
    return value


def luminosity_distance(z, cosmo=None, units=au.Mpc):
    """Return the luminosity distance at redshift `z`."""
    return _resolve_cosmology(cosmo).luminosity_distance(z).to(units)


def angular_diameter_distance(z, cosmo=None, units=au.Mpc):
    """Return the angular-diameter distance at redshift `z`."""
    return _resolve_cosmology(cosmo).angular_diameter_distance(z).to(units)


def angular_diameter_distance_between_z1_and_z2(
    z1,
    z2,
    cosmo=None,
    units=au.Mpc,
):
    """Return the angular-diameter distance between two redshifts."""
    return _resolve_cosmology(cosmo).angular_diameter_distance_z1z2(
        z1=z1,
        z2=z2,
    ).to(units)


def lookback_time(z, cosmo=None, units=au.Gyr):
    """Return the cosmological lookback time at redshift `z`."""
    return _resolve_cosmology(cosmo).lookback_time(z).to(units)


def age(z, cosmo=None, units=au.Gyr):
    """Return the age of the universe at redshift `z`."""
    return _resolve_cosmology(cosmo).age(z).to(units)


def redshift_from_distance(distance, cosmo=None):
    """Estimate redshift from a small-distance Hubble-law approximation."""
    resolved_cosmo = _resolve_cosmology(cosmo)
    z = distance * resolved_cosmo.H0 / constants.c
    return z.decompose()
