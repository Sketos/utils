import numpy as np


def reshape(a, axis, shape):

    # NOTE: If I put axis=-1 this DOES NOT WORK ...

    # NOTE: shape must be an array?
    a_shape = a.shape

    a_shape_axis = a_shape[axis]



    if a_shape_axis == np.prod(shape):
        a_shape_new = sum([a_shape[:axis], shape, a_shape[axis + 1:]], ())
        a_reshaped = a.reshape(a_shape_new)
    else:
        raise ValueError("...")

    return a_reshaped


def reshape_axes(a, axes):

    if len(axes) == 2:
        i, j = axes

        if i + 1 == j:
            a_shape = a.shape

            if i > 0 and j < len(a_shape):

                if j == len(a_shape) - 1:
                    new_shape = a_shape[:i] + (int(a_shape[i] * a_shape[j]), )
                else:
                    new_shape = a_shape[:i] + (int(a_shape[i] * a_shape[j]), ) + a_shape[j + 1:]

        else:
            raise ValueError("This is not valid")

    else:
        raise ValueError("This is not valid")

    return a.reshape(new_shape)


if __name__ == "__main__":


    """
    a = np.random.random(size=(2, 128, 1000, 2))
    #print(a.shape)

    a_reshaped = a.reshape(2, int(128 * 1000), 2)

    # a_reshaped = reshape(a=a, axis=2, shape=(2, 500))
    # print(a_reshaped.shape)
    #
    # a_reshaped_inverse = reshape_inverse(a=a, axes=[1, 2])
    # print(a_reshaped_inverse.shape)
    # a_reshaped = a.reshape([2, 128, 500, 2, 2])
    # print(a_reshaped.shape)
    """


    a = np.random.random(size=(2, 3, 2, 5))
    print(a)

    a_reshaped = reshape_axes(a=a, axes=[1, 2])
    print(a_reshaped)
