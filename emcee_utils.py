"""Utilities for running and summarizing emcee samplers."""

import importlib
from multiprocessing import Pool
from pathlib import Path
import tempfile
import numpy as np


def _import_emcee():
    """Import emcee lazily so non-sampler helpers remain usable without it."""
    try:
        return importlib.import_module("emcee")
    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(
            "emcee is required for sampler and backend operations in emcee_utils."
        ) from error


def flatten_chain(
    chain,
):
    """Flatten a 3D emcee chain into a 2D sample array."""
    if chain.ndim == 2:
        return chain
    if chain.ndim == 3:
        return chain.reshape(-1, chain.shape[-1])
    raise ValueError("Expected a 2D or 3D chain array.")


def parameter_percentiles(
    chain,
    percentiles=(16, 50, 84),
):
    """Return requested percentiles for each parameter in a chain."""
    chain_flattened = flatten_chain(chain)
    return np.percentile(chain_flattened, percentiles, axis=0).T


def parameters_from(
    chain,
):
    """Return the 50th-percentile value for each parameter."""
    return parameter_percentiles(chain)[:, 1]


def parameters_and_errors_from(
    chain,
):
    """Return median values and a symmetric max-error estimate for each parameter."""
    summary = parameter_percentiles(chain)
    parameters = summary[:, 1]
    lower_errors = parameters - summary[:, 0]
    upper_errors = summary[:, 2] - parameters
    parameters_errors = np.maximum(lower_errors, upper_errors)
    return parameters, parameters_errors


def results(
    samples_flattened,
):
    """Compatibility wrapper returning median values and symmetric errors."""
    return parameters_and_errors_from(samples_flattened)


def get_best_fit_parameters_from_chain_as_50th_percentile(
    chain,
):
    """Compatibility wrapper returning the median of each parameter."""
    return parameters_from(chain)


def filter_chain(
    chain,
    parameter_indexes,
    values_min,
    values_max,
):
    """Return a walker mask for samples that stay inside parameter bounds."""
    walker_mask = np.ones(chain.shape[1], dtype=bool)

    for parameter_index, value_min, value_max in zip(
        parameter_indexes,
        values_min,
        values_max,
    ):
        for step_index in range(chain.shape[0]):
            step_mask = np.logical_and(
                chain[step_index, :, parameter_index] > value_min,
                chain[step_index, :, parameter_index] < value_max,
            )
            walker_mask &= step_mask

    return walker_mask


def get_random_state_from_limits(
    limits,
    rng=None,
):
    """Sample one parameter vector uniformly within the provided limits."""
    rng = np.random.default_rng() if rng is None else rng
    return limits[:, 0] + (limits[:, 1] - limits[:, 0]) * rng.random(
        limits.shape[0]
    )


def check_values(
    values,
    limits,
):
    """Validate that parameter values lie strictly within the provided limits."""
    values = np.asarray(values)
    limits = np.asarray(limits)

    if limits.shape[0] != len(values):
        raise ValueError("The number of values must match the number of limits.")

    conditions = np.logical_and(values > limits[:, 0], values < limits[:, 1])
    if not np.all(conditions):
        raise ValueError("Some values lie outside the provided limits.")


def log_prior_conditions(
    values,
    values_min,
    values_max,
):
    """Return a boolean mask describing whether values lie inside prior bounds."""
    values = np.asarray(values)
    return np.logical_and(values > values_min, values < values_max)


def initialize_state(
    ndim,
    nwalkers,
    limits,
    p0=None,
    eps=1e-5,
    rng=None,
):
    """Initialize walker positions either uniformly in bounds or near `p0`."""
    rng = np.random.default_rng() if rng is None else rng
    limits = np.asarray(limits)

    if p0 is None:
        return rng.uniform(
            low=limits[:, 0],
            high=limits[:, 1],
            size=(nwalkers, ndim),
        )

    p0 = np.asarray(p0)
    return p0 + eps * rng.standard_normal(
        size=(nwalkers, ndim)
    )


def initialize_state_from_p0(
    p0,
    ndim,
    nwalkers,
    limits,
    eps=1e-5,
    rng=None,
):
    """Initialize walkers near `p0` while clipping out-of-bounds values back to `p0`."""
    initial_state = initialize_state(
        ndim=ndim,
        nwalkers=nwalkers,
        limits=limits,
        p0=p0,
        eps=eps,
        rng=rng,
    )

    p0 = np.asarray(p0)
    limits = np.asarray(limits)
    below_min = initial_state < limits[:, 0]
    above_max = initial_state > limits[:, 1]
    out_of_bounds = np.logical_or(below_min, above_max)

    if np.any(out_of_bounds):
        initial_state[out_of_bounds] = np.broadcast_to(
            p0,
            initial_state.shape,
        )[out_of_bounds]

    return initial_state


class Dataset:
    """Simple container for x/y data and uncertainties used by toy examples."""

    def __init__(
        self,
        x,
        y,
        y_error,
    ):
        self.x = x
        self.y = y
        self.y_error = y_error


