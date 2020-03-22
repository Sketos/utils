import os
import sys


sys.path.insert(
    0,
    os.environ["Galpak3D"]
)
import galpak


def create_model_cube(galaxy_model, galaxy_parameters, shape, dv):

    #zo = int(shape[0] / 2.0)

    cube, mom0, mom1, mom2 = galaxy_model._create_cube(
        galaxy_parameters, shape, dv, galaxy_parameters.z
    )

    return cube
