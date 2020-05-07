import numpy as np


def BIC(number_of_data_points, number_of_parameters, maximum_likelihood):

    return np.log(number_of_data_points) * number_of_parameters - np.log(maximum_likelihood)
