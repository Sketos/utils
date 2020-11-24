import numpy as np

def compute_baselines_from_antenna_positions(antenna_positions):

    # NOTE: Check if antenna positions have the required shape ...
    x, y, z = antenna_positions

    baselines = np.zeros(
        shape=int(antenna_positions.shape[1] * (antenna_positions.shape[1] - 1) / 2.0)
    )

    n = 0
    for i in np.arange(0, antenna_positions.shape[1]):
        for j in np.arange(i + 1, antenna_positions.shape[1]):
            baselines[n] = np.sqrt(
                (x[i] - x[j])**2.0 + (y[i] - y[j])**2.0 + (z[i] - z[j])**2.0
            )
            n += 1

    return baselines
