import numpy as np
import matplotlib.pyplot as plt
import emcee
from multiprocessing import Pool


# NOTE:
def model(x, theta):
    a, b, c = theta
    return a * x**2.0 + b * x + c


# NOTE:
def log_likelihood_helper(obj, theta):

    y_model = model(obj.x, theta)

    return -0.5 * np.sum(
        (obj.y - y_model)**2.0 / obj.yerr**2.0 + np.log(2.0 * np.pi * obj.yerr**2.0)
    )



# NOTE: This will be added in the class as a staticmethod and be used in log_prior
# def check(value, value_min, value_max):
#     if value > value_min and value < value_max:
#         return True
#     return False
#
# value = 2.0
# value_min = -5.0
# value_max = 5.0
#
#
# # check_outcome = check(value=value, value_min=value_min, value_max=value_max)
# # print(check_outcome)
#
# values = [-20.0, -10.0, 2.0]
# args = (value_min, value_max)
# check_outcomes = list(map(lambda val: check(val, *args), values))
# print(check_outcomes)

class emcee_wrapper:

    def __init__(self, x, y, yerr, mcmc_limits, n_walkers=500):

        self.x = x
        self.y = y

        # NOTE: What do I do in the case where I dont have yerr available
        if yerr is None:
            self.yerr = np.ones(shape=self.y.shape)
        else:
            self.yerr = yerr

        # ...
        if mcmc_limits is None:
            raise ValueError

        self.par_min = mcmc_limits[:, 0]
        self.par_max = mcmc_limits[:, 1]

        self.n_dim = mcmc_limits.shape[0]

        self.n_walkers = n_walkers

        # NOTE: ...
        self.initial_state = self.initialize(
            par_min=self.par_min,
            par_max=self.par_max,
            n_dim=self.n_dim,
            n_walkers=self.n_walkers
        )

    @staticmethod
    def initialize(par_min, par_max, n_dim, n_walkers):

        return np.array([
            par_min + (par_max - par_min) * np.random.rand(n_dim)
            for i in range(n_walkers)
        ])


    def log_prior(self, theta):

        # NOTE: make this a function
        condition = np.zeros(
            shape=self.n_dim, dtype=bool
        )
        for n in range(len(theta)):
            if self.par_min[n] < theta[n] < self.par_max[n]:
                condition[n] = True

        if np.all(condition):
            return 0.0
        else:
            return -np.inf


    def log_likelihood(self, theta):

        # NOTE: pass the object so that the helper function has the data.
        _log_likelihood = log_likelihood_helper(
            self, theta
        )

        return _log_likelihood


    def log_probability(self,theta):

        lp = self.log_prior(theta)

        if not np.isfinite(lp):
            return -np.inf
        else:
            return lp + self.log_likelihood(theta=theta)


    # NOTE: This function makes the "log_probability" pickleable.
    def __call__(self, theta):
        return self.log_probability(theta)


    def run(self, nsteps, parallel=False):

        if parallel:
            pool = Pool()
        else:
            pool = None

        sampler = emcee.EnsembleSampler(
            nwalkers=self.n_walkers,
            ndim=self.n_dim,
            log_prob_fn=self.log_probability,
            pool=pool
        )

        sampler.run_mcmc(
            initial_state=self.initial_state,
            nsteps=nsteps,
            progress=True
        )

        return sampler




# class test_class:
#     def __init__(self, x):
#         self.x = x
#
#     def func(self):
#
#         other_func(obj=self)
#
# def other_func(obj):
#     print(obj.x)
#
# o = test_class(x=2.0)
# o.func()

#exit()

if __name__ == "__main__":

    xmin = -1.0
    xmax = 2.0
    xnum = 20
    x = np.linspace(xmin, xmax, xnum)

    a_true = 2.0
    b_true = -2.5
    c_true = 0.5
    theta = [a_true, b_true, c_true]
    y = model(
        x=x, theta=theta
    )

    yerr = np.random.normal(0.0, 0.2, size=len(x))
    y += yerr


    model_parameter_limits = np.array([
        [-5.0,5.0], [-5.0,5.0], [-5.0,5.0],
    ])

    obj = emcee_wrapper(
        x=x, y=y, yerr=yerr, mcmc_limits=model_parameter_limits, n_walkers=500
    )

    sampler = obj.run(nsteps=500, parallel=False)


    flat_samples = sampler.get_chain(discard=100, thin=15, flat=True)

    # plt.figure()
    # plt.errorbar(x, y, yerr=yerr, linestyle="None", marker="o")
    # plt.show()
    # exit()

    import corner

    fig = corner.corner(
        flat_samples, labels=["a", "b", "c"], truths=[a_true, b_true, c_true]
    )
    plt.show()
