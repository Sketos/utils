import numpy as np

arr = np.array([
    [0,1,2,5],
    [3,4,5,2]
])

arr2 = np.array([2, 1])

print(arr / arr2[:, None])


def get_uv_wavelengths_from_ms(ms):
    pass
