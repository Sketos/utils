import importlib.util
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import emcee_utils


def test_parameter_helpers():
    chain = np.array(
        [
            [[0.0, 1.0], [2.0, 3.0]],
            [[4.0, 5.0], [6.0, 7.0]],
        ]
    )

    flattened = emcee_utils.flatten_chain(chain)
    parameters = emcee_utils.parameters_from(chain)
    parameters_with_errors = emcee_utils.parameters_and_errors_from(chain)

    assert flattened.shape == (4, 2)
    assert parameters.shape == (2,)
    assert parameters_with_errors[1].shape == (2,)


def test_state_initialization_helpers():
    limits = np.array([[-1.0, 1.0], [0.0, 2.0]])
    initial_state = emcee_utils.initialize_state(
        ndim=2,
        nwalkers=8,
        limits=limits,
        rng=np.random.default_rng(1),
    )
    emcee_utils.check_values(initial_state[0], limits)

    centered_state = emcee_utils.initialize_state_from_p0(
        p0=np.array([0.1, 1.1]),
        ndim=2,
        nwalkers=8,
        limits=limits,
        eps=1e-3,
        rng=np.random.default_rng(2),
    )

    assert centered_state.shape == (8, 2)


def test_toy_emcee_example():
    if importlib.util.find_spec("emcee") is None:
        return

    emcee_utils.test__toy_sampler()


if __name__ == "__main__":
    test_parameter_helpers()
    test_state_initialization_helpers()
    test_toy_emcee_example()
    print("All emcee_utils tests passed.")
