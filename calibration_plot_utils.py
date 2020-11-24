import numpy as np

import matplotlib.pyplot as plt




def plot_phase_errors(phase_errors, condition, axes=None, ylim=None):

    # NOTE: The shape of the phase errors is (n_c, n_t, n_a)

    if condition:
        phase_errors_averaged = np.average(phase_errors, axis=0)

        for i in range(phase_errors_averaged.shape[-1]):

            if axes is None:
                plt.plot(phase_errors_averaged[:, i], marker="o")
            else:
                axes.plot(phase_errors_averaged[:, i], marker="o")

            if ylim is None:
                pass
            else:
                if axes is None:
                    plt.ylim(ylim)
                else:
                    axes.set_ylim(ylim)

    if axes:
        pass
    else:
        plt.xlabel("t / dt (dt = N sec)", fontsize=15)
        plt.show()


def plot_list_of_phase_errors(list_of_phase_errors, condition, ylim=None):

    ncols = len(list_of_phase_errors)

    figure, axes = plt.subplots(nrows=1, ncols=ncols)

    for i in range(ncols):

        plot_phase_errors(
            phase_errors=list_of_phase_errors[i],
            condition=condition,
            axes=axes[i],
            ylim=ylim
        )

    plt.show()
