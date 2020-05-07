import os
import numpy as np
import matplotlib.pyplot as plt

from emcee_wrapper import emcee_wrapper


# NOTE:
def model(x, theta):
    a, b, c = theta
    return a * x**2.0 + b * x + c


# NOTE:
def log_likelihood_func(obj, theta):

    y_model = model(obj.helper.data.x, theta)

    return -0.5 * np.sum(
        (obj.helper.data.y - y_model)**2.0 / obj.helper.data.yerr**2.0 + np.log(2.0 * np.pi * obj.helper.data.yerr**2.0)
    )


# NOTE:
class Data:
    def __init__(self, x, y, yerr):

        self.x = x
        self.y = y

        # NOTE: ...
        if yerr is None:
            self.yerr = np.ones(shape=self.y.shape)
        else:
            self.yerr = yerr


class Helper:
    def __init__(self, data):
        self.data = data


def backend_filename():
    filename = None
    return filename


if __name__ == "__main__":
    os.system("rm backend.h5")

    xmin = -1.0
    xmax = 2.0
    xnum = 20
    x = np.linspace(xmin, xmax, xnum)

    a_true = 2.0
    b_true = -2.5
    c_true = 0.5
    theta = [a_true, b_true, c_true]
    #theta = [a_true, b_true, c_true, d_true, e_true]
    y = model(
        x=x, theta=theta
    )

    yerr = np.random.normal(0.0, 0.2, size=len(x))
    y += yerr

    # plt.errorbar(x, y, yerr=yerr)
    # plt.show()
    # exit()

    data = Data(x=x, y=y, yerr=yerr)

    helper = Helper(data=data)


    mcmc_limits = np.array([
        [-50.0,50.0], [-50.0,50.0], [-50.0,50.0],
    ])
    # mcmc_limits = np.array([
    #     [-5.0,5.0], [-5.0,5.0], [-5.0,5.0], [-5.0,5.0], [0.0,5.0],
    # ])



    obj = emcee_wrapper(
        helper=helper,
        mcmc_limits=mcmc_limits,
        log_likelihood_func=log_likelihood_func,
        nwalkers=500
    )

    #print(obj.log_likelihood);exit()

    sampler = obj.run(nsteps=200, parallel=True)
    print(sampler.chain.shape)

    flat_samples = sampler.get_chain(discard=100, thin=10, flat=True)

    # plt.figure()
    # plt.errorbar(x, y, yerr=yerr, linestyle="None", marker="o")
    # plt.show()
    # exit()

    import corner

    fig = corner.corner(
        flat_samples, truths=theta
    )
    plt.show()
