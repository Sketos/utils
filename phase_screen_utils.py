# NOTE: Put all the function that are used to generate phase screens here ...


import numpy as np

from scipy import interpolate


def interpolate_phase_screen(phase_screen, delta_x, L=None):

    if L is None:
        raise ValueError(
            "This has not been implemented yet."
        )

        # N = phase_screen.shape[0]
        # L = N * delta_x

    # NOTE: The phase screen must be a 2D array
    if len(phase_screen.shape) == 2:
        if phase_screen.shape[0] != phase_screen.shape[1]:
            raise ValueError(
                "This has not been implemented yet."
            )
    else:
        raise ValueError(
            "The phase screen must be a 2D array, instead the shape of the input is {}".format(
                phase_screen.shape
            )
        )

    x = np.arange(
        0, L, delta_x
    )
    y = np.arange(
        0, L, delta_x
    )

    return interpolate.RegularGridInterpolator(
        (x, y),
        phase_screen,
        bounds_error=False,
        fill_value=0.0
    )



def generate_phases_from_interpolated_phase_screen(interpolated_phase_screen, antenna_positions, t, v):

    # NOTE: t is the time interval it takes for a visibility to be recorded

    # NOTE: Do a few checks

    phases = np.zeros(
        shape=(
            len(t),
            antenna_positions.shape[-1]
        )
    )
    for i, t_i in enumerate(t):
        points = list(
            zip(
                antenna_positions[0, :] + v * t_i,
                antenna_positions[1, :] + v * t_i
            )
        )

        phases[i] = interpolated_phase_screen(points)

    return phases


def generate_phases_from_phase_screen(phase_screen, delta_x, L, antenna_positions, t, v):


    interpolated_phase_screen = interpolate_phase_screen(
        phase_screen=phase_screen,
        delta_x=delta_x,
        L=L
    )

    return generate_phases_from_interpolated_phase_screen(
        interpolated_phase_screen=interpolated_phase_screen,
        antenna_positions=antenna_positions,
        t=t,
        v=v
    )

# def phases_from_antenna_phases(antenna_phases, wrap_phases=False):
#     """
#
#     WARNING: Keep wrap_phases=False
#     """
#
#     n_t, n_a = antenna_phases.shape
#
#     phases = np.zeros(
#         shape=(
#             n_t,
#             int(
#                 n_a * (n_a - 1) / 2.0
#             )
#         )
#     )
#
#     for i in range(n_t):
#         j = 0
#         for j_1 in range(n_a):
#             for j_2 in range(j_1 + 1, n_a):
# #                 print(
# #                     "antenna_i = {}".format(j_1),
# #                     "antenna_j = {}".format(j_2)
# #                 )
#                 if wrap_phases:
#                     phases[i, j] = wrap(
#                         a=np.subtract(
#                             antenna_phases[i, j_1],
#                             antenna_phases[i, j_2]
#                         )
#                     )
#                 else:
#                     phases[i, j] = np.subtract(
#                         antenna_phases[i, j_1],
#                         antenna_phases[i, j_2]
#                     )
#
#
#                 j+=1
#
#     return phases
