import os
import sys
import matplotlib.pyplot as plt

sys.path.insert(
    0,
    os.environ["Galpak3D"]
)
import galpak


def create_model_cube(galaxy_model, galaxy_parameters, shape, dv):

    #zo = int(shape[0] / 2.0)

    # TODO: Check that galaxy_model is a galpak.galaxy_model object
    if not isinstance(galaxy_model, galpak.Model):
        raise ValueError

    # NOTE: Do we need the moment maps?
    cube, mom0, mom1, mom2 = galaxy_model._create_cube(
        galaxy_parameters, shape, dv, galaxy_parameters.z
    )

    # plt.figure()
    # plt.imshow(mom1)
    # plt.show()
    # exit()

    return cube


# TODO: Take as an input a galap.galaxy_parameters object and a dictionary of parameters and update the object using those
def update_galaxy_parameters(galaxy_parameters):
    pass



if __name__ == "__main__":

    print(galpak.Model)
