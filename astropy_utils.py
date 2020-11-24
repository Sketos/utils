import numpy as np
import matplotlib.pyplot as plt

from astropy.cosmology import FlatLambdaCDM
from astropy.modeling import models


def get_default_FlatLambdaCDM():
    return FlatLambdaCDM(
        H0=70, Om0=0.3, Tcmb0=2.725
    )

# def get_FlatLambdaCDM_from_():
#     pass

if __name__ == "__main__":
    pass


    f = models.SmoothlyBrokenPowerLaw1D(
        amplitude=1,
        x_break=50,
        alpha_1=-0.5,
        alpha_2=-3.0
    )

    x = np.logspace(0.7, 2.3, 500)
    plt.plot(x, f(x), '--', label='delta=0.5')

    plt.xscale("log")
    plt.yscale("log")
    plt.show()
