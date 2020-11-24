import time
import matplotlib

import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits

from fbm import fbm

import autolens as al


def wrap(a):
    """Short summary.

    Parameters
    ----------
    a : type
        Description of parameter `a`.

    Returns
    -------
    type
        Description of returned object.

    """

    return (a + np.pi) % (2.0 * np.pi) - np.pi


def phase_errors_from_A_and_B_matrices(phases, model_phases, A, B):
    """Short summary.

    Parameters
    ----------
    phases : type
        Description of parameter `phases`.
    model_phases : type
        Description of parameter `model_phases`.
    A : type
        Description of parameter `A`.
    B : type
        Description of parameter `B`.

    Returns
    -------
    type
        Description of returned object.

    """

    phase_difference = wrap(
        a=np.subtract(
            phases,
            model_phases
        )
    )

    phase_errors = np.linalg.solve(
        A,
        np.matmul(
            B,
            phase_difference
        )
    )

    return phase_errors


def phase_errors_from_dataset_and_model_data(dataset, model_data):

    return phase_errors_from_A_and_B_matrices(
        phases=dataset.phases,
        model_phases=model_data.phases,
        A=dataset.A,
        B=dataset.B
    )


# #U, S, V = np.linalg.svd(a=dataset.A, full_matrices=True)
# U, S, V = np.linalg.svd(
#     a=(dataset.A + 10**7.0 * np.identity(n=dataset.A.shape[0])),
#     full_matrices=True
# )
#
# print(S);exit()

def phase_errors_from_A_and_B_matrices_with_regularization(phases, model_phases, A, B, coefficient=0.0, type=None):

    phase_difference = wrap(
        a=np.subtract(
            phases,
            model_phases
        )
    )

    B = np.matmul(
        B,
        phase_difference
    )

    # plt.figure()
    # plt.imshow(
    #     A,
    #     cmap="jet",
    #     norm=matplotlib.colors.SymLogNorm(10**-1)
    # )
    # plt.xticks([])
    # plt.yticks([])
    # plt.colorbar()
    # plt.show()
    # exit()

    # figure, axes = plt.subplots(
    #     nrows=1,
    #     ncols=2
    # )
    # axes[0].imshow(A, aspect="auto")
    # axes[1].imshow(B, aspect="auto")
    # plt.show()
    # exit()

    # plt.figure()
    # #plt.imshow(np.log10(np.linalg.inv(A)))
    # plt.imshow(A)
    # plt.colorbar()
    # plt.show()
    # exit()

    I = np.identity(n=A.shape[0])

    if type is None:
        phase_errors = np.linalg.solve(A, B)

        # phase_errors = np.dot(
        #     np.linalg.inv(A),
        #     B
        # ) # NOTE: This has a numerical problem ...
        # phase_errors = np.dot(
        #     np.linalg.inv(np.add(A, 1.e-8)),
        #     B
        # )

        #phase_errors, _, _, _ = np.linalg.lstsq(A, B)

    elif type == "Tikhonov":
        phase_errors = np.linalg.solve(
            np.add(
                A,
                coefficient * I
            ),
            B
        )
    elif type == "Wiener":

        U, S, V = np.linalg.svd(a=A, full_matrices=True)

        phase_errors = np.sum(
            S / (S**2.0 + coefficient**2.0) * np.matmul(V, B) * U,
            axis=1
        )
    else:
        raise ValueError("...")

    return phase_errors




