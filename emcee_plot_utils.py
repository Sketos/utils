import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner


def plot_chain(chain, log_prob=None, ncols=5, figsize=None, walkers=None, truths=None, limits=None, title=None, ylabels=None):

    # ...
    if chain.shape[-1] % ncols == 0:
        nrows = int(chain.shape[-1] / ncols)
    else:
        nrows = int(chain.shape[-1] / ncols) + 1

    chain_averaged = np.average(chain, axis=1)

    figure, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize
    )

    if log_prob is not None:
        log_prob_max = np.max(log_prob)
    else:
        log_prob_max = 0.0

    k = 0
    for i in range(nrows):
        for j in range(ncols):

            if k < chain.shape[-1]:

                # for n in range(chain.shape[0]):
                #     axes[i, j].scatter(np.tile(n, chain.shape[1]), chain[n, :, k], c=log_prob[n, :]/log_prob_max, cmap="jet")

                for n in range(chain.shape[1]):
                    axes[i, j].plot(chain[:, n, k], color="black", alpha=0.25)

                axes[i, j].plot(chain_averaged[:, k], linewidth=2, color="r", alpha=1.00)

                if truths is not None:
                    axes[i, j].axhline(truths[k], linestyle="--", color="b")

                if limits is not None:
                    axes[i, j].set_ylim((limits[k, 0], limits[k, 1]))

                    axes[i, j].set_yticks(np.linspace(limits[k, 0], limits[k, 1], 3))

                if ylabels is not None:
                    axes[i, j].set_ylabel(
                        r"{}".format(ylabels[k])
                    )
                else:
                    axes[i, j].set_ylabel("param_{}".format(k))



                k += 1
            else:
                axes[i, j].axis("off")


    if walkers is None:
        pass
    else:
        k = 0
        for i in range(nrows):
            for j in range(ncols):
                if k < chain.shape[-1]:

                    axes[i, j].plot(chain[:, walkers, k], color="b", alpha=0.75)
                    k += 1


    if title is not None:
        figure.suptitle(title)


    plt.subplots_adjust(wspace=0.25, left=0.05, right=0.995)

    plt.show()


# NOTE: Move this function to the main "plot_utils.py"
def plot_corner(chain, c, truths=None, labels=None, s=10, figsize=(10, 9)):

    #print(chain.shape)

    N = int(chain.shape[-1] - 1)

    figure, axes = plt.subplots(nrows=N, ncols=N, figsize=figsize)

    for i in range(N):
        for j in range(i + 1, N):
            axes[i, j].axis("off")


    for i in range(N):

        for j in range(0, i + 1):
            print(i, j)

            axes[i, j].plot(
                chain[:, j],
                chain[:, i+1],
                linewidth=1,
                color="black",
                alpha=0.5
            )

            sc = axes[i, j].scatter(
                chain[:, j],
                chain[:, i+1],
                cmap="jet",
                c=c,
                s=s,
                alpha=0.5
            )



            if truths:
                axes[i, j].axvline(truths[j], linestyle="--", color="black")
                axes[i, j].axhline(truths[i+1], linestyle="--", color="black")
                axes[i, j].plot([truths[j]],[truths[i+1]], linestyle="None", marker="o", markersize=10, color="black")

            if i != N-1:
                axes[i, j].set_xticks([])

            if j != 0:
                axes[i, j].set_yticks([])


    if labels:
        for i in range(N):
            axes[i, 0].set_ylabel(labels[i+1], fontsize=15)
            axes[N-1, i].set_xlabel(labels[i], fontsize=15)

    plt.subplots_adjust(wspace=0.0, hspace=0.0)

    cbar_ax = figure.add_axes([0.85, 0.30, 0.05, 0.6])
    figure.colorbar(sc, cax=cbar_ax)

    plt.show()


def filter_chain(chain, parameter_indexes, values_min, values_max):

    idx = np.full(
        shape=chain.shape[1], fill_value=True
    )
    for i, parameter_idx in enumerate(parameter_indexes):
        for j in range(chain.shape[0]):
            idx_temp = np.logical_and(
                chain[j, :, parameter_idx] > values_min[i],
                chain[j, :, parameter_idx] < values_max[i]
            )

            idx[~idx_temp] = False

    return idx


