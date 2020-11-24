import numpy as np
import matplotlib.pyplot as plt


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


def average(a, mask=None, axis=0):

    return np.average(a=a[mask.astype(np.bool)], axis=axis)


# TODO: Write a function that determines if a is a scalar or a list/array/tuple
def isscalar(a):
    pass



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
    pass

    a = np.arange(12).reshape(2, 6)
    print(a)

    a_tiled = np.tile(a, 2)
    print(a_tiled)

    # a = np.ones(shape=(4, 3))
    #
    # # a = np.column_stack((a, np.zeros(shape=(a.shape[0], ))))
    # # a = np.vstack((a, np.zeros(shape=(a.shape[1], ))))
    # # #a = np.vstack((a, np.zeros(a.shape[1])))
    #
    # a = np.pad(a, (1, 1), 'constant')
    #
    # print(a)
    # print(a.shape)





    # a = 3.0 + 1j * 2.0
    # print(np.abs(a))

    # a = np.ones(shape=(10, 2,2))
    # a = np.pad(a, pad_width=(0, 2, 2), mode='constant', constant_values=0)
    # print(a.shape)



    # a = np.random.normal(0.0, 1.0, size=10)
    #
    # a[100] = 0.0
    # mask = np.ones(shape=a.shape)
    # mask[:int(a.shape[0]/2.0)] = 0
    # #print(a, a[mask])
    # a_masked = a[mask.astype(np.bool)]
    # print(
    #     np.average(a_masked),
    #     average(a=a, mask=mask, axis=0)
    # )

    # a = np.random.normal(0.0, 1.0, size=(10, 2))
    # a_complex = a[:, 0] + 1j * a[:, 1]
    # b = np.random.normal(0.0, 1.0, size=(10, 2))
    # b_complex = a[:, 0] + 1j * a[:, 1]
    #
    # print(np.multiply(a_complex, b_complex))
    # # #print(a.shape)
    # # print(np.linalg.norm(a_complex))
    # # # a = a.view(dtype=np.complex128)
    # # # print(a)

    # a = np.arange(12)
    #
    # print(a.reshape(4,3))


    # z = 2.0 + 1j * 5.0
    #
    # print(np.abs(z), np.linalg.norm(z), np.hypot(z.real, z.imag))


    # data = np.random.normal(1.0, 0.05, size=(100,))
    # model_data = np.ones(shape=(100, ))
    # mask = data<1.0
    #
    # y = np.subtract(
    #     data, model_data, out=np.zeros_like(data) + 1, where=np.asarray(mask) == 0
    # )
    #
    #
    # plt.plot(data)
    # plt.plot(model_data)
    # plt.plot(y)
    # plt.show()


    # NOTE: TEST
    # N_c = 100
    # N_p = 20
    # velocities = np.arange(100)
    # velocities = velocities[:, None, None]
    # print(velocities.shape)
    #
    # cube = np.zeros(shape=(N_c, N_p, N_p))
    #
    # a = (cube - velocities)**2.0
    #
    # print(a)
    #
    # for i in range(cube.shape[0]):
    #
    #     plt.figure()
    #     plt.imshow(a[i, :, :])
    #     plt.show()

    # N = 3
    # a_real = np.random.random(size=(N, N))
    # a_imag = np.random.random(size=(N, N))
    #
    # a = a_real + 1j * a_imag
    #
    # a_diag = np.diag(a)
    # print(a)
    # print(a_diag)
