import numpy as np

import matplotlib.pyplot as plt

from scipy import optimize, stats, special

from astropy import units


def gaussian(
    x,
    A,
    x0,
    sigma
):

    return A * np.exp(-(x - x0)**2.0 / (2.0 * sigma**2.0))


def gaussian_with_continuum(
    x,
    A,
    x0,
    sigma,
    A_continuum=0.0
):

    return gaussian(x=x, A=A, x0=x0, sigma=sigma) + A_continuum


def cumulative_gaussian(x, A, x0, sigma, a=1.0):

    return A * sigma * np.sqrt(np.pi / 2.0) * (1.0 + special.erf(a * (x - x0) / (sigma * np.sqrt(2.0))))


def gaussian_skewed(x, A, x0, sigma, a):

    return 2.0 * gaussian(x=x, A=A, x0=x0, sigma=sigma) * cumulative_gaussian(x=x, A=A, x0=x0, sigma=sigma, a=a)


def gaussian_x2(x, A_1, x0_1, sigma_1, A_2, x0_2, sigma_2):

    return np.add(
        gaussian(x=x, A=A_1, x0=x0_1, sigma=sigma_1),
        gaussian(x=x, A=A_2, x0=x0_2, sigma=sigma_2),
    )

def gaussian2D(x, y, A, x0, y0, sigma_x, sigma_y, theta):

    theta *= units.deg.to(units.rad)

    a = np.cos(theta)**2.0 / (2.0 * sigma_x**2.0) + np.sin(theta)**2.0 / (2.0 * sigma_y**2.0)
    b = -np.sin(2.0 * theta) / (2.0 * sigma_x**2.0) + np.sin(2.0 * theta) / (2.0 * sigma_y**2.0)
    c = np.sin(theta)**2.0 / (2.0 * sigma_x**2.0) + np.cos(theta)**2.0 / (2.0 * sigma_y**2.0)

    return A * np.exp(
        -(
            a * ((x - x0)**2.0) +
            b * (x - x0) * (y - y0) +
            c * ((y - y0)**2.0)
        )
    )

def fit_gaussian2D(
    x,
    y,
    z,
    p0=None,
    return_cov=True,
    **kwargs
):

    def gaussian2D_wrapper(xy, A, x0, y0, sigma_x, sigma_y, theta):

        x, y = xy

        #print(A, x0, y0, sigma_x, sigma_y, theta)#;exit()

        return np.ndarray.flatten(
            gaussian2D(x, y, A, x0, y0, sigma_x, sigma_y, theta)
        )


    p, p_cov = optimize.curve_fit(
        gaussian2D_wrapper,
        (x, y),
        np.ndarray.flatten(z),
        p0=p0
    )

    return p



def fit_gaussian(
    x,
    y,
    p0=None,
    sigma=None,
    return_cov=True,
    **kwargs
):

    p, p_cov = optimize.curve_fit(
        gaussian,
        x,
        y,
        p0=p0,
        sigma=sigma,
        **kwargs
    )

    if return_cov:
        return p, p_cov
    return p


def fit_gaussian_with_continuum(
    x,
    y,
    p0=None,
    sigma=None,
    return_cov=True,
    **kwargs
):

    p, p_cov = optimize.curve_fit(
        gaussian_with_continuum,
        x,
        y,
        p0=p0,
        sigma=sigma,
        **kwargs
    )

    if return_cov:
        return p, p_cov
    return p


def fit_gaussian_skewed(
    x,
    y,
    p0=None,
    sigma=None,
    return_cov=True,
    **kwargs
):
    # NOTE: Global solution
    def loss_function(
        parameters,
        x,
        y,
        sigma=None
    ):
        residuals = y - gaussian_skewed(x, *parameters)
        if sigma is not None:
            return np.sum((residuals / sigma)**2.0)
        else:
            return np.sum(residuals**2.0)

    # NOTE:
    result = optimize.minimize(
        loss_function,
        p0,
        args=(x, y, sigma),
        method="L-BFGS-B",
        options={
            'maxiter':10000, # NOTE: kwargs["maxfev"]
            #'ftol':1e-8,  # Function tolerance
            #'gtol':1e-6,  # Gradient tolerance
        }
    )
    # # NOTE: DELETE
    # loss = loss_function(
    #     parameters=result.x,
    #     x=x,
    #     y=y,
    #     sigma=sigma
    # )
    # print("loss (stage 1) =", loss)
    # if return_cov:
    #     return result.x, None
    # return result.x

    # NOTE:
    p, p_cov = optimize.curve_fit(
        gaussian_skewed,
        x,
        y,
        p0=result.x,
        sigma=sigma,
        **kwargs
    )
    # # NOTE: DELETE
    # loss = loss_function(
    #     parameters=p,
    #     x=x,
    #     y=y,
    #     sigma=sigma
    # )
    # print("loss (stage 2) =", loss)

    if return_cov:
        return p, p_cov
    return p




