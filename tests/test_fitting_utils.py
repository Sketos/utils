import sys
from pathlib import Path

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("scipy")
pytest.importorskip("astropy")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import fitting_utils


def test_fit_gaussian_from_data_estimates_image_background_noise():
    rng = np.random.default_rng(1)
    image = rng.normal(loc=0.02, scale=0.15, size=(128, 128))

    image[10:14, 10:14] += 2.0
    image[0, 0] = np.nan
    image[0, 1] = np.inf

    p = fitting_utils.fit_gaussian_from_data(
        data=image,
        bins=80,
        xmin=-0.6,
        xmax=0.6,
        density=True,
    )

    assert p is not None
    assert p[1] == pytest.approx(0.02, abs=0.02)
    assert p[2] == pytest.approx(0.15, abs=0.02)


def test_fit_gaussian_from_data_can_return_covariance_and_histogram_x():
    rng = np.random.default_rng(2)
    image = rng.normal(loc=0.0, scale=0.1, size=(32, 32))

    (p, p_cov), x = fitting_utils.fit_gaussian_from_data(
        data=image,
        bins=30,
        density=True,
        return_cov=True,
        return_x=True,
    )

    assert p.shape == (3,)
    assert p_cov.shape == (3, 3)
    assert x.shape == (30,)
