import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import distance

from scipy import stats


def minimum_distance(points, metric='euclidean'):

    # NOTE: If points is an (N, 2) array then the shape of distances is (N x N).
    distances = distance.cdist(
        points, points, metric=metric
    )

    # NOTE: Replace the zeros, which come from comparing each point to itself, with nan.
    distances[distances == 0] = np.nan

    return np.nanmin(distances)

# NOTE: write a test function that checks the output of this function with the function "minimum_distance".
# def minimum_distance_for_comparison(points):
#
#     if isinstance(points, list):
#         points = np.asarray(points)
#
#     N = points.shape[0]
#     x = points[:, 0]
#     y = points[:, 1]
#     distance = 1.0e99
#     idx_i = 0
#     idx_j = 0
#     for i in range(N):
#         for j in range(i+1, N):
#             distance_temp = np.hypot(x[i] - x[j], y[i] - y[j])
#             if distance_temp<distance:
#                 distance = distance_temp
#                 idx_i = i
#                 idx_j = j
#
#     return distance


def lognormal(x, mean, sigma):

    return 1.0 / (x * sigma * np.sqrt(2.0 * np.pi)) * np.exp(-(np.log(x) - mean)**2.0 / (2.0 * sigma**2.0))

if __name__ == "__main__":

    xmin = 10**-2.0
    xmax = 10**+2.0
    x = np.logspace(np.log10(xmin), np.log10(xmax), 100)

    plt.plot(x, stats.lognorm.pdf(x, 1.0))
    plt.plot(x, lognormal(x, np.log(0.1), 1.0))
    plt.xscale("log")
    plt.show()
