import numpy as np


# TODO: Extend this function for ndarray.
def average_1d_array(array, n_elements):

    if len(array) % n_elements == 0:
        array_averaged = np.mean(
            a=array.reshape(-1, n_elements),
            axis=1
        )
    else:
        raise ValueError(
            "The length of the array is not divisible by {}".format(n_elements)
        )

    return array_averaged


# def average_nd_array(array, axis, n_elements=None):
#     if n_elements is None:
#         return np.average(array, axis)
#     else:
#         n_elements = int(n_elements)
#
#         # ...
#         new_shape = list(array.shape)
#         if array.shape[axis] % n_elements == 0:
#             new_shape[axis] = int(new_shape[axis] / n_elements)
#             new_shape.insert(axis+1, n_elements)
#             array_reshaped = array.reshape(new_shape)
#         else:
#             raise ValueError
#
#         return np.average(array_reshaped, axis=axis + 1)

def pad_image():
    pass

def pad_cube():
    pass

if __name__ == "__main__":

    a = np.ones(shape=(10, 2,2))
    a = np.pad(a, pad_width=(0, 2, 2), mode='constant', constant_values=0)
    print(a.shape)
