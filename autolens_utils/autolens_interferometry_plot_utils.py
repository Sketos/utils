

def plot_fit(fit):

    # NOTE: use fit.grid.extent
    extent = [
        np.min(fit.grid[:, 1]),
        np.max(fit.grid[:, 1]),
        np.max(fit.grid[:, 0]),
        np.min(fit.grid[:, 0])
    ]
