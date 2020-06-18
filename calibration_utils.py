import numpy as np

def wrap(a):

    return (a + np.pi) % (2.0 * np.pi) - np.pi


def phase_errors_from_A_and_B_matrices(phases, model_phases, A, B):

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


def compute_f_matrix_from_antennas(antennas):

    f = np.zeros(
        shape=(
            len(np.unique(antennas)),
            antennas.shape[0]
        )
    )

    # TODO: compute this using numba
    for i in range(f.shape[0]):
        for j in range(f.shape[1]):
            if antennas[j, 0] == i:
                f[i,j] = +1.0
            if antennas[j, 1] == i:
                f[i,j] = -1.0

    return f


def compute_A_matrix_from_f_and_C_matrices(f, C):

    A = np.matmul(
        f,
        np.matmul(C, f.T)
    )

    return A


def compute_B_matrix_from_f_and_C_matrices(f, C):

    B = np.matmul(f, C)

    return B






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
