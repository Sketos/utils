import numpy as np
from astropy import modeling

# NOTE : "fitting_dirty_beam_with_2D_Gaussian.py"
# def Gaussian2D_astropy_wrapper(shape_2d, amplitude, x_mean, y_mean, x_stddev, y_stddev, theta):
#     print(shape_2d, amplitude, x_mean, y_mean, x_stddev, y_stddev, theta)
#     # if shape_2d:
#     #     n_pixels_x, n_pixels_y = shape_2d
#     # else:
#     #     raise ValueError
#     n_pixels_x, n_pixels_y = shape_2d
#     x = np.arange(n_pixels_x)
#     y = np.arange(n_pixels_y)
#     x_meshgrid, y_meshgrid = np.meshgrid(x, y)
#
#     # ...
#     Gaussian2D = modeling.models.Gaussian2D(
#         amplitude=amplitude,
#         x_mean=x_mean,
#         y_mean=y_mean,
#         x_stddev=x_stddev,
#         y_stddev=y_stddev,
#         theta=theta
#     )
#
#     return Gaussian2D(
#         x_meshgrid,
#         y_meshgrid
#     )
