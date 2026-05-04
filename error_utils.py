"""Utilities for common uncertainty propagation calculations."""

import numpy as np


def error_average(
    A_error,
    A=None,
):
    """Return the uncertainty on the average of values with independent errors."""
    error = np.sqrt(np.sum(A_error**2.0)) / len(A_error)

    if A is not None:
        raise NotImplementedError() # NOTE: error = np.sqrt(error**2.0 + np.std(A) ** 2.0), this is incorrect 

    return error


def error_propagation_addition(
    A,
    A_error,
    B,
    B_error,
    a=1.0,
    b=1.0,
):
    """Propagate uncertainties for ``a * A + b * B``."""
    return np.sqrt(a**2.0 * A_error**2.0 + b**2.0 * B_error**2.0)


def error_propagation_log10(
    A,
    A_error,
):
    """Propagate uncertainties for ``log10(A)``."""
    return np.abs(
        np.divide(
            A_error,
            A * np.log(10.0),
        )
    )


def error_propagation_power(
    A,
    A_error,
    a=10.0,
    b=1.0,
):
    """Propagate uncertainties for ``a ** (b * A)``."""
    f = a ** (b * A)
    return np.abs(f) * np.abs(b * np.log(a) * A_error)


def error_propagation_quadratic(
    A,
    A_error,
    B,
    B_error,
    a,
    b,
):
    """Propagate uncertainties for ``sqrt(a * A**2 + b**2 * B**2)``."""
    f = np.sqrt(a * A**2.0 + b**2.0 * B**2.0)

    return np.sqrt(
        (a * A / f) ** 2.0 * A_error**2.0
        + (b**2.0 * B / f) ** 2.0 * B_error**2.0
    )


def error_propagation_product(
    A,
    A_error,
    B,
    B_error,
):
    """Propagate uncertainties for ``A * B``."""
    f = A * B

    return np.abs(f) * np.sqrt(
        (A_error / A) ** 2.0
        + (B_error / B) ** 2.0
    )


def error_propagation_division(
    A,
    A_error,
    B,
    B_error,
):
    """Propagate uncertainties for ``A / B``."""
    f = A / B

    return np.abs(f) * np.sqrt(
        (A_error / A) ** 2.0
        + (B_error / B) ** 2.0
    )


def monte_carlo_errors_for_linear_relation(
    x,
    a,
    a_error,
    b,
    b_error,
    n,
):
    """Draw Monte Carlo realizations for y = a * x + b."""
    a_random = np.random.normal(
        loc=a,
        scale=a_error,
        size=n,
    )
    b_random = np.random.normal(
        loc=b,
        scale=b_error,
        size=n,
    )

    return np.asarray(
        [
            a_i * x + b_i
            for a_i, b_i in zip(a_random, b_random)
        ]
    )

# def monte_carlo_errors(
#     func,
#     parameter_means,
#     parameter_errors,
#     n,
#     *func_args,
#     **func_kwargs,
# ):
#     """Draw Monte Carlo realizations for a model with uncertain parameters."""
#     parameter_samples = np.random.normal(
#         loc=parameter_means,
#         scale=parameter_errors,
#         size=(n, len(parameter_means)),
#     )
#     outputs = [
#         func(
#             *func_args,
#             *parameters,
#             **func_kwargs,
#         )
#         for parameters in parameter_samples
#     ]

#     return np.asarray(outputs)

