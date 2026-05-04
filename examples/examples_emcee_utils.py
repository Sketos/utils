import sys
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import emcee_utils
import emcee_plot_utils


def model(
    x,
    theta,
):
    a, b, c = theta
    return a * x**2.0 + b * x + c


def log_likelihood_func(
    dataset,
    theta,
):
    y_model = model(dataset.x, theta)
    return -0.5 * np.sum(
        (dataset.y - y_model) ** 2.0 / dataset.y_error**2.0
        + np.log(2.0 * np.pi * dataset.y_error**2.0)
    )


def main():
    rng = np.random.default_rng(7)
    x = np.linspace(-1.0, 2.0, 20)
    theta_true = np.array([2.0, -2.5, 0.5])
    y_error = np.full_like(x, 0.1)
    y = model(x=x, theta=theta_true) + rng.normal(0.0, y_error, size=len(x))

    dataset = emcee_utils.Dataset(x=x, y=y, y_error=y_error)
    limits = np.array([[-5.0, 5.0], [-5.0, 5.0], [-5.0, 5.0]])

    with tempfile.TemporaryDirectory() as temp_dir:
        backend_filename = str(Path(temp_dir) / "toy_backend.h5")
        wrapper = emcee_utils.EmceeWrapper(
            dataset=dataset,
            log_likelihood_func=log_likelihood_func,
            limits=limits,
            p0=theta_true,
            nwalkers=24,
            backend_filename=backend_filename,
            eps=1e-2,
            rng=np.random.default_rng(11),
        )
        sampler = wrapper.run(nsteps=200, parallel=False, progress=True)

        chain = sampler.get_chain(discard=50, thin=2, flat=False)
        log_prob = sampler.get_log_prob(discard=50, thin=2, flat=False)
        flat_chain = sampler.get_chain(discard=50, thin=2, flat=True)
        fitted = emcee_utils.parameters_from(flat_chain)
        y_model = model(x=x, theta=fitted)

    print("true parameters     :", theta_true)
    print("recovered parameters:", fitted)

    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
    axes.errorbar(
        x,
        y,
        yerr=y_error,
        linestyle="None",
        marker="o",
        color="black",
        label="data",
    )
    axes.plot(
        x,
        model(
            x=x,
            theta=theta_true,
        ),
        color="blue",
        linestyle="--",
        label="truth",
    )
    axes.plot(
        x,
        y_model,
        color="red",
        label="best fit",
    )
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.legend()

    emcee_plot_utils.plot_chain(
        chain=chain,
        log_probs=log_prob,
        ncols=3,
        figsize=(12, 4),
        truths=theta_true,
        ylabels=["a", "b", "c"],
        title="Toy emcee chain",
    )

    emcee_plot_utils.plot_log_prob(
        log_prob=log_prob,
        xlabel="step",
        ylabel="-log probability",
    )

    emcee_plot_utils.corner_from_flat_samples(
        samples=flat_chain,
        truths=theta_true,
        labels=["a", "b", "c"],
    )

    plt.show()


if __name__ == "__main__":
    main()
