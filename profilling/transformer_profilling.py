import os
import sys
import time

import numpy as np

import matplotlib.pyplot as plt

from astropy.io import fits




def paths(autolens_version, cosma_server="7"):

    config_path = "./config_{}".format(
        autolens_version
    )
    if os.environ["HOME"].startswith("/cosma"):
        suffix = "host"
    else:
        suffix = "local"

    output_path = "{}/simulations/output".format(
        os.environ["COSMA{}_DATA_{}".format(cosma_server, suffix)]
    )

    return config_path, output_path

autolens_version = "0.45.0"
config_path, output_path = paths(
    autolens_version=autolens_version
)


import autofit as af
af.conf.instance = af.conf.Config(
    config_path=config_path,
    output_path=output_path
)
import autolens as al


if __name__ == "__main__":



    n_pixels = 256
    pixel_scale = 0.025

    grid = al.Grid.uniform(
        shape_2d=(
            n_pixels,
            n_pixels
        ),
        pixel_scales=(
            pixel_scale,
            pixel_scale
        ),
        sub_size=1
    )

    uv_wavelengths = np.random.normal(size=(2, 10000))

    # transformer = transformer_class(
    #     uv_wavelengths=uv_wavelengths,
    #     grid=grid.in_radians,
    # )
    #
    # time_i = time.time()
    # visibilities = tracer.profile_visibilities_from_grid_and_transformer(
    #     grid=grid, transformer=transformer
    # )
    # time_j = time.time()

    source = al.Galaxy(
        redshift=0.5,
        light=al.lp.EllipticalSersic(
            centre=(0.01, 0.0),
            axis_ratio=0.4,
            phi=100.0,
            intensity=0.000001,
            effective_radius=0.15,
            sersic_index=1.0,
        ),
    )

    lens = al.Galaxy(
        redshift=1.0,
        mass=al.mp.EllipticalPowerLaw(
            centre=(0.0, 0.05),
            axis_ratio=0.75,
            phi=45.0,
            einstein_radius=1.0,
            slope=2.0
        ),
    )

    tracer = al.Tracer.from_galaxies(
        galaxies=[lens, source]
    )


    def profilling(uv_wavelengths, grid, transformer_class_1, transformer_class_2, tracer):

        transformer_1 = transformer_class_1(
            uv_wavelengths=uv_wavelengths,
            grid=grid.in_radians,
        )

        transformer_2 = transformer_class_2(
            uv_wavelengths=uv_wavelengths,
            grid=grid.in_radians,
        )

        time_i = time.time()
        visibilities = tracer.profile_visibilities_from_grid_and_transformer(
            grid=grid, transformer=transformer_1
        )
        time_j = time.time()
        print(time_j - time_i)

        time_i = time.time()
        visibilities = tracer.profile_visibilities_from_grid_and_transformer(
            grid=grid, transformer=transformer_2
        )
        time_j = time.time()
        print(time_j - time_i)

    profilling(
        uv_wavelengths=uv_wavelengths,
        grid=grid,
        transformer_class_1=al.TransformerNUFFT,
        transformer_class_2=al.TransformerDFT,
        tracer=tracer
    )