def fit_gaussian_x2(
    x,
    y,
    p0=None,
    return_cov=True,
    **kwargs
):

    p, p_cov = optimize.curve_fit(
        gaussian_x2,
        x,
        y,
        p0=p0,
        **kwargs
    )

    if return_cov:
        return p, p_cov
    return p


def gaussian_x2_with_shared_sigma(
    x,
    A_1,
    x0_1,
    A_2,
    x0_2,
    sigma
):

    return np.add(
        gaussian(x=x, A=A_1, x0=x0_1, sigma=sigma),
        gaussian(x=x, A=A_2, x0=x0_2, sigma=sigma),
    )

def fit_gaussian_x2_with_shared_sigma(
    x,
    y,
    p0=None,
    return_cov=True,
    **kwargs
):

    p, p_cov = optimize.curve_fit(
        gaussian_x2_with_shared_sigma,
        x,
        y,
        p0=p0,
        **kwargs
    )

    if return_cov:
        return p, p_cov
    return p


def gaussian_x2_with_shared_sigma_and_fixed_offset(
    x,
    A_1,
    x0,
    sigma,
    A_2,
    offset,
):

    # print(
    #     "parameters:",
    #     A_1,
    #     x0,
    #     sigma,
    #     A_2,
    #     offset,
    # )

    return np.add(
        gaussian(
            x=x,
            A=A_1,
            x0=x0,
            sigma=sigma
        ),
        gaussian(
            x=x,
            A=A_2,
            x0=x0 + offset,
            sigma=sigma
        ),
    )

def gaussian_x3_with_shared_sigma_and_fixed_offset(
    x,
    A_1,
    x0,
    sigma,
    A_2,
    offset_2,
    A_3,
    offset_3,
    condition=False
):

    # print(
    #     "parameters:",
    #     A_1,
    #     x0,
    #     sigma,
    #     A_2,
    #     offset_2,
    #     A_3,
    #     offset_3,
    # )

    g1 = gaussian(
        x=x,
        A=A_1,
        x0=x0,
        sigma=sigma
    )
    g2 = gaussian(
        x=x,
        A=A_2,
        x0=x0 + offset_2,
        sigma=sigma
    )
    g3 = gaussian(
        x=x,
        A=A_3,
        x0=x0 + offset_3,
        sigma=sigma
    )

    if condition:
        return np.add.reduce((g1, g2, g3)), g1, g2, g3
    else:
        return np.add.reduce((g1, g2, g3))

def fit_gaussian_x2_with_shared_sigma_and_fixed_offset(
    x,
    y,
    offset,
    p0=None,
    return_cov=True,
    **kwargs
):

    model = lambda a, A_1, x0, sigma, A_2:gaussian_x2_with_shared_sigma_and_fixed_offset(
        x,
        A_1,
        x0,
        sigma,
        A_2,
        offset=offset,
    )

    p, p_cov = optimize.curve_fit(
        model,
        x,
        y,
        p0=p0,
        **kwargs
    )

    if return_cov:
        return p, p_cov
    return p

def fit_gaussian_x3_with_shared_sigma_and_fixed_offset(
    x,
    y,
    offset_i,
    offset_j,
    p0=None,
    sigma=None,
    return_cov=True,
    **kwargs
):

    model = lambda a, A_1, x0, sigma, A_2, A_3:gaussian_x3_with_shared_sigma_and_fixed_offset(
        x,
        A_1,
        x0,
        sigma,
        A_2,
        offset_i,
        A_3,
        offset_j,
    )

    p, p_cov = optimize.curve_fit(
        model,
        x,
        y,
        p0=p0,
        sigma=sigma,
        **kwargs
    )

    if return_cov:
        return p, p_cov
    return p


def fit_gaussian_with_fixed_x0(x, y, x0, p0=None, return_cov=True, **kwargs):

    func = lambda x, A, sigma: gaussian(x=x, x0=x0, A=A, sigma=sigma)

    p, p_cov = optimize.curve_fit(func, x, y, p0=p0, **kwargs)

    if return_cov:
        return p, p_cov
    return p


def _clean_histogram_data(data, weights=None, xmin=None, xmax=None):
    values = np.asarray(data, dtype=float).ravel()

    if values.size == 0:
        raise ValueError("data must contain at least one value")

    mask = np.isfinite(values)

    if weights is None:
        weights_clean = None
    else:
        weights_values = np.asarray(weights, dtype=float).ravel()
        if weights_values.shape != values.shape:
            raise ValueError("weights must have the same shape as data")
        mask &= np.isfinite(weights_values)

    if xmin is not None:
        mask &= values >= xmin
    if xmax is not None:
        mask &= values <= xmax

    values_clean = values[mask]

    if values_clean.size == 0:
        raise ValueError("no finite data remain after applying limits")

    if weights is not None:
        weights_clean = weights_values[mask]

    return values_clean, weights_clean


