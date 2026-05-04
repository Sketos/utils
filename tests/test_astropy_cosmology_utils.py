from astropy import units as au

import astropy_cosmology_utils


def test_FlatLambdaCDM_preserves_parameters():
    cosmo = astropy_cosmology_utils.FlatLambdaCDM(H0=67.7, Om0=0.31, Tcmb0=2.73)

    assert float(cosmo.H0.value) == 67.7
    assert cosmo.Om0 == 0.31


def test_kpc_proper_per_arcsec_is_positive():
    value = astropy_cosmology_utils.kpc_proper_per_arcsec(z=1.0)

    assert value > 0.0


def test_distance_helpers_return_positive_quantities():
    assert astropy_cosmology_utils.luminosity_distance(z=1.0).value > 0.0
    assert astropy_cosmology_utils.angular_diameter_distance(z=1.0).value > 0.0
    assert (
        astropy_cosmology_utils.angular_diameter_distance_between_z1_and_z2(
            z1=0.5,
            z2=1.0,
        ).value
        > 0.0
    )


def test_time_helpers_return_positive_quantities():
    assert astropy_cosmology_utils.lookback_time(z=1.0).value > 0.0
    assert astropy_cosmology_utils.age(z=1.0).value > 0.0


def test_redshift_from_distance_is_positive():
    z = astropy_cosmology_utils.redshift_from_distance(distance=100.0 * au.Mpc)

    assert z.value > 0.0
