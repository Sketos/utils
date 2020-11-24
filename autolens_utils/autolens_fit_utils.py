import numpy as np

import autolens as al


# def fit_from_masked_dataset_model_data_and_inversion(masked_dataset, model_data, inversion):
#     pass

def fit(interferometer, tracer, grid, real_space_mask=None, transformer_class=al.TransformerNUFFT):

    if real_space_mask is None:
        real_space_mask = al.Mask.unmasked(
            shape_2d=grid.shape_2d,
            pixel_scales=grid.pixel_scales,
            sub_size=grid.sub_size,
        )
    else:
        pass # TODO: check that grid and mask have the same pixel_scale and shape_2d

    return al.FitInterferometer(
        masked_interferometer=al.MaskedInterferometer(
            interferometer=interferometer,
            visibilities_mask=np.full(
                shape=interferometer.visibilities.shape,
                fill_value=False
            ),
            real_space_mask=real_space_mask,
            transformer_class=al.TransformerNUFFT
        ),
        tracer=tracer
    )