def _initial_gaussian_parameters(x, y, data):
    amplitude = float(np.nanmax(y))
    if not np.isfinite(amplitude) or amplitude <= 0.0:
        amplitude = 1.0

    x0 = float(x[np.nanargmax(y)])

    lower, upper = np.nanpercentile(data, [15.865, 84.135])
    sigma = 0.5 * (upper - lower)
    if not np.isfinite(sigma) or sigma <= 0.0:
        sigma = float(np.nanstd(data))
    if not np.isfinite(sigma) or sigma <= 0.0:
        sigma = np.finfo(float).eps

    return amplitude, x0, sigma


def fit_gaussian_from_data(
    data: np.ndarray,
    weights=None,
    bins=50,
    xmin=None,
    xmax=None,
    density=None,
    p0=None,
    return_cov=False,
    debug=False,
    return_x=False,
    **kwargs
):
    """Fit a Gaussian to the pixel-value distribution of an image.

    The fitted Gaussian width, ``p[2]``, is the background-noise estimate.
    ``data`` is flattened before fitting, so 2D images and already-flattened
    arrays are both accepted.
    """

    data_sanitized, weights_sanitized = _clean_histogram_data(
        data=data,
        weights=weights,
        xmin=xmin,
        xmax=xmax,
    )

    y, x = np.histogram(
        a=data_sanitized,
        bins=bins,
        density=density,
        weights=weights_sanitized,
    )
    x = (x[:-1] + x[1:]) / 2.0

    x_for_plotting = np.linspace(np.min(x), np.max(x), 500)

    if p0 is None:
        p0 = _initial_gaussian_parameters(x=x, y=y, data=data_sanitized)

    fit_kwargs = {"maxfev": 10000}
    fit_kwargs.update(kwargs)
    if "bounds" not in fit_kwargs:
        fit_kwargs["bounds"] = (
            (0.0, -np.inf, np.finfo(float).eps),
            (np.inf, np.inf, np.inf),
        )

    try:
        p, p_cov = fit_gaussian(
            x=x,
            y=y,
            p0=p0,
            return_cov=True,
            **fit_kwargs,
        )
    except (RuntimeError, ValueError, FloatingPointError):
        p, p_cov = None, None

    if debug:
        plt.figure()

        _, bins, _ = plt.hist(
            data_sanitized,
            bins=bins,
            density=density,
            weights=weights_sanitized,
            color="b",
            alpha=0.5,
        )

        plt.plot(x, y, linestyle="None", marker="o", color="black", label="data")

        if p is not None:
            y_for_plotting = gaussian(x_for_plotting, *p)

            plt.plot(
                x_for_plotting,
                y_for_plotting,
                linewidth=5,
                color="black",
                alpha=0.75,
                label="fit",
            )

        # mu, sigma = stats.norm.fit(data)
        # best_fit_line = stats.norm.pdf(bins, mu, sigma)
        # plt.plot(bins, best_fit_line, color="r")

        plt.legend()
        #plt.show()

    result = (p, p_cov) if return_cov else p

    if return_x:
        return result, x
    return result


def fit_gaussian_with_fixed_x0_from_data(
    data,
    x0,
    bins=50,
    density=None,
    p0=None,
    xmax=None,
    return_cov=True,
    debug=False,
    return_x=False,
    **kwargs
):

    y, x = np.histogram(
        a=data,
        bins=bins,
        density=density
    )
    x = (x[:-1] + x[1:]) / 2.0

    if xmax is None:
        x_for_fit = x
        y_for_fit = y
    else:
        idx = x < xmax
        x_for_fit = x[idx]
        y_for_fit = y[idx]

    p = fit_gaussian_with_fixed_x0(x=x_for_fit, y=y_for_fit, x0=x0, p0=p0, return_cov=False)
    print("p =", p)

    if debug:
        plt.figure()

        _, bins, _ = plt.hist(
            data,
            bins=bins,
            density=density,
            color="b",
            alpha=0.5
        )

        plt.plot(x, y, linestyle="None", marker="o", color="black", label="data")

        xmin = np.min(x)
        if xmax is None:
            xmax = np.max(x)
        x_model = np.linspace(xmin, xmax, 1000)

        y_model = gaussian(x_model, A=p[0], x0=x0, sigma=p[1])

        plt.plot(x_model, y_model, linewidth=5, color="black", alpha=0.75, label="fit")

        # mu, sigma = stats.norm.fit(data)
        # best_fit_line = stats.norm.pdf(bins, mu, sigma)
        # plt.plot(bins, best_fit_line, color="r")


        plt.axvline(x0, linestyle="--", color="black")
        plt.yscale("log")
        plt.ylim(10**-1.0, 10**5.0)
        plt.legend()
        plt.show()

    if return_x:
        return p, x
    return p



if __name__ == "__main__":
    pass