def compute_f_matrix_from_antennas(antennas):
    """Short summary.

    Parameters
    ----------
    antennas : type
        The shape of the array must of the form (n_v, 2).

    Returns
    -------
    type
        Description of returned object.

    """

    def reshape(a, n_b):
        """ This is used for arrays, a, of the form (n_v, 2), where n_v is the number
        of visibilities.

        Parameters
        ----------
        a : type
            Description of parameter `a`.
        n_b : type
            The number of baselines (this is equal to, n_b = n_a * (n_a - 1) / 2,
            where n_a is the number of antennas).

        Returns
        -------
        type
            Description of returned object.

        """

        a_reshaped = a.reshape(int(a.shape[0] / n_b), n_b, a.shape[-1])

        return a_reshaped


    def reshape_f(f, n_b):

        f_reshaped = f.reshape(f.shape[0], int(f.shape[1] / n_b), n_b)

        return f_reshaped


    antennas_unique = np.unique(antennas)

    n_a = len(antennas_unique)

    # NOTE: This test will be usefull when analyzing real data, where some antennas
    # have been flagged.
    # TODO: WHAT IF ONE ANTENNA HAS BEEN FLAGGED???
    for n in range(n_a):
        if n not in antennas_unique:
            raise ValueError(
                "The n={} antenna is not in the list".format(n)
            )


    # # NOTE: The default method of computing the f matrix (slow).
    # # TODO: Compute this using numba
    # f = np.zeros(
    #     shape=(
    #         n_a,
    #         antennas.shape[0]
    #     )
    # )
    # for i in range(f.shape[0]):
    #     for j in range(f.shape[1]):
    #         if antennas[j, 0] == i:
    #             f[i, j] = +1.0
    #         if antennas[j, 1] == i:
    #             f[i, j] = -1.0

    n_b = int(n_a * (n_a - 1.0) / 2.0)

    antennas_reshaped = reshape(
        a=antennas, n_b=n_b
    )

    # NOTE: An alternative method of computing the f matrix. The comparison with
    # the default method has been made and the two methods agree.
    f_temp = np.zeros(
        shape=(n_a, n_b)
    )
    for i in range(f_temp.shape[0]):
        for j in range(f_temp.shape[1]):
            if antennas_reshaped[0, j, 0] == i:
                f_temp[i, j] = +1.0
            if antennas_reshaped[0, j, 1] == i:
                f_temp[i, j] = -1.0

    f = np.tile(f_temp, antennas_reshaped.shape[0])

    return f


def compute_A_matrix_from_f_and_C_matrices(f, C):
    """Short summary.

    Parameters
    ----------
    f : type
        Description of parameter `f`.
    C : type
        Description of parameter `C`.

    Returns
    -------
    type
        Description of returned object.

    """

    A = np.matmul(
        f,
        np.matmul(C, f.T)
    )

    # NOTE:
    # A = np.matmul(
    #     f,
    #     f.T
    # )

    return A


def compute_B_matrix_from_f_and_C_matrices(f, C):
    """Short summary.

    Parameters
    ----------
    f : type
        Description of parameter `f`.
    C : type
        Description of parameter `C`.

    Returns
    -------
    type
        Description of returned object.

    """

    B = np.matmul(f, C)

    # NOTE:
    #B = f

    return B


# def generate_stochastic_phase_errors(N_antennas, n, min, max, filename=None):
#
#     def normalize(a, min, max):
#
#         a_min = np.min(a)
#         a_max = np.max(a)
#
#         a_normalized = np.add(
#             np.multiply(
#                 np.divide(
#                     np.subtract(
#                         max,
#                         min
#                     ),
#                     np.subtract(
#                         a_max,
#                         a_min
#                     )
#                 ),
#                 np.subtract(
#                     a,
#                     a_min
#                 )
#             ),
#             min
#         )
#
#         return a_normalized
#
#     filename = "stochastic_phase_errors_n_{}.fits".format(n)
#
#     if os.path.isfile(filename):
#         phase_errors = fits.getdata(
#             filename=filename
#         )
#     else:
#         phase_errors = np.zeros(
#             shape=(N_antennas, n)
#         )
#         for i in range(phase_errors.shape[0]):
#             a = fbm(
#                 n=n - 1,
#                 hurst=0.75,
#                 length=1,
#                 method='daviesharte'
#             )
#
#             phase_errors[i, :] = normalize(
#                 a=a,
#                 min=min,
#                 max=max
#             )
#
#         fits.writeto(
#             filename=filename,
#             data=phase_errors
#         )
#
#     return phase_errors