class EmceeWrapper:
    """Small convenience wrapper around an `emcee.EnsembleSampler` run."""

    def __init__(
        self,
        dataset,
        log_likelihood_func,
        limits,
        p0=None,
        nwalkers=100,
        backend_filename="backend.h5",
        parallization=False,
        eps=1e-3,
        rng=None,
    ):
        self.dataset = dataset
        self.log_likelihood_func = log_likelihood_func
        self.limits = np.asarray(limits)

        if self.limits.ndim != 2 or self.limits.shape[1] != 2:
            raise ValueError("`limits` must have shape (ndim, 2).")

        self.par_min = self.limits[:, 0]
        self.par_max = self.limits[:, 1]
        self.ndim = self.limits.shape[0]
        self.nwalkers = nwalkers
        self.parallization = parallization
        self.eps = eps
        self.rng = np.random.default_rng() if rng is None else rng

        if self.parallization not in [False, None]:
            raise NotImplementedError(
                "Only serial and multiprocessing modes are supported."
            )

        emcee = _import_emcee()
        self.backend = emcee.backends.HDFBackend(filename=backend_filename)
        backend_path = Path(backend_filename)
        if backend_path.exists():
            self.previous_nsteps = self.backend.iteration
        else:
            self.previous_nsteps = 0

        if self.previous_nsteps > 0:
            self.initial_state = self.backend.get_last_sample()
        else:
            self.initial_state = self._create_initial_state(p0=p0)
            self.check_state(
                state=np.asarray(self.initial_state),
                par_min=self.par_min,
                par_max=self.par_max,
            )
            self.backend.reset(self.nwalkers, self.ndim)

    def _create_initial_state(
        self,
        p0=None,
    ):
        """Create an initial walker state, preferring a tight ball around `p0`."""
        if p0 is not None:
            return initialize_state_from_p0(
                p0=p0,
                ndim=self.ndim,
                nwalkers=self.nwalkers,
                limits=self.limits,
                eps=self.eps,
                rng=self.rng,
            )

        initial_state = initialize_state(
            ndim=self.ndim,
            nwalkers=self.nwalkers,
            limits=self.limits,
            eps=self.eps,
            rng=self.rng,
        )

        log_likelihood_values = np.array(
            [self.log_likelihood(theta=state) for state in initial_state]
        )
        best_state = initial_state[np.argmax(log_likelihood_values)]

        return initialize_state_from_p0(
            p0=best_state,
            ndim=self.ndim,
            nwalkers=self.nwalkers,
            limits=self.limits,
            eps=self.eps,
            rng=self.rng,
        )

    @staticmethod
    def initialize_state(
        ndim,
        nwalkers,
        limits,
        p0=None,
        eps=1e-5,
        rng=None,
    ):
        """Compatibility wrapper around the module-level initializer."""
        return initialize_state(
            ndim=ndim,
            nwalkers=nwalkers,
            limits=limits,
            p0=p0,
            eps=eps,
            rng=rng,
        )

    @staticmethod
    def initialize_state_from_p0(
        p0,
        ndim,
        nwalkers,
        limits,
        eps=1e-5,
        rng=None,
    ):
        """Compatibility wrapper around the module-level `p0` initializer."""
        return initialize_state_from_p0(
            p0=p0,
            ndim=ndim,
            nwalkers=nwalkers,
            limits=limits,
            eps=eps,
            rng=rng,
        )

    def check_state(
        self,
        state,
        par_min,
        par_max,
    ):
        """Ensure that every walker state lies inside the prior limits."""
        state = np.asarray(state)
        for state_vector in state:
            conditions = log_prior_conditions(
                values=state_vector,
                values_min=par_min,
                values_max=par_max,
            )
            if not np.all(conditions):
                raise ValueError(
                    "Some values in the initial state are outside the limits."
                )

    def log_prior(
        self,
        theta,
    ):
        """Return a uniform log-prior inside limits and `-inf` outside them."""
        conditions = log_prior_conditions(
            values=np.asarray(theta),
            values_min=self.par_min,
            values_max=self.par_max,
        )
        return 0.0 if np.all(conditions) else -np.inf

    def log_likelihood(
        self,
        theta,
    ):
        """Evaluate the user-provided log-likelihood for one parameter vector."""
        return self.log_likelihood_func(self.dataset, theta)

    def log_probability(
        self,
        theta,
    ):
        """Return posterior log-probability as prior plus likelihood."""
        log_prior_value = self.log_prior(theta)
        if not np.isfinite(log_prior_value):
            return -np.inf
        return log_prior_value + self.log_likelihood(theta=theta)

    def run(
        self,
        nsteps,
        parallel=False,
        progress=True,
    ):
        """Run the ensemble sampler up to `nsteps` total iterations."""
        emcee = _import_emcee()
        nsteps_to_run = nsteps - self.previous_nsteps
        if nsteps_to_run <= 0:
            sampler = emcee.EnsembleSampler(
                nwalkers=self.nwalkers,
                ndim=self.ndim,
                log_prob_fn=self.log_probability,
                backend=self.backend,
            )
            return sampler

        def run_func(pool=None):
            sampler = emcee.EnsembleSampler(
                nwalkers=self.nwalkers,
                ndim=self.ndim,
                log_prob_fn=self.log_probability,
                backend=self.backend,
                pool=pool,
            )
            sampler.run_mcmc(
                initial_state=self.initial_state,
                nsteps=nsteps_to_run,
                progress=progress,
            )
            return sampler

        if parallel:
            with Pool() as pool:
                sampler = run_func(pool=pool)
        else:
            sampler = run_func()

        self.previous_nsteps = self.backend.iteration
        return sampler

    def get_chain(
        self,
        flat=False,
        thin=1,
        discard=0,
    ):
        """Proxy to the backend chain getter."""
        return self.backend.get_chain(flat=flat, thin=thin, discard=discard)

    def get_log_prob(
        self,
        flat=False,
        thin=1,
        discard=0,
    ):
        """Proxy to the backend log-probability getter."""
        return self.backend.get_log_prob(flat=flat, thin=thin, discard=discard)


