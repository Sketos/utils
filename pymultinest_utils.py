import ctypes
import numpy as np

def sanitize(theta, theta_len):

    if isinstance(theta, ctypes.POINTER(ctypes.c_double)):
        theta_temp = np.zeros(
            shape=(theta_len, ),
            dtype=np.float
        )
        for i in range(theta_len):
            theta_temp[i] = theta[i]

        theta = theta_temp

    return theta
