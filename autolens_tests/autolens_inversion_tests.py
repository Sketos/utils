import os
import sys

import numpy as np

import matplotlib.pyplot as plt

import autolens as al


sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)

import autolens_utils.autolens_plot_utils as autolens_plot_utils
import autolens_utils.autolens_tracer_utils as autolens_tracer_utils
import autolens_utils.autolens_inversion_utils as autolens_inversion_utils


def mask_circular(grid, radius, centre):

    return al.Mask.circular(
        shape_2d=grid.shape_2d,
        pixel_scales=grid.pixel_scales,
        sub_size=grid.sub_size,
        radius=radius,
        centre=centre
    )

def test_1(uv_wavelengths, real_space_mask, grid, tracer, transformer_class, noise_map, pixelization=None):
    """

    - Conclusion for when the noise map is the same that was added to the visibilities:

    Increasing the noise of the visibilities the coefficient that maximizes the
    bayesian evidence does NOT change.

    Increasing the number of source-plane pixel has dramatic changes in the
    amplitude of the bayesian evidence

    - Conclusion for when the noise map is estimated as the rms of the visibilities:

    """

    transformer = transformer_class(
        uv_wavelengths=uv_wavelengths,
        grid=grid.in_radians,
    )

    visibilities = transformer.visibilities_from_image(
        image=tracer.profile_image_from_grid(grid=grid)
    )

    interferometer = al.Interferometer(
        visibilities=al.Visibilities.manual_1d(
            np.add(visibilities, noise_map)
        ),
        noise_map=noise_map,
        uv_wavelengths=al.Visibilities.manual_1d(uv_wavelengths)
    )

    # plt.figure()
    # plt.plot(
    #     np.hypot(
    #         interferometer.uv_wavelengths[:, 0],
    #         interferometer.uv_wavelengths[:, 1]
    #     ),
    #     np.hypot(
    #         interferometer.visibilities[:, 0],
    #         interferometer.visibilities[:, 1]
    #     ),
    #     linestyle="None",
    #     marker="o"
    # )
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.show()

    # dirty_image = autolens_plot_utils.dirty_image_from_visibilities_and_transformer(
    #     visibilities=interferometer.visibilities,
    #     transformer=transformer
    # )
    # plt.figure()
    # plt.imshow(dirty_image)
    # plt.colorbar()
    # plt.show()
    # exit()


    lens_galaxies = autolens_tracer_utils.galaxies_with_mass_profiles_from_tracer(
        tracer=tracer
    )

    masked_interferometer = al.MaskedInterferometer(
        interferometer=interferometer,
        visibilities_mask=np.full(
            shape=interferometer.visibilities.shape,
            fill_value=False
        ),
        real_space_mask=real_space_mask,
        transformer_class=transformer_class
    )

    # autolens_inversion_utils.minimize_regularization_coefficient(
    #     masked_interferometer=masked_interferometer,
    #     lens_galaxies=lens_galaxies,
    #     pixelization=pixelization,
    #     source_redshift=2.0
    # )

    # NOTE: Make this a test
    coefficients_1, evidences_1 = autolens_inversion_utils.minimize_regularization_coefficient(
        masked_interferometer=masked_interferometer,
        lens_galaxies=lens_galaxies,
        pixelization=al.pix.VoronoiMagnification(
            shape=(22, 22)
        ),
        source_redshift=2.0
    )

    coefficients_2, evidences_2 = autolens_inversion_utils.minimize_regularization_coefficient(
        masked_interferometer=masked_interferometer,
        lens_galaxies=lens_galaxies,
        pixelization=al.pix.VoronoiMagnification(
            shape=(21, 21)
        ),
        source_redshift=2.0
    )

    coefficients_3, evidences_3 = autolens_inversion_utils.minimize_regularization_coefficient(
        masked_interferometer=masked_interferometer,
        lens_galaxies=lens_galaxies,
        pixelization=al.pix.VoronoiMagnification(
            shape=(20, 20)
        ),
        source_redshift=2.0
    )

    figure, axes = plt.subplots(nrows=1, ncols=3)
    axes[0].plot(coefficients_1, evidences_1, marker="o", label="pix 1")
    axes[1].plot(coefficients_2, evidences_2, marker="o", label="pix 2")
    axes[2].plot(coefficients_3, evidences_3, marker="o", label="pix 3")
    axes[0].set_xscale("log")
    axes[1].set_xscale("log")
    axes[2].set_xscale("log")
    plt.show()
    exit()


    # min_coefficient = 10**1.0
    # max_coefficient = 10**3.0
    # coefficients = np.logspace(
    #     np.log10(min_coefficient),
    #     np.log10(max_coefficient),
    #     10
    # )
    #
    # array_term_1 = []
    # array_term_2 = []
    # array_term_3 = []
    # array_term_4 = []
    # array_term_5 = []
    # for i, coefficient in enumerate(coefficients):
    #     print(coefficient)
    #
    #     source = al.Galaxy(
    #         redshift=2.0,
    #         pixelization=al.pix.VoronoiMagnification(
    #             shape=(20, 20)
    #         ),
    #         regularization=al.reg.Constant(
    #             coefficient=coefficient
    #         ),
    #     )
    #
    #     tracer = al.Tracer.from_galaxies(
    #         galaxies=[*lens_galaxies, source]
    #     )
    #
    #     fit = al.FitInterferometer(
    #         masked_interferometer=masked_interferometer,
    #         tracer=tracer
    #     )
    #
    #     # autolens_plot_utils.plot_fit(
    #     #     fit=fit,
    #     #     xlim_source_plane=(-1.0, 1.0),
    #     #     ylim_source_plane=(-1.0, 1.0),
    #     # )
    #
    #     #array_1.append(fit.figure_of_merit)
    #
    #
    #     term_1, term_2, term_3, term_4, term_5 = fit.evidence_terms
    #     print(term_1, term_2, term_3, term_4, term_5)
    #     array_term_1.append(term_1)
    #     array_term_2.append(term_2)
    #     array_term_3.append(term_3)
    #     array_term_4.append(term_4)
    #     array_term_5.append(term_5)
    #
    #
    # #     print(fit.figure_of_merit)
    # #
    # #     a.append(fit.figure_of_merit)
    #
    # plt.plot(coefficients, np.asarray(array_term_1))
    # plt.plot(coefficients, np.asarray(array_term_2))
    # plt.plot(coefficients, np.asarray(array_term_3))
    # plt.plot(coefficients, np.asarray(array_term_4))
    # plt.plot(coefficients, np.asarray(array_term_5))
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.show()




    # source = al.Galaxy(
    #     redshift=2.0,
    #     pixelization=al.pix.VoronoiMagnification(
    #         shape=(30, 30)
    #     ),
    #     regularization=al.reg.Constant(
    #         coefficient=100.0
    #     ),
    # )
    #
    # tracer = al.Tracer.from_galaxies(
    #     galaxies=[*lens_galaxies, source]
    # )
    #
    # fit = al.FitInterferometer(
    #     masked_interferometer=masked_interferometer,
    #     tracer=tracer
    # )
    #
    # autolens_plot_utils.plot_fit(
    #     fit=fit,
    #     xlim_source_plane=(-1.0, 1.0),
    #     ylim_source_plane=(-1.0, 1.0),
    # )
