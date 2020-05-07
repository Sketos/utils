# NOTE: THIS IS JUST A TEST SCRIPT. DELETE IT AFTERWARDS.

import os
import sys
import time
import emcee
import numpy as np
from multiprocessing import Pool
import h5py
from schwimmbad import MPIPool

os.environ["OMP_NUM_THREADS"] = "1"


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


class emcee_wrapper:
    def __init__(self, helper, log_likelihood_func, nwalkers, mcmc_limits, backend_filename):

        self.helper = helper
        self.log_likelihood_func = log_likelihood_func

        self.backend = emcee.backends.HDFBackend(
            filename=backend_filename
        )

        self.nwalkers=nwalkers
        self.ndim=mcmc_limits.shape[0]

        np.random.seed(42)

        self.par_min = mcmc_limits[:, 0]
        self.par_max = mcmc_limits[:, 1]

        self.initial = self.initialize_state(
            par_min=self.par_min,
            par_max=self.par_max,
            ndim=self.ndim,
            nwalkers=self.nwalkers
        )


    @staticmethod
    def initialize_state(par_min, par_max, ndim, nwalkers):

        return np.array([
            par_min + (par_max - par_min) * np.random.rand(ndim)
            for i in range(nwalkers)
        ])


    @staticmethod
    def log_prior_conditions(values, values_min, values_max):

        conditions = np.zeros(
            shape=values.shape, dtype=bool
        )

        for i, value in enumerate(values):
            if values_min[i] < value < values_max[i]:
                conditions[i] = True

        return conditions


    def log_prior(self, theta):

        conditions = self.log_prior_conditions(
            values=theta,
            values_min=self.par_min,
            values_max=self.par_max
        )

        if np.all(conditions):
            return 0.0
        else:
            return -np.inf


    # def log_prob(self, theta):
    #     _log_prob = self.log_prob_func(self, theta=theta)
    #     return _log_prob


    #def __call__(self, theta):
    #    return self.log_prob(theta)

    def log_likelihood(self, theta):

        # NOTE: pass the object to have flexibility on what to do on the log_likelihood function.
        _log_likelihood = self.log_likelihood_func(
            self, theta
        )

        return _log_likelihood


    def log_probability(self, theta):

        lp = self.log_prior(theta)

        if not np.isfinite(lp):
            return -np.inf
        else:
            return lp + self.log_likelihood(theta=theta)


    def run(self, nsteps, parallel):

        def run_func(nsteps, pool=None):
            sampler = emcee.EnsembleSampler(
                nwalkers=self.nwalkers,
                ndim=self.ndim,
                log_prob_fn=self.log_probability,
                backend=self.backend,
                pool=pool
            )

            sampler.run_mcmc(
                initial_state=self.initial,
                nsteps=nsteps,
                progress=True
            )

            return sampler

        start = time.time()
        if parallel:
            with MPIPool() as pool:
                if not pool.is_master():
                    pool.wait()
                    sys.exit(0)
                run_func(nsteps=nsteps, pool=pool)
        end = time.time()
        print("total time =", end - start)


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


xmin = -1.0
xmax = 2.0
xnum = 20
x = np.linspace(
    xmin,
    xmax,
    xnum
)

a_true, b_true, c_true = 2.0, -2.5, 0.5
y = model(
    x=x,
    theta=[
        a_true,
        b_true,
        c_true
    ]
)

yerr = np.random.normal(
    0.0, 0.2, size=len(x)
)
y += yerr

mcmc_limits = np.array([
    [-10.0, 10.0], [-10.0, 10.0], [-10.0, 10.0],
])



#np.random.seed(42)
#initial = np.random.randn(32, 5)
nwalkers = 32
nsteps = 2000

helper = Helper(
    data=Data(
        x=x,
        y=y,
        yerr=yerr
    )
)

backend_filename = "backend_nsteps_{}.h5".format(nsteps)
os.system(
    "rm {}".format(backend_filename)
)

obj = emcee_wrapper(
    helper=helper,
    log_likelihood_func=log_likelihood_func,
    nwalkers=nwalkers,
    mcmc_limits=mcmc_limits,
    backend_filename=backend_filename
)

obj.run(
    nsteps, parallel=True
)














# import os
# import sys
# import time
# import emcee
# import numpy as np
# from multiprocessing import Pool
# import h5py
# from schwimmbad import MPIPool
#
# os.environ["OMP_NUM_THREADS"] = "1"
#
# class Helper:
#     def __init__(self):
#         pass
#
#
# def log_prob_func(obj, theta):
#     t = time.time() + np.random.uniform(0.005, 0.008)
#     #while True:
#     #    if time.time() >= t:
#     #        break
#     return -0.5 * np.sum(theta ** 2)
#
#
# class emcee_wrapper:
#     def __init__(self, helper, log_prob_func, mcmc_limits, nwalkers, backend_filename):
#         self.helper = helper
#         self.log_prob_func = log_prob_func
#
#         self.backend = emcee.backends.HDFBackend(
#             filename=backend_filename
#         )
#
#         self.nwalkers=nwalkers
#
#         self.ndim = mcmc_limits.shape[0]
#
#         np.random.seed(42)
#         self.initial = np.random.randn(self.nwalkers, self.ndim)
#
#
#     # def initialize_state(par_min, par_max, ndim, nwalkers):
#     #
#     #     return np.array([
#     #         par_min + (par_max - par_min) * np.random.rand(ndim)
#     #         for i in range(nwalkers)
#     #     ])
#
#
#     def log_prob(self, theta):
#         _log_prob = self.log_prob_func(self, theta=theta)
#         return _log_prob
#
#
#     #def __call__(self, theta):
#     #    return self.log_prob(theta)
#
#
#     def run(self, nsteps, parallel):
#
#         def run_func(nsteps, pool=None):
#             sampler = emcee.EnsembleSampler(nwalkers=self.nwalkers, ndim=self.ndim, log_prob_fn=self.log_prob, backend=self.backend, pool=pool)
#             sampler.run_mcmc(initial_state=self.initial, nsteps=nsteps, progress=True)
#
#             return sampler
#
#         start = time.time()
#         if parallel:
#             with MPIPool() as pool:
#                 if not pool.is_master():
#                     pool.wait()
#                     sys.exit(0)
#                 run_func(nsteps=nsteps, pool=pool)
#                 #sampler = emcee.EnsembleSampler(nwalkers, ndim, self.log_prob, backend=self.backend, pool=pool)
#                 #sampler.run_mcmc(initial, nsteps, progress=True)
#         end = time.time()
#         print("total time =", end - start)
#
# #np.random.seed(42)
# #initial = np.random.randn(32, 5)
# nwalkers = 200
# nsteps=500
#
# helper = Helper()
#
# mcmc_limits = np.array([
#     [0.0, 5.0],
#     [0.0, 5.0],
#     [0.0, 5.0]
# ])
#
# os.system("rm backend.h5")
# obj = emcee_wrapper(helper=helper, log_prob_func=log_prob_func, mcmc_limits=mcmc_limits, nwalkers=nwalkers, backend_filename="backend.h5")
#
# obj.run(nsteps=nsteps, parallel=True)
