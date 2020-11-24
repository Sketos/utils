import numpy as np
import matplotlib.pyplot as plt
import emcee
import corner



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



flat = False
thin = 1
discard = 0

if __name__ =="__main__":

    #filename = "name.h5"
    filename = "/Users/ccbh87/Desktop/GitHub/UVgalpak3D/backends/backend_masked_AzTEC1_nwalkers_400_nsteps_1000.h5"
    backend = emcee.backends.HDFBackend(filename)

    log_prob = backend.get_log_prob(
        flat=flat,
        thin=thin,
        discard=discard
    )

    plot_log_prob(
        log_prob=log_prob,
        xlim=(0, 4000)
    )
