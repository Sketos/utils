import numpy as np


# NOTE:
def average_sigma(sigma, mask=None, axis=0):

    if mask is not None:
        sigma_masked = sigma[mask.astype(np.bool)]
    else:
        sigma_masked = sigma

    return np.divide(
        np.sqrt(
            np.sum(
                sigma_masked**2.0,
                axis=axis
            )
        ),
        sigma_masked.shape[axis]
    )
