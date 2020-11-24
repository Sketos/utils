import numpy as np
import matplotlib.pyplot as plt

from scipy import special


def velocity_profile(r, r_turn, r_disk, v_max, profile="arctan"):

    x = r / r_turn

    if profile == "arctan":
        velocity_profile = 2.0 / np.pi * np.arctan(x) * v_max

    if profile == "freeman":

        def velocity_profile_freeman(r, r_disk, v_max):

            y = 1.68 * r / r_disk / 2.0

            B = np.subtract(
                special.i0(y) * special.k0(y),
                special.i1(y) * special.k1(y)
            )

            B1 = 0.1934
            v_disk_sq =  v_max**2.0 * y**2.0 * B / B1

            return v_disk_sq

        velocity_profile = np.sqrt(
            velocity_profile_freeman(
                r=r,
                r_disk=r_disk,
                v_max=v_max
            )
        )

    return velocity_profile


if __name__ == "__main__":

    r_max = 2.0 # kpc

    r = np.linspace(-r_max, r_max, 100)

    r_turn = 0.1 # kpc
    r_disk = 1.0 # kpc
    v_max = 200.0 # km / s

    profile_arctan = velocity_profile(r=r, r_turn=r_turn, r_disk=r_disk, v_max=v_max, profile="arctan")
    profile_freeman = velocity_profile(r=r, r_turn=r_turn, r_disk=r_disk, v_max=v_max, profile="freeman")

    plt.plot(r, profile_arctan, marker="o")
    plt.plot(r, profile_freeman, marker="o")
    plt.show()
