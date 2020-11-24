import numpy as np


def reshape(a, n_b):
    """
    The data are arranged in the following format,

    D = {
        V_{0, t_0}, V_{1, t_0}, ..., V_{M, t_0},
        V_{0, t_1}, V_{1, t_1}, ..., V_{M, t_1},
        .
        .
        .
        V_{0, t_n}, V_{1, t_n}, ..., V_{M, t_n}
    }

    where V_{i, t_j} is the visibility of the i'th baseline at the j'th time.

    Parameters
    ----------
    a : type
        Description of parameter `a`.
    n_b : type
        Description of parameter `n_b`.

    Returns
    -------
    type
        Description of returned object.

    """

    if len(a.shape) > 1:
        return a.reshape(
            (int(a.shape[0] / n_b), n_b, -1)
        )
    else:
        return a.reshape(
            (int(a.shape[0] / n_b), n_b)
        )


def reshape_reverse(a):

    if len(a.shape) > 2:
        return a.reshape(
            (int(a.shape[0] * a.shape[1]), -1)
        )
    else:
        return a.reshape(
            (int(a.shape[0] * a.shape[1]))
        )


def indexes(shape, n_b, n_t):

    def indexes_helper(shape, n_b, n_t):

        indexes_reshaped = reshape(
            a=np.zeros(
                shape=shape
            ),
            n_b=n_b
        )

        if indexes_reshaped.shape[0] % n_t != 0:
            raise ValueError("...")
        else:
            dn = int(
                np.divide(
                    indexes_reshaped.shape[0],
                    n_t
                )
            )

        n_i = 0
        for n in range(n_t):
            n_j = n_i + dn

            indexes_reshaped[int(n_i):int(n_j), ...] = n

            n_i = n_j

        return reshape_reverse(
            a=indexes_reshaped
        )

    idx = indexes_helper(
        shape=shape,
        n_b=n_b,
        n_t=n_t
    )

    indexes = np.zeros(
        shape=(
            n_t,
            int(idx.shape[0] / n_t)
        ),
        dtype=int
    )
    for n in range(n_t):
        indexes_n = np.where(
            idx == n
        )[0]

        indexes[n, :] = indexes_n

    return indexes


def indexing(a, n_b, n_t, idx=None):

    if idx is None:
        idx = indexes(
            shape=a.shape[:-1],
            n_b=n_b,
            n_t=n_t
        )

    a_indexed = np.zeros(
        shape=idx.shape + (a.shape[-1], )
    )

    for i in range(idx.shape[0]):
        a_indexed[i, ...] = a[idx[i], ...]

    return a_indexed


# def plot(a_indexed):
#     pass


if __name__ == "__main__":

    a = 8
    b = 3.2
    print(a % b)