def plot_log_prob(log_prob, truth=None, xlabel="# of steps", ylabel="-logL", xlim=None, ylim=None):

    figure = plt.figure(
        figsize=(10, 5)
    )


    for i in range(log_prob.shape[1]):
        plt.plot(
            np.arange(log_prob.shape[0]),
            -log_prob[:, i],
            color="black",
            alpha=0.5
        )

    if truth:
        plt.axhline(
            -truth,
            linestyle="--",
            color="b"
        )

    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.yscale("log")
    plt.show()

def plot_list_of_log_probs(list_of_log_probs, truth=None, xlabel="# of steps", ylabel="-Likelihood", xlim=None, ylim=None, legends=None):

    figure = plt.figure(
        figsize=(10, 5)
    )

    # TODO: initialize random colors
    colors = ["b", "r"]

    legend_conditions = np.full(
        shape=(len(legends), ), fill_value=True
    )

    for j, log_prob in enumerate(list_of_log_probs):
        for i in range(log_prob.shape[1]):

            plt.plot(
                np.arange(log_prob.shape[0]),
                -log_prob[:, i],
                color=colors[j],
                alpha=0.5,
                label=legends[j] if legends is not None and legend_conditions[j] else None
            )
            if legend_conditions[j]:
                legend_conditions[j] = False

    if truth:
        plt.axhline(
            -truth,
            linestyle="--",
            color="black"
        )

    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.yscale("log")
    if legends is not None:
        plt.legend(fontsize=15)
    plt.show()


def get_best_fit_parameters_from_chain_as_50th_percentile(chain):


    if len(chain.shape) == 2:
        pass
    elif len(chain.shape) == 3:
        chain = chain.reshape(-1, chain.shape[-1])
    else:
        raise ValueError

    best_fit_parameters = np.zeros(
        shape=chain.shape[-1],
        dtype=np.float
    )
    for i in range(chain.shape[-1]):
        best_fit_parameters[i] = np.percentile(
            a=chain[:, i], q=50.0
        )

    return best_fit_parameters

