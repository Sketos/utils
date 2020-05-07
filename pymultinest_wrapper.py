import os
import sys
import json
import ctypes
import numpy as np
import scipy.stats, scipy
import pymultinest
import matplotlib.pyplot as plt

import getdist_utils as getdist_utils


class pymultinest_wrapper:

    def __init__(self, helper, log_likelihood_func, parameters, prior_limits):

        self.helper = helper

        self.log_likelihood_func = log_likelihood_func

        # NOTE: This should be combined as one thingy
        self.parameters = parameters
        self.prior_limits = prior_limits


    def run(self, output_directory=None, n_live_points=100, const_efficiency_mode=False):

        def log_likelihood(cube, ndim, nparams):

            _log_likelihood = self.log_likelihood_func(
                obj=self, cube=cube
            )

            return _log_likelihood


        # NOTE: ...
        def prior(cube, ndim, nparams):

            phys_cube = list(
                map(self.helper.prior_model.uniform, self.prior_limits, cube)
            )

            for i in range(len(phys_cube)):
                cube[i] = phys_cube[i]

            return cube


        # NOTE:
        if output_directory is None:
            output_directory = os.path.dirname(
                os.path.realpath(__file__)
            )
        else:
            pass


        # NOTE:
        np.savetxt(
            "{}/multinest_.paramnames".format(
                output_directory
            ),
            np.transpose([
                ["param_{}".format(i) for i in range(len(self.parameters))],
                self.parameters
            ]),
            fmt="%s"
        )
        
        # NOTE:
        pymultinest.run(
            log_likelihood,
            prior,
            len(self.parameters),
            outputfiles_basename="{}/multinest_".format(
                output_directory
            ),
            n_live_points=n_live_points,
            const_efficiency_mode=const_efficiency_mode,
            resume=False,
            verbose=True
        )




# NOTE: ...
def model(x, theta):
    pos, width, height = theta

    return  height * scipy.stats.norm.pdf(x, pos, width)


# NOTE:
def log_likelihood_func(obj, cube):

    def error_normalization(yerr):

        return np.log(2.0 * np.pi * yerr**2.0)

    # NOTE: ...
    if isinstance(cube, ctypes.POINTER(ctypes.c_double)):
        theta = np.zeros(
            shape=(len(obj.parameters)),
            dtype=np.float
        )
        for i in range(len(obj.parameters)):
            theta[i] = cube[i]
    else:
        pass

    y_model = model(obj.helper.data.x, theta)

    return -0.5 * np.sum(
        (obj.helper.data.y - y_model)**2.0
        / obj.helper.data.yerr**2.0
        + error_normalization(yerr=obj.helper.data.yerr)
    )


# NOTE:
class Data:
    def __init__(self, x, y, yerr=None):

        self.x = x
        self.y = y

        # NOTE: ...
        if yerr is None:
            raise ValueError("...")
            #self.yerr = np.ones(shape=self.y.shape)
        else:
            self.yerr = yerr


class PriorModel:

    def __init__(self):
        pass

    def uniform(self, vector, value):

        return vector[0] + value * (vector[1] - vector[0])


    def loguniform(self, vector, value):
        pass


    def gaussian(self, vector, value):
        pass


class Helper:

    def __init__(self, data, prior_model=None):

        self.data = data

        self.prior_model = prior_model





if __name__ == "__main__":

    x = np.linspace(0, 1, 400)

    param_0 = 0.5
    param_1 = 0.1
    param_2 = 0.5
    theta = [param_0, param_1, param_2]

    y = model(x, theta)

    yerr = np.random.normal(
        loc=0.0,
        scale=0.1,
        size=y.shape
    )
    y += yerr

    prior_limits = np.array([
        [0.0, 1.0],
        [0.0, 2.0],
        [0.0, 1.0]
    ])

    # plt.figure()
    # plt.plot(x, y)
    # plt.plot(x, yerr)
    # plt.show()

    helper = Helper(
        data=Data(
            x=x,
            y=y,
            yerr=yerr
        ),
        prior_model=PriorModel()
    )

    parameters = ["a", "b", "c"]

    obj = pymultinest_wrapper(
        helper=helper,
        log_likelihood_func=log_likelihood_func,
        parameters=parameters,
        prior_limits=prior_limits
    )

    output_directory = os.path.dirname(
        os.path.realpath(__file__)
    )
    os.system(
        "rm {}/multinest_*".format(output_directory)
    )
    obj.run(output_directory=output_directory)

    #json.dump(parameters, open("{}/multinest_.json".format(output_directory), 'w'))



    getdist_utils.triangle_plot(
        directory=output_directory,
        suffix="_",
        width_inch=16
    )


    # def results(helper, output_directory):
    #     pass
    #
    # # NOTE: Turn this into a function. Although getdist is not implemented so not really nessesary
    # plt.figure()
    # plt.plot(
    #     helper.data.x,
    #     helper.data.y,
    #     marker='+',
    #     color='red',
    #     label='data'
    # )
    # a = pymultinest.Analyzer(
    #     outputfiles_basename="{}/multinest_".format(
    #         output_directory
    #     ),
    #     n_params=len(obj.parameters)
    # )
    # for (pos, width, height) in a.get_equal_weighted_posterior()[::100,:-1]:
    # 	plt.plot(
    #         helper.data.x,
    #         model(
    #             helper.data.x,
    #             theta=[pos, width, height]
    #         ),
    #         linestyle='-',
    #         color='blue',
    #         alpha=0.3,
    #         label='model'
    #     )
    #
    # plt.show()
