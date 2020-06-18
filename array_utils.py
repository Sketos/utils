import numpy as np


def reshape_array(array):

    return array.reshape(
        -1,
        array.shape[-1]
    )


if __name__ == "__main__":
    array1 = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
    array2 = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
    array3 = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])
    array4 = np.array([[0.0, 1.0], [0.0, 1.0], [0.0, 1.0], [0.0, 1.0]])



    # arrays = np.empty(0)
    # arrays = np.append(arrays, array1)
    # arrays = np.append(arrays, array2)
    #
    # #arrays = np.array([array1, array2, array3, array4])
    # #print(array1.shape)
    # print(arrays.shape)

    arrays = []
    arrays.append(array1)
    arrays.append(array2)
    arrays.append(array3)

    print(np.shape(arrays))
    arrays = np.asarray(arrays)
    print(np.shape(arrays))
    #d = (arrays[i] for i in range(arrays.shape[0])

    arrays_concatenated = np.concatenate(tuple(arrays[i] for i in range(np.shape(arrays)[0])), axis=0)
    print(arrays_concatenated.shape)
