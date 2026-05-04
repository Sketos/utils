"""Plotting helpers for emcee chains and log-probability traces."""

import matplotlib.pyplot as plt
import numpy as np


def plot_chain(
    chain,
    log_probs=None,
    ncols=5,
    figsize=None,
    walkers=None,
    truths=None,
    limits=None,
    title=None,
    ylabels=None,
    vmin=-1000,
    show=False,
):
    """Plot walker traces for each parameter in an emcee chain."""
    n_parameters = chain.shape[-1]
    nrows = int(np.ceil(n_parameters / ncols))

    figure, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        squeeze=False,
    )
    axes_flattened = axes.ravel()
    chain_averaged = np.average(chain, axis=1)
    log_prob_max = np.max(log_probs) if log_probs is not None else 0.0

    for parameter_index, axis in enumerate(axes_flattened):
        if parameter_index >= n_parameters:
            axis.axis("off")
            continue

        if log_probs is not None:
            for walker_index in range(chain.shape[1]):
                axis.plot(
                    np.arange(chain.shape[0]),
                    chain[:, walker_index, parameter_index],
                    #c=log_probs[:, walker_index] - log_prob_max,
                    #s=2,
                    #cmap="jet",
                    #vmin=vmin,
                    #vmax=0.0,
                )
        else:
            for walker_index in range(chain.shape[1]):
                axis.plot(
                    chain[:, walker_index, parameter_index],
                    color="black",
                    alpha=0.25,
                )

        axis.plot(chain_averaged[:, parameter_index], linewidth=2, color="r", alpha=1.0)

        if truths is not None:
            axis.axhline(truths[parameter_index], linestyle="--", color="b")

        if limits is not None:
            axis.set_ylim((limits[parameter_index, 0], limits[parameter_index, 1]))
            axis.set_yticks(
                np.linspace(
                    limits[parameter_index, 0],
                    limits[parameter_index, 1],
                    3,
                )
            )

        if ylabels is not None:
            axis.set_ylabel(r"{}".format(ylabels[parameter_index]))
        else:
            axis.set_ylabel(f"param_{parameter_index}")

    if walkers is not None:
        for parameter_index, axis in enumerate(axes_flattened[:n_parameters]):
            axis.plot(chain[:, walkers, parameter_index], color="b", alpha=0.75)

    if title is not None:
        figure.suptitle(title)

    plt.subplots_adjust(wspace=0.25, left=0.05, right=0.995)

    if show:
        plt.show()

    return figure, axes


def plot_corner(
    chain,
    c=None,
    truths=None,
    labels=None,
    s=10,
    figsize=(10, 9),
    show=False,
):
    """Plot a simple lower-triangle corner-style scatter matrix."""
    n_parameters = int(chain.shape[-1] - 1)
    figure, axes = plt.subplots(
        nrows=n_parameters,
        ncols=n_parameters,
        figsize=figsize,
    )

    for i in range(n_parameters):
        for j in range(i + 1, n_parameters):
            axes[i, j].axis("off")

    sc = None
    for i in range(n_parameters):
        for j in range(0, i + 1):
            axes[i, j].plot(
                chain[:, j],
                chain[:, i + 1],
                linewidth=1,
                color="black",
                alpha=0.5,
            )
            sc = axes[i, j].scatter(
                chain[:, j],
                chain[:, i + 1],
                cmap="jet",
                c=c,
                s=s,
                alpha=0.5,
            )

            if truths is not None:
                axes[i, j].axvline(truths[j], linestyle="--", color="black")
                axes[i, j].axhline(truths[i + 1], linestyle="--", color="black")
                axes[i, j].plot(
                    [truths[j]],
                    [truths[i + 1]],
                    linestyle="None",
                    marker="o",
                    markersize=10,
                    color="black",
                )

            if i != n_parameters - 1:
                axes[i, j].set_xticks([])
            if j != 0:
                axes[i, j].set_yticks([])

    if labels is not None:
        for i in range(n_parameters):
            axes[i, 0].set_ylabel(labels[i + 1], fontsize=15)
            axes[n_parameters - 1, i].set_xlabel(labels[i], fontsize=15)

    plt.subplots_adjust(wspace=0.0, hspace=0.0)

    if sc is not None:
        cbar_ax = figure.add_axes([0.85, 0.30, 0.05, 0.6])
        figure.colorbar(sc, cax=cbar_ax)

    if show:
        plt.show()

    return figure, axes


def plot_log_prob(
    log_prob,
    truth=None,
    xlabel="# of steps",
    ylabel="-logL",
    xlim=None,
    ylim=None,
    show=False,
):
    """Plot the negative log-probability evolution for each walker."""
    figure = plt.figure(figsize=(10, 5))

    for walker_index in range(log_prob.shape[1]):
        plt.plot(
            np.arange(log_prob.shape[0]),
            -log_prob[:, walker_index],
            color="black",
            alpha=0.5,
        )

    if truth is not None:
        plt.axhline(-truth, linestyle="--", color="b")

    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    plt.yscale("log")

    if show:
        plt.show()

    return figure


def plot_list_of_log_probs(
    list_of_log_probs,
    truth=None,
    xlabel="# of steps",
    ylabel="-Likelihood",
    xlim=None,
    ylim=None,
    legends=None,
    show=False,
):
    """Plot multiple log-probability traces on the same axes."""
    figure = plt.figure(figsize=(10, 5))
    colors = ["b", "r", "g", "orange", "purple"]

    if legends is None:
        legends = [None] * len(list_of_log_probs)

    legend_conditions = np.full(shape=(len(legends),), fill_value=True)

    for j, log_prob in enumerate(list_of_log_probs):
        color = colors[j % len(colors)]
        for walker_index in range(log_prob.shape[1]):
            plt.plot(
                np.arange(log_prob.shape[0]),
                -log_prob[:, walker_index],
                color=color,
                alpha=0.5,
                label=(
                    legends[j]
                    if legends[j] is not None and legend_conditions[j]
                    else None
                ),
            )
            if legend_conditions[j]:
                legend_conditions[j] = False

    if truth is not None:
        plt.axhline(-truth, linestyle="--", color="black")

    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    plt.yscale("log")
    if any(legend is not None for legend in legends):
        plt.legend(fontsize=15)

    if show:
        plt.show()

    return figure


def corner_from_flat_samples(
    samples,
    truths=None,
    labels=None,
    bins=20,
    **kwargs,
):
    """Thin wrapper around `corner.corner` for flattened emcee samples."""
    import corner

    return corner.corner(
        samples,
        truths=truths,
        labels=labels,
        bins=bins,
        **kwargs,
    )
