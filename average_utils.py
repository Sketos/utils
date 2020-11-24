import numpy as np


def average(a, axis, n_elements=None):
    """Short summary.

    Parameters
    ----------
    a : type
        Description of parameter `a`.
    axis : type
        Description of parameter `axis`.
    n_elements : type
        Description of parameter `n_elements`.

    Returns
    -------
    type
        Description of returned object.

    """

    if n_elements is None:
        return np.average(a, axis)
    else:
        n_elements = int(n_elements)

        # ...
        new_shape = list(a.shape)
        if a.shape[axis] % n_elements == 0:
            new_shape[axis] = int(new_shape[axis] / n_elements)
            new_shape.insert(axis + 1, n_elements)
            #print("new_shape = ", new_shape);exit()
            a_reshaped = a.reshape(new_shape)
        else:
            raise ValueError(
                "The length, n={}, of the array, for axis = {}, must be a multiple of n={}".format(
                    a.shape[axis],
                    axis,
                    n_elements
                )
            )

        return np.average(a_reshaped, axis=axis + 1)



def sum_updated(array, axis, n_elements=None):
    if n_elements is None:
        return np.sum(
            array,
            axis=axis
        )
    else:
        n_elements = int(n_elements)

        # ...
        new_shape = list(array.shape)
        if array.shape[axis] % n_elements == 0:
            new_shape[axis] = int(new_shape[axis] / n_elements)
            new_shape.insert(axis+1, n_elements)
            array_reshaped = array.reshape(new_shape)
        else:
            raise ValueError("...")

        return np.sum(array_reshaped, axis=axis + 1)


def rms(array, axis, n_elements=None):
    if n_elements is None:
        return np.sqrt(
            np.sum(
                array**2.0,
                axis=axis
            )
        )
    else:
        return np.sqrt(
            sum_updated(
                array**2.0,
                axis=axis,
                n_elements=n_elements
            )
        )


def average_sigma(sigma, axis, n_elements=None):

    return np.divide(
        rms(
            array=sigma,
            axis=axis,
            n_elements=n_elements
        ),
        np.sqrt(n_elements)
    )


if __name__ == "__main__":


    a = np.random.random(size=(4, 5))
    # print(a)
    # print(a.shape)
    # a_averaged = average(a=a, axis=0, n_elements=2)
    # print(a_averaged.shape)
    # print(a_averaged)

    a_summed = average(a=a, axis=0, n_elements=2)
    print(
        "a = ", a
    )
    print("\n")
    print(a_summed)
    # sigma_a = np.random.random(size=(10, ))
    #
    # print(
    #     np.sqrt(np.sum(np.square(sigma_a)) / len(sigma_a))
    # )
