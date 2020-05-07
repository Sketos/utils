import sys
import time
import emcee
import numpy as np
#from schwimmbad import MPIPool
from multiprocessing import Pool


class Helper:
    def __init__(self):
        pass


def log_prob_func(obj, theta):
    t = time.time() + np.random.uniform(0.005, 0.008)
    while True:
        if time.time() >= t:
            break
    return -0.5 * np.sum(theta ** 2)


class emcee_wrapper:
    def __init__(self, helper, log_prob_func):
        self.helper = helper
        self.log_prob_func = log_prob_func


    def log_prob(self, theta):
        _log_prob = self.log_prob_func(self, theta=theta)
        return _log_prob


    def __call__(self, theta):
        return self.log_prob(theta)


    def run(self, nwalkers, ndim, initial, nsteps, parallel):

        start = time.time()
        if parallel:
            with MPIPool() as pool:
                if not pool.is_master():
                    pool.wait()
                    sys.exit(0)
                    
                sampler = emcee.EnsembleSampler(nwalkers, ndim, self.log_prob, pool=pool)
                sampler.run_mcmc(initial, nsteps, progress=True)
        end = time.time()
        print("total time =", end - start)


np.random.seed(42)
initial = np.random.randn(32, 5)
nwalkers, ndim = initial.shape
nsteps=200

helper = Helper()

obj = emcee_wrapper(helper=helper, log_prob_func=log_prob_func)
obj.run(nwalkers, ndim, initial, nsteps, parallel=True)




""" # NOTE: This runs fine on COSMA with omp
def log_prob(theta):
    t = time.time() + np.random.uniform(0.005, 0.008)
    while True:
        if time.time() >= t:
            break
    return -0.5*np.sum(theta**2)

with MPIPool() as pool:
    if not pool.is_master():
        pool.wait()
        sys.exit(0)

    np.random.seed(42)
    initial = np.random.randn(32, 5)
    nwalkers, ndim = initial.shape
    nsteps = 100

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_prob, pool=pool)
    start = time.time()
    sampler.run_mcmc(initial, nsteps)
    end = time.time()
    print(end - start)
"""



#env MPICC=/usr/local/bin/mpicc pip install mpi4py