# Backwards-compatible alias matching the old class name.
emcee_wrapper = EmceeWrapper


def _toy_model(
    x,
    theta,
):
    """Quadratic toy model used by internal smoke tests."""
    a, b, c = theta
    return a * x**2.0 + b * x + c


def _toy_log_likelihood_func(
    dataset,
    theta,
):
    """Gaussian log-likelihood for the quadratic toy model."""
    y_model = _toy_model(dataset.x, theta)
    variance = dataset.y_error**2.0
    return -0.5 * np.sum(
        (dataset.y - y_model) ** 2.0 / variance
        + np.log(2.0 * np.pi * variance)
    )


def test__parameter_helpers():
    """Smoke test for chain-summary helper functions."""
    chain = np.array(
        [
            [[0.0, 1.0], [2.0, 3.0]],
            [[4.0, 5.0], [6.0, 7.0]],
        ]
    )
    flattened = flatten_chain(chain)
    parameters = parameters_from(chain)
    _, parameter_errors = parameters_and_errors_from(chain)

    if flattened.shape != (4, 2):
        raise ValueError("Unexpected flattened chain shape.")
    if parameters.shape != (2,):
        raise ValueError("Unexpected parameter summary shape.")
    if not np.all(parameter_errors >= 0.0):
        raise ValueError("Parameter errors should be non-negative.")


def test__state_initialization():
    """Smoke test for the state initialization helpers."""
    rng = np.random.default_rng(1)
    limits = np.array([[-1.0, 1.0], [0.0, 2.0]])
    initial_state = initialize_state(
        ndim=2,
        nwalkers=8,
        limits=limits,
        rng=rng,
    )
    check_values(initial_state[0], limits)

    centered_state = initialize_state_from_p0(
        p0=np.array([0.1, 1.1]),
        ndim=2,
        nwalkers=8,
        limits=limits,
        eps=1e-3,
        rng=np.random.default_rng(2),
    )
    if centered_state.shape != (8, 2):
        raise ValueError("Unexpected centered state shape.")


def test__toy_sampler():
    """Smoke test for the emcee wrapper using a small quadratic toy problem."""
    _import_emcee()
    rng = np.random.default_rng(7)
    x = np.linspace(-1.0, 2.0, 20)
    theta_true = np.array([2.0, -2.5, 0.5])
    y_error = np.full_like(x, 0.1)
    y = _toy_model(x=x, theta=theta_true) + rng.normal(0.0, y_error, size=len(x))

    dataset = Dataset(x=x, y=y, y_error=y_error)
    limits = np.array([[-5.0, 5.0], [-5.0, 5.0], [-5.0, 5.0]])

    with tempfile.TemporaryDirectory() as temp_dir:
        backend_filename = str(Path(temp_dir) / "toy_backend.h5")
        wrapper = EmceeWrapper(
            dataset=dataset,
            log_likelihood_func=_toy_log_likelihood_func,
            limits=limits,
            p0=theta_true,
            nwalkers=24,
            backend_filename=backend_filename,
            eps=1e-2,
            rng=np.random.default_rng(11),
        )
        sampler = wrapper.run(nsteps=120, parallel=False, progress=False)
        chain = sampler.get_chain(discard=40, thin=2, flat=True)
        fitted = parameters_from(chain)

        if chain.shape[1] != 3:
            raise ValueError("Unexpected flattened toy chain width.")
        if not np.allclose(fitted, theta_true, atol=0.5):
            raise ValueError("Toy sampler failed to recover the true parameters.")


def run_tests():
    """Run the module's lightweight smoke tests."""
    test__parameter_helpers()
    test__state_initialization()
    test__toy_sampler()
