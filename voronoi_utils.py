import numpy as np


def voronoi_polygons(voronoi, radius=None):
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.
    Parameters
    ----------
    voronoi : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.
    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.
    """

    if voronoi.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = voronoi.vertices.tolist()

    center = voronoi.points.mean(axis=0)
    if radius is None:
        radius = voronoi.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(voronoi.ridge_points, voronoi.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(voronoi.point_region):
        vertices = voronoi.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = voronoi.points[p2] - voronoi.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # hyper

            midpoint = voronoi.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = voronoi.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


def grid_to_voronoi():

    pass

    # n_voronoi, n_test = 100, 1000
    #
    # voronoi_points = np.random.rand(n_voronoi, 2)
    # test_points = np.random.rand(n_test, 2)
    #
    # voronoi_kdtree = cKDTree(voronoi_points)
    #
    # test_point_dist, test_point_regions = voronoi_kdtree.query(test_points, k=1)
    # print(len(test_point_regions))
    #
    # plt.figure()
    # plt.plot(voronoi_points[:, 0], voronoi_points[:, 1], linestyle="None", marker="o", markersize=10, color="black")
    # plt.plot(test_points[:, 0], test_points[:, 1], linestyle="None", marker="o", markersize=5, color="r")
    #
    # for i in range(len(test_point_regions)):
    #     plt.plot([test_points[i, 0], voronoi_points[test_point_regions[i], 0]], [test_points[i, 1], voronoi_points[test_point_regions[i], 1]], linestyle="-", color="b")
    # plt.show()
    # exit()
