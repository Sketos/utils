import numpy as np

import matplotlib.pyplot as plt

import spectral_utils as spectral_utils
import plot_utils as plot_utils


def rotation_curve(cube, x, y, velocities, f_min=None):

    # cube_moment_1 = spectral_utils.moment_1(cube=cube, velocities=velocities, f_min=f_min, axis=0)
    #
    # plt.imshow(cube_moment_1, cmap="jet", vmin=-250, vmax=250)
    # plt.plot(x, y, color="black")
    # plt.show()




    #print(velocities.shape, cube.shape);exit()


    cube[np.where(cube < f_min)] = np.nan

    z_temp = []
    for i, (x_i, y_i) in enumerate(zip(x, y)):

        i = int(x_i)
        j = int(y_i)

        #cube[:, j, i] = np.nan

        spectrum = cube[:, j, i]
        #print(i)
        #if i == 0:
        #plt.plot(velocities, spectrum)

        x_temp = velocities
        y_temp = cube[:, j, i]

        print(x_temp, y_temp)



        idx = np.isnan(y_temp)

        x_temp_idx = x_temp[~idx]
        y_temp_idx = y_temp[~idx]

        if all(idx):
            z_temp.append(np.nan)
        else:
            z = np.average(x_temp_idx, weights=y_temp_idx)

            z = x_temp_idx[np.argmax(y_temp_idx)]

            plt.plot(x_temp, y_temp)
            plt.axvline(z, color="black")
            plt.xlim((-500, 500))
            plt.show()

            z_temp.append(z)

    plt.figure()
    plt.plot(z_temp, marker="o")
    plt.show()

    #plot_utils.plot_cube(cube=cube, ncols=5)


    exit()
