from scipy import interpolate


def interpolated_reconstruction(voronoi, values, grid):

    return interpolate.griddata(
        voronoi._points,
        values,
        grid.in_2d,
        method="cubic",
        fill_value=0.0
    )

# interpolated_reconstruction = interpolate.griddata(
#     fit.inversion.mapper.voronoi._points,
#     source_pixel_values,
#     grid.in_2d,
#     method="cubic",
#     fill_value=0.0
# )
