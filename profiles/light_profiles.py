import numpy as np
import matplotlib.pyplot as plt

from scipy import special
from astropy import units

def Disk(r, s0, rs, h, hs):

    return s0 * (r / rs) * special.k1(r / rs) * np.square(1.0 / np.cosh(h / hs))


if __name__ == "__main__":

    N = 100
    r_min = 10**-2.0
    r_max = 10**+1.0

    r = np.logspace(
        np.log10(r_min),
        np.log10(r_max),
        N
    )




    plt.figure()
    for h in [0.1, 0.5, 1.0]:
        profile = Disk(
            r=r,
            s0=10**12.0,
            rs=0.5,
            h=h,
            hs=0.5,
        )
        plt.plot(r, profile, label="h={}".format(h))
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.show()
