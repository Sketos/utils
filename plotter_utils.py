import numpy as np

import matplotlib.pyplot as plt


class plotter:

    def __init__(
        self,
        figsize=figsize
    ):

        self.figure = plt.figure()
        self.axes = None


class subplotter:

    def __init__(
        self,
        nrows=nrows,
        ncols=ncols,
        figsize=figsize
    ):

        self.figure, self.axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=figsize
        )


if __name__ = "__main__":

    def plot_array(array, baseclass):

        if baseclass.axes == None:
            pass 

    plot_array(
        array=np.random.normal(size=(100, 2)), baseclass=plotter()
    )