if __name__ =="__main__":

    flat = False
    thin = 1
    discard = 0

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/pyBBarolo__backend_nwalkers_200_nsteps_4000.h5"
    # truths = None

    # filename = "/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HATLAS_J090311.6+003906_2016.1.01093.S__backend_nwalkers_200_nsteps_4000.h5"
    # truths = None
    # log_prob_truth = None

    filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backends/backend_masked_AzTEC1_nwalkers_400_nsteps_1000.h5"
    discard = 350
    truths = None
    log_prob_truth = None

    # NOTE: THIS IS NOT WORKING ...
    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_with_lensing_nwalkers_200_nsteps_2000.h5"
    # truths = [50.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.05, 0.1, 0.75, 45.0, 1.0]

    # NOTE: THIS IS NOT WORKING ...
    #filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_with_FIXED_lensing_nwalkers_200_nsteps_2000.h5"

    #filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_PA_0_360_masked_nwalkers_500_nsteps_500.h5"
    #filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_PA_0_90_unmasked_nwalkers_500_nsteps_500.h5"
    #filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_PA_0_90_unmasked_nwalkers_300_nsteps_1000.h5"

    #discard = 100
    #filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_with_lensing_TURNED_OFF_nwalkers_200_nsteps_2000.h5"
    #discard = 100

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_backend_PA_0_180_unmasked__n_pixels_100_pixel_scale_0.1_nwalkers_400_nsteps_2000.h5"
    # discard = 100
    # truths = None
    #
    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/TEST_backend_with_FIXED_lensing_nwalkers_400_nsteps_2000.h5"
    # discard = 200
    # truths = [5.0e+01,  5.0e+01,  1.6e+01,  2.5e-01,  7.5e+00,  5.0e+01,  6.5e+01,  2.0e+00, 3.0e+02,  5.0e+01]
    #
    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backend_with_lensing_nwalkers_400_nsteps_2000.h5"
    # discard = 3500
    # truths = [5.0e+01,  5.0e+01,  1.6e+01,  2.5e-01,  7.5e+00,  5.0e+01,  6.5e+01,  2.0e+00, 3.0e+02,  5.0e+01, -5.0e-02,  1.0e-01,  7.5e-01,  4.5e+01,  1.0e+00]

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_backend_with_lensing_nwalkers_300_nsteps_4000.h5"
    # discard = 100
    # truths = None

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_real_plane_CONTINUUM__backend_nwalkers_200_nsteps_3000.h5"
    # discard = 1000
    # truths = [0.0, 0.0, 0.75, 50.0, 5e-05, 0.25]


    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_real_plane_LINE__backend_nwalkers_200_nsteps_3000.h5"
    # discard = 1500
    # truths = [50, 50, 16.0, 0.25, 7.5, 50.0, 65.0, 2.0, 300.0, 50.0]

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_real_plane_SIMULTANEOUS_MODERETELYFINETUNNED__backend_nwalkers_200_nsteps_4000.h5"
    # truths = None

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_real_plane_SIMULTANEOUS_INITIALIZE_AROUND_TRUTH__backend_nwalkers_200_nsteps_4000.h5"
    # truths = [0.0, 0.0, 0.75, 50.0, 5e-05, 0.25, 50, 50, 16.0, 0.25, 7.5, 50.0, 65.0, 2.0, 300.0, 50.0]

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_real_plane_CLEAN_SIMULTANEOUS_NOVELTY__backend_nwalkers_200_nsteps_4000.h5"
    # truths = [0.0, 0.0, 0.75, 50.0, 0.00005, 0.25, 1.0, 0.0, 0.0, 16.0, 0.5, 0.5, 40.0, 50.0, 0.1, 200.0, 50.0]
    # log_prob_truth = -160000.23726599006

    # filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/fit_continuum_and_kinematics_real_plane_CLEAN_SIMULTANEOUS_NOVELTY_TRUTHINIT__backend_nwalkers_200_nsteps_4000.h5"
    # truths = [0.0, 0.0, 0.75, 50.0, 0.00005, 0.25, 1.0, 0.0, 0.0, 16.0, 0.5, 0.5, 40.0, 50.0, 0.1, 200.0, 50.0]
    # log_prob_truth = -160000.23726599006
    # discard = 200


    backend = emcee.backends.HDFBackend(filename)
    log_prob = backend.get_log_prob(
        flat=flat, thin=thin, discard=discard
    )
    chain = backend.get_chain(
        flat=flat, thin=thin, discard=discard
    )
    print("shape (chain):", chain.shape)#;exit()

    # plot_log_prob(log_prob=log_prob)
    # exit()

    # NOTE: ...
    # idx = filter_chain(
    #     chain=chain,
    #     parameter_indexes=[0, 1],
    #     values_min=[40.0, 40.0],
    #     values_max=[60.0, 60.0]
    # )
    # chain = chain[:, idx, :]
    # log_prob = log_prob[:, idx]

    # NOTE: ...
    #log_prob_min = - 5.0 * 10**9.0
    #log_prob_min = - 1.0 * 10**8.0
    #log_prob_min = - 1.0 * 10**9.0
    log_prob_min = - 4.8944 * 10**7.0
    idx = np.where(
        log_prob[-1, :] > log_prob_min
    )
    chain = chain[:, idx[0], :]
    log_prob = log_prob[:, idx[0]]



    # plot_log_prob(
    #     log_prob=log_prob,
    #     truth=log_prob_truth,
    #     xlim=(0, 400)
    # )
    # exit()

    #exit()

    #labels = [r"$x$", r"$y$", r"$x$", r"$flux$", r"$r$", r"$i$", r"$\theta$", r"$r_{turn}$", r"$V_{max}$", r"$\sigma$"]

    #print(chain.shape, log_prob.shape);exit()

    #plot_corner(chain=chain.reshape(-1, chain.shape[-1]), c=np.ndarray.flatten(log_prob), s=1, figsize=(10, 9))


    # NOTE: TURN THIS INTO A FUNCTION
    """
    log_prob_max = np.max(log_prob)

    k = 0
    plt.figure(figsize=(12, 8))
    for n_w in range(chain.shape[1]):
        plt.plot(chain[:, n_w, k], color="black", alpha=0.25)

    for n_w in range(chain.shape[1]):
        plt.scatter(np.arange(chain.shape[0]), chain[:, n_w, k], s=10, c=log_prob[:, n_w]/log_prob_max, cmap="jet")

    for i in range(chain.shape[1]):
        plt.text(0.0, chain[0, i, k], str(i), color="black")
    plt.show()
    exit()
    """

    # NOTE: Turn this into a function
    """
    chain = chain.reshape(-1, chain.shape[-1])
    c = np.ndarray.flatten(log_prob)
    i = -5
    j = -4
    figure = plt.figure()
    sc = plt.scatter(chain[:, i], chain[:, j], c=c, cmap="jet")
    plt.axvline(truths[i], color="black", linestyle="--")
    plt.axhline(truths[j], color="black", linestyle="--")
    figure.colorbar(sc)
    plt.show()
    exit()
    """

    # plot_chain(
    #     chain=chain,
    #     log_prob=None,
    #     ncols=4,
    #     figsize=(20, 6),
    #     walkers=None,
    #     truths=truths,
    #     title="N={} steps have been discarded".format(discard),
    #     ylabels=["x", "y", "z", "flux", "R", "i", r"$\theta$", "$r_{t}$", "$V_{max}$", "$\sigma$"]
    # )
    # exit()

    chain = np.delete(chain, 2, 2)

    figure = corner.corner(
        xs=chain.reshape(-1, chain.shape[-1]),
        bins=20,
        labels=["x", "y", "flux", r"$R^{1/2}$", "i", r"$\theta$", r"$r_{turn}$", r"$V_{max}$", r"$\sigma$"]
    )

    axes = np.array(figure.axes).reshape((chain.shape[-1], chain.shape[-1]))

    plt.show()
    exit()

    #exit()

    """
    # NOTE: MAKE THIS A FUNCTION
    N = 1.0
    chain_for_par = chain[:, :, -1]
    chain_for_par_bool = np.ones(shape=chain_for_par.shape, dtype=bool)#;print(chain_for_par_bool);exit()
    for i in range(chain_for_par.shape[0]):
        mean = np.mean(chain_for_par[i, :])
        std = np.std(chain_for_par[i, :])

        for j in range(chain_for_par.shape[1]):
            if chain_for_par[i, j] < mean - N * std or chain_for_par[i, j] > mean + N * std:
                chain_for_par_bool[i, j] = False

    # plt.imshow(chain_for_par_bool)
    # plt.show()
    # exit()

    cutoff = 85.0
    idx = np.ones(shape=chain_for_par.shape[1], dtype=bool)
    for i in range(idx.shape[0]):

        if np.sum(chain_for_par_bool[:, i]) / chain_for_par.shape[0] * 100.0 < cutoff:
            idx[i] = False

        #print(i, np.sum(chain_for_par_bool[:, i]) / chain_for_par.shape[0] * 100.0)

    # chain_for_par_temp = chain_for_par[:, idx]
    # print(chain_for_par_temp.shape, chain_for_par.shape)
    # exit()

    chain = chain[:, idx, :]

    plot_chain(chain=chain, ncols=5, figsize=(20, 6))

    fig = corner.corner(
        chain.reshape(-1, chain.shape[-1]), bins=20
    )
    plt.show()
    """


    N = 1.0
    chain_idx = np.ones(
        shape=chain.shape[:-1],
        dtype=bool
    )
    for k in range(chain.shape[-1]):

        for i in range(chain.shape[0]):

            mean = np.mean(chain[i, :, k])
            std = np.std(chain[i, :, k])

            for j in range(chain.shape[1]):
                if chain[i, j, k] < mean - N * std or chain[i, j, k] > mean + N * std:
                    chain_idx[i, j] = False

    cutoff = 95.0
    idx = np.ones(shape=chain_idx.shape[-1], dtype=bool)
    for i in range(idx.shape[0]):

        if np.sum(chain_idx[:, i]) / chain.shape[0] * 100.0 < cutoff:
            idx[i] = False

    chain = chain[:, idx, :]
    log_prob = log_prob[:, idx]
    #print(chain.shape);exit()




    # get_best_fit_parameters_from_chain_as_50th_percentile(chain)
    # exit()

    # plt.figure()
    # chain = chain.reshape(-1, chain.shape[-1])
    # plt.scatter(chain[:, 0], chain[:, 1], c=np.ndarray.flatten(log_prob), s=1)
    # plt.show()
    # exit()

    plot_chain(chain=chain, log_prob=None, ncols=5, figsize=(20, 6))
    exit()

    # fig = corner.corner(
    #     xs=chain.reshape(-1, chain.shape[-1]),
    #     bins=20,
    #     quantiles=[0.16, 0.5, 0.84],
    # )
    # #labels=labels,
    # #show_titles=True,
    # #title_kwargs={"fontsize": 12}
    # plt.show()
    # exit()


    plot_corner(chain=chain.reshape(-1, chain.shape[-1]), c=np.ndarray.flatten(log_prob))