def corrupt(model_data, phase_errors, f_T):
    """Short summary.

    Parameters
    ----------
    model_data : type
        Description of parameter `model_data`.
    phase_errors : type
        Description of parameter `phase_errors`.
    f_T : type
        The transpose of the f matrix.

    Returns
    -------
    type
        Description of returned object.

    """

    model_phases_corrupted = np.add(
        model_data.phases,
        np.matmul(
            f_T,
            phase_errors
        )
    )

    return al.Visibilities(
        visibilities_1d=np.stack(
            arrays=(
                np.multiply(
                    model_data.amplitudes,
                    np.cos(model_phases_corrupted)
                ),
                np.multiply(
                    model_data.amplitudes,
                    np.sin(model_phases_corrupted)
                )
            ),
            axis=-1
        )
    )


def calibrate(masked_dataset, model_data, x0=None, max_nfev=25):

    def least_squares_fun(phase_errors, data, model_data, sigma, f_T):

        def least_squares_fun_helper(data, model_data, sigma):

            return np.divide(
                np.subtract(
                    data,
                    model_data
                ),
                sigma
            )

        model_data_corrupted = corrupt(
            model_data=model_data,
            phase_errors=phase_errors,
            f_T=f_T
        )

        fun_real = least_squares_fun_helper(
            data=data[:, 0],
            model_data=model_data_corrupted[:, 0],
            sigma=sigma[:, 0]
        )
        fun_imag = least_squares_fun_helper(
            data=data[:, 1],
            model_data=model_data_corrupted[:, 1],
            sigma=sigma[:, 1]
        )

        return np.concatenate(
            [fun_real, fun_imag],
            axis=0
        )

    def least_squares_jac(phase_errors, data, model_data, sigma, f_T):

        model_data_corrupted = corrupt(
            model_data=model_data,
            phase_errors=phase_errors,
            f_T=f_T
        )

        jac_real_array = np.divide(
            model_data_corrupted[:, 1],
            sigma[:, 0]
        )
        jac_imag_array = np.divide(
            model_data_corrupted[:, 0],
            sigma[:, 1]
        )

        jac_real = np.multiply(
            f_T,
            jac_real_array[:, np.newaxis]
        )
        jac_imag = np.multiply(
            -f_T,
            jac_imag_array[:, np.newaxis]
        )

        jac = np.concatenate(
            [jac_real, jac_imag],
            axis=0
        )

        return jac


    if x0 is None:
        x0 = np.zeros(
            shape=phase_errors_approx.shape[0]
        )

    res = optimize.least_squares(
        least_squares_fun,
        x0=x0,
        jac=least_squares_jac,
        bounds=(-np.pi, np.pi),
        max_nfev=max_nfev,
        args=(
            masked_dataset.data,
            model_data,
            masked_dataset.sigma,
            masked_dataset.f_T,
        ),
        verbose=0
    )

    model_data_corrupted = corrupt(
        model_data=model_data,
        phase_errors=res.x,
        f_T=masked_dataset.f_T
    )




if __name__ == "__main__":

    pass

    from astropy import units, constants

    print((units.Hz / constants.c).to(1.0 / units.m));exit()
    import matplotlib.pyplot as plt
    from scipy.linalg import block_diag

    a = np.array([[3,1], [1,2]])
    #print(a)
    #exit()
    # a_block = np.block([a, a])
    # print(a_block)
    # exit()

    # a_block = np.block([
    #     [a,               np.zeros(shape=a.shape)],
    #     [np.zeros(shape=a.shape), a              ]
    # ])
    a_block = block_diag((*[a, a])) # NOTE: This is the same as the line above.
    # print(a_block)
    # plt.imshow(a_block, aspect="auto")
    # plt.show()
    # exit()

    b = np.array([9,8])
    b_block = np.block([b, b])

    #print(b_block);exit()

    b_block = []
    for block in [b,b]:
        b_block.extend(block)
    b_block = np.asarray(b_block)
    print(b_block);exit()
    # b_block = np.block([
    #     [b,               np.zeros(shape=b.shape)],
    #     [np.zeros(shape=b.shape), b              ]
    # ])

    x = np.linalg.solve(a, b)
    x_block = np.linalg.solve(a_block, b_block)
    print(x)
    print(x_block)
