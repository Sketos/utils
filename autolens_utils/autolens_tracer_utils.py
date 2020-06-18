import time
import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate

import autolens as al


# NOTE: This works regardless of how many galaxies are used in the tracer
# NOTE: The spped of this function can not improve by means of saving the weights of the interpolation
def ray_trace(traced_grids_of_planes, image, interpolator=None):

    traced_grid_i = traced_grids_of_planes[0]
    traced_grid_j = traced_grids_of_planes[1]

    x_interp = np.unique(traced_grid_i[:, 0])
    y_interp = np.unique(traced_grid_i[:, 1])

    #start = time.time()
    image_interp = interpolate.RegularGridInterpolator(
        points=(y_interp, x_interp),
        values=image[::-1, :],
        method="linear",
        bounds_error=False,
        fill_value=0.0
    )

    lensed_image = image_interp(traced_grid_j).reshape(image.shape)
    #end = time.time()
    #print(end - start)

    # NOTE: check autoarray/grids.py -> interpolator (I am not sure if it's going to be faster)
    # lensed_image = interpolate.griddata(
    #     points=traced_grid_i,
    #     values=np.ndarray.flatten(image[:, :]),
    #     xi=traced_grid_j,
    #     method="linear",
    # )
    # lensed_image = lensed_image.reshape(image.shape)

    return lensed_image





# def tracer(lens_galaxy, source_redshift):
#
#     # NOTE: Do I need to check anything about the lens_galaxy?
#
#     tracer = al.Tracer.from_galaxies(
#         galaxies=[
#             lens_galaxy,
#             al.Galaxy(
#                 redshift=source_redshift,
#                 light=al.lp.LightProfile()
#             )
#         ]
#     )
#
#     return tracer

"""
# NOTE: Rename to get_lensed_image_from_image_and_tracer
def func_image(lens_galaxy, source_redshift, grid, image):

    tracer = al.Tracer.from_galaxies(
        galaxies=[
            lens_galaxy,
            al.Galaxy(
                redshift=source_redshift,
                light=al.lp.LightProfile()
            )
        ]
    )

    traced_grids_of_planes = tracer.traced_grids_of_planes_from_grid(
        grid=grid,
        plane_index_limit=tracer.upper_plane_index_with_light_profile
    )

    lensed_image = ray_trace(
        traced_grids_of_planes=traced_grids_of_planes,
        image=image
    )

    return lensed_image


def func_cube(lens_galaxy, source_redshift, grid, cube, interpolator=None):

    tracer = al.Tracer.from_galaxies(
        galaxies=[
            lens_galaxy,
            al.Galaxy(
                redshift=source_redshift,
                light=al.lp.LightProfile()
            )
        ]
    )

    return lensed_cube_from_tracer(
        tracer=tracer,
        grid=grid,
        cube=cube,
        interpolator=interpolator
    )
"""


def lensed_image_from_tracer(tracer, grid, image, interpolator=None):

    traced_grids_of_planes = tracer.traced_grids_of_planes_from_grid(
        grid=grid,
        plane_index_limit=tracer.upper_plane_index_with_light_profile
    )

    lensed_image = ray_trace(
        traced_grids_of_planes=traced_grids_of_planes,
        image=image
    )

    return lensed_image


def lensed_cube_from_tracer(tracer, grid, cube, interpolator=None):

    traced_grids_of_planes = tracer.traced_grids_of_planes_from_grid(
        grid=grid,
        plane_index_limit=tracer.upper_plane_index_with_light_profile
    )

    # start = time.time()
    lensed_cube = np.zeros(
        shape=cube.shape
    )
    for i in range(lensed_cube.shape[0]):

        lensed_cube[i] = ray_trace(
            traced_grids_of_planes=traced_grids_of_planes,
            image=cube[i]
        )
    # end = time.time()
    # print("Total time:", end - start)
    # exit()

    return lensed_cube


def lensed_cube_from_galaxies(galaxies, grid, cube, interpolator=None):
    pass
