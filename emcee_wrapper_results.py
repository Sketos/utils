import numpy as np
import matplotlib.pyplot as plt
import emcee


nsteps = 2000
filename = "backend_nsteps_{}.h5".format(nsteps)

backend = emcee.backends.HDFBackend(filename)
samples = backend.get_chain(
    discard=100, flat=True, thin=15
)

truths = [2.0, -2.5, 0.5]
best_fit_parameters = []
for i in range(samples.shape[-1]):
    i_best_fit_parameter = np.percentile(samples[:, i], [50])
    print(i_best_fit_parameter)

exit()
