import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


def add_colorbar_to_axes(figure, im, axes):

    # TODO: Make an example to demonstrate how to use this function

    cax = make_axes_locatable(
        axes
    ).append_axes('right', size='5%', pad=0.05)

    figure.colorbar(
        im,
        cax=cax,
        orientation='vertical'
    )


if __name__ == "__main__":
    pass
