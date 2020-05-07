import numpy as np




class Image:
    def __init__(self, array_2d, mask=None):
        self.array_2d = array_2d
        self.mask = mask

    @property
    def in_1d_binned(self):
        return np.ndarray.flatten(self.array_2d)


class Cube:
    def __init__(self):
        pass


# def multiprocessing_map_function(args):
#
#     uv_wavelengths, grid, image, n = args
#
#     transformer = al.TransformerDFT(
#         uv_wavelengths=uv_wavelengths,
#         grid=grid,
#         preload_transform=False
#     )
#
#     visibilities = transformer.visibilities_from_image(
#         image=image
#     )
#
#     return visibilities


# NOTE: THE FOLLOWING FUNCTIONS CAN NOT BE IMPORTED CAUSE OF THE DECORATOR_UTIL.
"""
import decorator_util as decorator_util

@decorator_util.jit()
def preload_real_transforms_inverse(grid_radians, uv_wavelengths):

    preloaded_real_transforms_inverse = np.zeros(
        shape=(grid_radians.shape[0], uv_wavelengths.shape[0])
    )

    for image_1d_index in range(grid_radians.shape[0]):
        for vis_1d_index in range(uv_wavelengths.shape[0]):
            preloaded_real_transforms_inverse[image_1d_index, vis_1d_index] += np.cos(
                2.0
                * np.pi
                * (
                    grid_radians[image_1d_index, 1] * uv_wavelengths[vis_1d_index, 0]
                    + grid_radians[image_1d_index, 0] * uv_wavelengths[vis_1d_index, 1]
                )
            )

    return preloaded_real_transforms_inverse


@decorator_util.jit()
def preload_imag_transforms_inverse(grid_radians, uv_wavelengths):

    preloaded_imag_transforms_inverse = np.zeros(
        shape=(grid_radians.shape[0], uv_wavelengths.shape[0])
    )

    for image_1d_index in range(grid_radians.shape[0]):
        for vis_1d_index in range(uv_wavelengths.shape[0]):
            preloaded_imag_transforms_inverse[image_1d_index, vis_1d_index] += np.sin(
                2.0
                * np.pi
                * (
                    grid_radians[image_1d_index, 1] * uv_wavelengths[vis_1d_index, 0]
                    + grid_radians[image_1d_index, 0] * uv_wavelengths[vis_1d_index, 1]
                )
            )

    return preloaded_imag_transforms_inverse


@decorator_util.jit()
def image_from_visibilities_via_preload_jit(image_1d_shape, real_visibilities, imag_visibilities, preloaded_reals, preloaded_imags):

    image_1d = np.zeros(shape=image_1d_shape)

    for image_1d_index in range(image_1d.shape[0]):
        for vis_1d_index in range(preloaded_reals.shape[1]):
            image_1d[image_1d_index] += real_visibilities[vis_1d_index] * preloaded_reals[image_1d_index, vis_1d_index]
            image_1d[image_1d_index] += imag_visibilities[vis_1d_index] * preloaded_imags[image_1d_index, vis_1d_index]

    # NOTE : This is an alternative way of doing the calculation. (There seems to be a 10**-14 difference between this method and "imag_visibilities_jit")
    # for image_1d_index in range(image_1d.shape[0]):
    #     for vis_1d_index in range(preloaded_reals.shape[1]):
    #         image_1d[image_1d_index] += real_visibilities[vis_1d_index] * preloaded_reals[image_1d_index, vis_1d_index]
    #
    # for image_1d_index in range(image_1d.shape[0]):
    #     for vis_1d_index in range(preloaded_imags.shape[1]):
    #         image_1d[image_1d_index] += imag_visibilities[vis_1d_index] * preloaded_imags[image_1d_index, vis_1d_index]

    return image_1d


@decorator_util.jit()
def image_from_visibilities_jit(image_1d_shape, grid_radians, uv_wavelengths, real_visibilities, imag_visibilities):

    image_1d = np.zeros(shape=image_1d_shape)

    for image_1d_index in range(image_1d.shape[0]):
        for vis_1d_index in range(uv_wavelengths.shape[0]):
            image_1d[image_1d_index] += real_visibilities[vis_1d_index] * np.cos(
                2.0
                * np.pi
                * (
                    grid_radians[image_1d_index, 1] * uv_wavelengths[vis_1d_index, 0]
                    + grid_radians[image_1d_index, 0] * uv_wavelengths[vis_1d_index, 1]
                )
            )

            image_1d[image_1d_index] -= imag_visibilities[vis_1d_index] * np.sin(
                2.0
                * np.pi
                * (
                    grid_radians[image_1d_index, 1] * uv_wavelengths[vis_1d_index, 0]
                    + grid_radians[image_1d_index, 0] * uv_wavelengths[vis_1d_index, 1]
                )
            )

    return image_1d


# def image_from_visibilities(self, real_visibilities, imag_visibilities):
#
#         if self.preload_transform:
#
#             return transformer_util.image_from_visibilities_via_preload_jit(
#                 image_1d_shape=self.total_image_pixels,
#                 real_visibilities=real_visibilities,
#                 imag_visibilities=imag_visibilities,
#                 preloaded_reals=self.preload_real_transforms,
#                 preloaded_imags=self.preload_imag_transforms
#             )
#         else:
#             return transformer_util.image_from_visibilities_jit(
#                 image_1d_shape=self.total_image_pixels,
#                 grid_radians=self.grid_radians,
#                 uv_wavelengths=self.uv_wavelengths,
#                 real_visibilities=real_visibilities,
#                 imag_visibilities=imag_visibilities
#             )
"""

if __name__ == "__main__":


    image = Image(
        array_2d=np.zeros(shape=(10, 10))
    )

    print(image.in_1d_binned)
