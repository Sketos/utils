import time
import numpy as np
import matplotlib.pyplot as plt

from scipy import interpolate

from itertools import compress

import autolens as al


def visibilities_from_cube(cube, transformers, shape):

    # NOTE: Check that the shape of the uv_wavelengths in the transformers is the
    # same as the input shape.

    class Image:
        def __init__(self, array_2d):
            self.array_2d = array_2d

        @property
        def in_1d_binned(self):
            return np.ndarray.flatten(self.array_2d)

        @property
        def in_2d_binned(self):
            return self.array_2d

    if len(transformers) == shape[0]:

        visibilities = np.zeros(shape=shape)
        for i in range(shape[0]):
            visibilities[i] = transformers[i].visibilities_from_image(
                image=Image(array_2d=cube[i])
            )

    else:
        raise ValueError("shape mismatch")

    return visibilities


def visibilities_from_image_and_uv_wavelengths(image, uv_wavelengths, grid, transformer_class):

    # NOTE: Image must be a class

    if len(uv_wavelengths.shape) == 2:

        transformer = transformer_class(
            uv_wavelengths=uv_wavelengths,
            grid=grid.in_radians,
        )

        visibilities = transformer.visibilities_from_image(
            image=image
        )

    if len(uv_wavelengths.shape) == 3:

        transformers = [
            transformer_class(
                uv_wavelengths=uv_wavelengths[i],
                grid=grid.in_radians,
            )
            for i in range(uv_wavelengths.shape[0])
        ]

        visibilities = np.zeros(
            shape=uv_wavelengths.shape
        )
        for i in range(uv_wavelengths.shape[0]):
            visibilities[i, ...] = transformers[i].visibilities_from_image(
                image=image
            )

    if len(uv_wavelengths.shape) == 4:

        raise ValueError("This has not been implemented yet")

    return visibilities















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


# def lensed_cube_from_galaxies(galaxies, grid, cube, interpolator=None):
#     pass


def mapper_from_tracer_and_grid(tracer, grid):

    mappers_of_planes = tracer.mappers_of_planes_from_grid(
        grid=grid,
    )

    return mappers_of_planes[-1]


def transformed_mapping_matrices_from_transformer_grid_and_tracer(transformer, grid, tracer):

    mapper = mapper_from_tracer_and_grid(
        tracer=tracer,
        grid=grid
    )

    return transformer.transformed_mapping_matrices_from_mapping_matrix(
        mapping_matrix=mapper.mapping_matrix
    )


# TODO: A LOT TO-DO
def get_parameter_from_tracer(tracer, parameter_name="centre"):

    for mass_profile in tracer.mass_profiles:

        if mass_profile.__class__.__name__ in [
            "EllipticalPowerLaw",
            "EllipticalIsothermal"
        ]:

            parameter = getattr(
                mass_profile,
                parameter_name
            )

    return parameter


def galaxies_with_mass_profiles_from_tracer(tracer):

    return list(
        compress(
            tracer.galaxies,
            list(map(lambda galaxy: galaxy.has_mass_profile, tracer.galaxies)))
    )


def galaxies_have_mass_profiles(galaxies):

    return all(list(map(lambda galaxy: galaxy.has_mass_profile, galaxies)))


def tracer_from_len_galaxies_and_src_galaxy_with_pixelization(len_galaxies, src_galaxy):

    if not isinstance(src_galaxy, al.Galaxy):
        raise ValueError(
            "The input must be an al.Galaxy class"
        )

    if src_galaxy.has_pixelization:
        if galaxies_have_mass_profiles(
            galaxies=len_galaxies
        ):
            galaxies = len_galaxies + [src_galaxy, ]
        else:
            raise ValueError(
                "Not all galaxies have mass profiles"
            )

            # NOTE: Diagnostics
    else:
        raise ValueError(
            "The \'src_galaxy\' does not have a pixelization"
        )

    return al.Tracer.from_galaxies(
        galaxies=galaxies
    )




def planes_with_light_profiles(tracer):

    """

    1) Find all planes with light profiles.

    2) Get the galaxies of these planes.

    3) Get the light profiles of those galaxies.

    4) Make images of all those light profiles.

    """
    # NOTE: Find all planes with light profiles
    # NOTE:
    # # image = tracer.galaxies[1].profile_image_from_grid(grid=grid)
    # # plt.figure()
    # # plt.imshow(image.in_2d)
    # # plt.show()
    #
    # # asd = list(map(lambda plane: plane.has_light_profile, tracer.planes))
    # # print(asd)
    # #print(tracer.planes)
    #
    # #print(tracer.has_light_profile)
    # #print(list(map(lambda plane: plane.has_light_profile, tracer.planes)))
    # #print(tracer.galaxies_with_light_profile)
    #
    # #print(tracer.planes[1].galaxies_with_light_profile)
    #
    # galaxies = tracer.planes[1].galaxies_with_light_profile
    # galaxy = galaxies[0]
    #
    # galaxy_light_profiles = galaxy.light_profiles
    #
    # image_0 = galaxy_light_profiles[0].profile_image_from_grid(grid=grid)
    # image_0_in_2d = image_0.in_2d
    #
    # image_1 = galaxy_light_profiles[1].profile_image_from_grid(grid=grid)
    # image_1_in_2d = image_1.in_2d


# al.Galaxy(
#     redshift=src_redshift,
#     pixelization=pixelization,
#     regularization=al.reg.Constant(
#         coefficient=1000000.0
#     ),
# )
