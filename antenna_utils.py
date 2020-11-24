import numpy as np


def shift_antenna_positions(antenna_positions):

    x, y, z = antenna_positions

    x_antenna_position = x - np.mean(x)
    y_antenna_position = y - np.mean(y)
    z_antenna_position = z - np.mean(z)
    x_antenna_position += -np.min(x_antenna_position) + np.std(x_antenna_position)
    y_antenna_position += -np.min(y_antenna_position) + np.std(y_antenna_position)
    z_antenna_position += -np.min(z_antenna_position) + np.std(z_antenna_position)

    return np.array([
        x_antenna_position,
        y_antenna_position,
        z_antenna_position
    ])
