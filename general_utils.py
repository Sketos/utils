import numpy as np


def concatenate_list_of_numpy_arrays(list_of_arrays, axis=0):

    if not all(
        [isinstance(array, np.ndarray) for array in list_of_arrays]
    ):
        raise ValueError("All elements of the list must be numpy arrays")

    else:
        if len(set([len(x.shape) for x in list_of_arrays])) == 1:
            concatenated_array = np.zeros(
                shape=list_of_arrays[0].shape
            )
            for i in range(len(list_of_arrays)):
                concatenated_array = np.concatenate(
                    tuple(list_of_arrays),
                    axis=axis
                )
        else:
            raise ValueError(
                "All arrays in the list must have the same shape length"
            )

    print(
        "The shape of the concatenated array is: {}".format(
            concatenated_array.shape
        )
    )
    return concatenated_array


def average_list_of_numpy_arrays(list_of_arrays, axis=0):

    if not all(
        [isinstance(array, np.ndarray) for array in list_of_arrays]
    ):
        raise ValueError("All elements of the list must be numpy arrays")

    else:
        if len(set([len(x.shape) for x in list_of_arrays])) == 1:
            concatenated_array = np.zeros(
                shape=list_of_arrays[0].shape
            )
            for i in range(len(list_of_arrays)):
                concatenated_array = np.concatenate(
                    tuple(list_of_arrays),
                    axis=axis
                )
        else:
            raise ValueError(
                "All arrays in the list must have the same shape length"
            )

    print(
        "The shape of the concatenated array is: {}".format(
            concatenated_array.shape
        )
    )
    return concatenated_array


def check_if_number_is_even(number):
    if (number % 2) == 0:
        return True
    return False
