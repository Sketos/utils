import numpy as np
import matplotlib.pyplot as plt

import autofit as af
import autolens as al


def evidence_from_constant_regularization(masked_dataset, lens_galaxies, source_redshift, pixelization, coefficients_array):


    # TODO: Check the pixelization

    # NOTE:
    evidences_array = np.zeros(
        shape=coefficients_array.shape,
        dtype=np.float
    )
    for i, coefficient in enumerate(coefficients_array):

        if isinstance(masked_dataset, al.MaskedInterferometer):
            fit = al.FitInterferometer(
                masked_interferometer=masked_dataset,
                tracer=al.Tracer.from_galaxies(
                    galaxies=[
                        *lens_galaxies,
                        al.Galaxy(
                            redshift=source_redshift,
                            pixelization=pixelization,
                            regularization=al.reg.Constant(
                                coefficient=coefficient
                            )
                        )
                    ]
                )
            )

        evidences_array[i] = fit.evidence

    plt.figure()
    plt.plot(coefficients_array, evidences_array)
    plt.xscale("log")
    plt.show()
