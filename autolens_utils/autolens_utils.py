import numpy as np

import autofit as af
import autolens as al


# def get_config_path(autolens_version):
#
#     if autolens_version is None:
#         raise ValueError
#     elif autolens_version in [
#         "0.40.0"
#     ]:
#         pass
#     else:
#         raise ValueError
#
#     "config_" + autolens_version


def figure_of_merit_from_interferometer_and_tracer(interferometer, transformer_class, grid, tracer):

    masked_interferometer = al.MaskedInterferometer(
        interferometer=interferometer,
        visibilities_mask=np.full(
            shape=interferometer.visibilities.shape, fill_value=False
        ),
        real_space_mask=al.Mask.unmasked(
            shape_2d=grid.shape_2d,
            pixel_scales=grid.pixel_scales,
            sub_size=grid.sub_size
        ),
        transformer_class=transformer_class
    )

    fit = al.FitInterferometer(
        masked_interferometer=masked_interferometer,
        tracer=tracer
    )

    return fit.figure_of_merit


class Image:
    def __init__(self, array_2d):
        self.array_2d = array_2d

    @property
    def in_1d_binned(self):
        return np.ndarray.flatten(self.array_2d)
