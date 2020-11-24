import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize, sparse

import autoarray as aa
import autolens as al

from autoarray.fit import fit as aa_fit


sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)

import autolens_utils.autolens_plot_utils as autolens_plot_utils
import autolens_utils.autolens_tracer_utils as autolens_tracer_utils


def mapped_reconstructed_visibilities(transformed_mapping_matrices, reconstruction):

    real_visibilities = aa.util.inversion_util.mapped_reconstructed_data_from_mapping_matrix_and_reconstruction(
        mapping_matrix=transformed_mapping_matrices[0],
        reconstruction=reconstruction,
    )

    imag_visibilities = aa.util.inversion_util.mapped_reconstructed_data_from_mapping_matrix_and_reconstruction(
        mapping_matrix=transformed_mapping_matrices[1],
        reconstruction=reconstruction,
    )

    return aa.structures.visibilities.Visibilities(
        visibilities_1d=np.stack(
            arrays=(real_visibilities, imag_visibilities),
            axis=-1
        )
    )

def mapped_reconstructed_visibilities_from_mapper_and_transformer(
    transformer,
    mapper,
    reconstruction
):

    return mapped_reconstructed_visibilities(
        transformed_mapping_matrices=transformer.transformed_mapping_matrices_from_mapping_matrix(
            mapping_matrix=mapper.mapping_matrix
        ),
        reconstruction=reconstruction
    )

def mapped_reconstructed_visibilities_from_mapper_and_transformers(transformers, mapper, reconstruction):

    return np.array([
        mapped_reconstructed_visibilities_from_mapper_and_transformer(
            transformer=transformer,
            mapper=mapper,
            reconstruction=reconstruction
        )
        for transformer in transformers
    ])



# def inversion_from_tracer(masked_dataset, tracer):
#
#     return al.Inversion(
#         masked_dataset=masked_dataset,
#         mapper=autolens_tracer_utils.mapper_from_tracer_and_grid(
#             tracer=tracer,
#             grid=masked_dataset.grid
#         ),
#         regularization=tracer.source_plane.regularization
#     )


def inversion_from_tracer(interferometer, real_space_mask, tracer, transformer_class=al.TransformerNUFFT):

    masked_interferometer = al.MaskedInterferometer(
        interferometer=interferometer,
        visibilities_mask=np.full(
            shape=interferometer.visibilities.shape,
            fill_value=False
        ),
        real_space_mask=real_space_mask,
        transformer_class=transformer_class
    )

    return al.Inversion(
        masked_dataset=masked_interferometer,
        mapper=autolens_tracer_utils.mapper_from_tracer_and_grid(
            tracer=tracer,
            grid=masked_interferometer.grid
        ),
        regularization=tracer.source_plane.regularization
    )


def inversions_from_transformers(masked_interferometer, tracer):

    fit = al.FitInterferometer(
        masked_interferometer=masked_interferometer,
        tracer=tracer
    )


# NOTE: TEST
def preconditioner_matrix(masked_interferometer, tracer):

    def data_vector_from(transformed_mapping_matrices, masked_interferometer):

        real_data_vector = aa.util.inversion_util.data_vector_from_transformed_mapping_matrix_and_data(
            transformed_mapping_matrix=transformed_mapping_matrices[0],
            visibilities=masked_interferometer.visibilities[:, 0],
            noise_map=masked_interferometer.noise_map[:, 0],
        )

        imag_data_vector = aa.util.inversion_util.data_vector_from_transformed_mapping_matrix_and_data(
            transformed_mapping_matrix=transformed_mapping_matrices[1],
            visibilities=masked_interferometer.visibilities[:, 1],
            noise_map=masked_interferometer.noise_map[:, 1],
        )

        data_vector = np.add(
            real_data_vector,
            imag_data_vector
        )

        return data_vector


    def curvature_matrix_from(transformed_mapping_matrices, masked_interferometer):

        # real_data_vector = aa.util.inversion_util.data_vector_from_transformed_mapping_matrix_and_data(
        #     transformed_mapping_matrix=transformed_mapping_matrices[0],
        #     visibilities=masked_interferometer.visibilities[:, 0],
        #     noise_map=masked_interferometer.noise_map[:, 0],
        # )
        #
        # imag_data_vector = aa.util.inversion_util.data_vector_from_transformed_mapping_matrix_and_data(
        #     transformed_mapping_matrix=transformed_mapping_matrices[1],
        #     visibilities=masked_interferometer.visibilities[:, 1],
        #     noise_map=masked_interferometer.noise_map[:, 1],
        # )
        #
        # data_vector = np.add(
        #     real_data_vector,
        #     imag_data_vector
        # )

        real_curvature_matrix = aa.util.inversion_util.curvature_matrix_from_transformed_mapping_matrix(
            transformed_mapping_matrix=transformed_mapping_matrices[0],
            noise_map=masked_interferometer.noise_map[:, 0],
        )

        imag_curvature_matrix = aa.util.inversion_util.curvature_matrix_from_transformed_mapping_matrix(
            transformed_mapping_matrix=transformed_mapping_matrices[1],
            noise_map=masked_interferometer.noise_map[:, 1],
        )

        curvature_matrix = np.add(
            real_curvature_matrix,
            imag_curvature_matrix
        )

        return curvature_matrix


    mapper = autolens_tracer_utils.mapper_from_tracer_and_grid(
        tracer=tracer,
        grid=masked_interferometer.grid
    )

    print("The shape", masked_interferometer.visibilities.shape)

    P_noise_normalization = np.sum(
        np.divide(1.0, masked_interferometer.noise_map[:, 0]**2.0 + masked_interferometer.noise_map[:, 1]**2.0)
    )

    #print(tracer.regularizations_of_planes[-1])

    regularization_matrix = tracer.regularizations_of_planes[-1].regularization_matrix_from_mapper(
        mapper=mapper
    )

    P = np.add(
        np.multiply(
            P_noise_normalization,
            np.dot(mapper.mapping_matrix.T, mapper.mapping_matrix)
        ),
        regularization_matrix
    )

    P_inv = np.linalg.inv(P)

    transformed_mapping_matrices = masked_interferometer.transformer.transformed_mapping_matrices_from_mapping_matrix(
        mapping_matrix=mapper.mapping_matrix
    )

    curvature_matrix = curvature_matrix_from(
        transformed_mapping_matrices=transformed_mapping_matrices,
        masked_interferometer=masked_interferometer
    )


    curvature_reg_matrix = np.add(curvature_matrix, regularization_matrix)


    # figure, axes = plt.subplots(nrows=1, ncols=3)
    # im0 = axes[0].imshow(curvature_reg_matrix, cmap="jet")
    # plt.colorbar(im0, ax=axes[0])
    # im1 = axes[1].imshow(P_inv, cmap="jet")
    # plt.colorbar(im1, ax=axes[1])
    # im2 = axes[2].imshow(np.matmul(P_inv, curvature_reg_matrix), cmap="jet")
    # plt.colorbar(im2, ax=axes[2])
    # plt.show()
    # exit()


    data_vector = data_vector_from(
        transformed_mapping_matrices=transformed_mapping_matrices,
        masked_interferometer=masked_interferometer
    )

    P_curvature_reg_matrix = np.matmul(
        P_inv, curvature_reg_matrix
    )
    print(
        "The condition number of P^{-1} * A is = ", np.linalg.cond(P_curvature_reg_matrix)
    )

    P_data_vector = np.matmul(
        P_inv, data_vector
    )

    # plt.figure()
    # plt.imshow(P_curvature_reg_matrix)
    # plt.colorbar()
    # #plt.show()
    # #exit()

    curvature_reg_matrix_inv = np.linalg.inv(curvature_reg_matrix)

    # time_i = time.time()
    # p_values = np.linalg.solve(
    #     P_curvature_reg_matrix,
    #     P_data_vector,
    # )
    # time_j = time.time()
    # print("It took t = {} sec".format(time_j - time_i))



    time_i = time.time()
    p_values_cg = sparse.linalg.cg(
        A=curvature_reg_matrix, b=data_vector, x0=np.zeros(shape=P.shape[0]), M=np.ones(shape=curvature_reg_matrix_inv.shape),
    )
    time_j = time.time()
    print("It took t = {} sec (with P)".format(time_j - time_i))

    time_i = time.time()
    values = np.linalg.solve(
        curvature_reg_matrix,
        data_vector
    )
    time_j = time.time()
    print("It took t = {} sec".format(time_j - time_i))



    exit()

    # for i in range(len(values)):
    #
    #     print(i, values[i], p_values[i])





# NOTE: This function is the equivalent of "minimize_regularization_coefficient" without any optimization. I need to figure out what is the difference of the two
def func_dev(masked_interferometer, len_galaxies, pixelization, redshift=2.0):

    min_coefficient = 10**5.0
    max_coefficient = 10**7.0
    coefficients = np.logspace(
        np.log10(min_coefficient),
        np.log10(max_coefficient),
        50
    )

    evidences = np.zeros(shape=coefficients.shape)

    for i, coefficient in enumerate(coefficients):

        src_galaxy = al.Galaxy(
            redshift=redshift,
            pixelization=pixelization,
            regularization=al.reg.Constant(
                coefficient=coefficient
            )
        )

        tracer = al.Tracer.from_galaxies(
            galaxies=len_galaxies + [src_galaxy, ]
        )

        fit = al.FitInterferometer(
            masked_interferometer=masked_interferometer,
            tracer=tracer
        )

        evidences[i] = fit.evidence


    plt.plot(coefficients, evidences, color="b")
    plt.xscale("log")
    plt.xlabel("Regularization Coefficient", fontsize=15)
    plt.ylabel("Bayesian Evidence", fontsize=15)
    plt.show()



def evidence_for_reg_coefficient_array(masked_interferometer, lens_galaxies, pixelization, source_redshift, use_linear_operators, reg_coefficient_array):

    if use_linear_operators:

        array_term_1 = []
        array_term_2 = []
        array_term_3 = []
        array_term_4 = []
        array_term_5 = []

        list_of_reconstructions = []
        max_flux = []

        log_evidences = []
        log_likelihoods = []
        for i, coefficient in enumerate(reg_coefficient_array):
            print(i, np.log10(coefficient))

            source_galaxy = al.Galaxy(
                redshift=source_redshift,
                pixelization=pixelization,
                regularization=al.reg.Constant(
                    coefficient=coefficient
                ),
            )

            tracer = al.Tracer.from_galaxies(
                galaxies=[*lens_galaxies, source_galaxy]
            )

            fit = al.FitInterferometer(
                masked_interferometer=masked_interferometer,
                tracer=tracer,
                settings_inversion=al.SettingsInversion(use_linear_operators=True)
            )

            log_evidences.append(fit.log_evidence)
            log_likelihoods.append(fit.log_likelihood)

            reconstruction = fit.inversion.reconstruction
            max_flux.append(np.max(reconstruction))
            list_of_reconstructions.append(fit.inversion.reconstruction)

            term_1, term_2, term_3, term_4, term_5 = fit.log_evidence_terms
            array_term_1.append(term_1)
            array_term_2.append(term_2)
            array_term_3.append(term_3)
            array_term_4.append(term_4)
            array_term_5.append(term_5)

    else:
        raise ValueError("This has not been implemented yet.")

    return log_evidences, log_likelihoods, array_term_1, array_term_2, array_term_3, array_term_4, array_term_5, list_of_reconstructions, max_flux


def minimize_regularization_coefficient_general(masked_interferometer, lens_galaxies, pixelization, source_redshift, use_linear_operators):

    if use_linear_operators:

        def fun_minimize(log_coefficient, pixelization, source_redshift, lens_galaxies, masked_interferometer):

            coefficient = 10.0**log_coefficient[0] ; print(log_coefficient)

            source_galaxy = al.Galaxy(
                redshift=source_redshift,
                pixelization=pixelization,
                regularization=al.reg.Constant(
                    coefficient=coefficient
                ),
            )

            tracer = al.Tracer.from_galaxies(
                galaxies=[*lens_galaxies, source_galaxy]
            )

            fit = al.FitInterferometer(
                masked_interferometer=masked_interferometer,
                tracer=tracer,
                settings_inversion=al.SettingsInversion(use_linear_operators=True)
            )

            return -fit.figure_of_merit

    else:
        raise ValueError("This has not been implemented yet.")


    res = optimize.minimize(
        fun_minimize,
        x0=1.0,
        args=(pixelization, source_redshift, lens_galaxies, masked_interferometer),
        method='COBYLA'
    )

    print(res)

# TODO: find the minimum regularization coefficient
# TODO: We can have as input the tracer from which we select only the lens galaxies using the "galaxies_with_mass_profiles_from_tracer(tracer)" function in the autolens_tracer_utils.py
def minimize_regularization_coefficient(masked_interferometer, lens_galaxies, pixelization, source_redshift):
    """
    lens_galaxies must be a list of al.Galaxy objects

    # NOTE: This is giving a higher value than the ones I am getting from inversion pipeline ...
    """

    def fit_from_masked_dataset_and_inversion(masked_dataset, inversion):

        if isinstance(masked_dataset, al.MaskedInterferometer):

            return aa.fit.fit.FitInterferometer(
                masked_interferometer=masked_dataset,
                model_visibilities=inversion.mapped_reconstructed_visibilities,
                inversion=inversion
            )

        if isinstance(masked_dataset, imaging.MaskedImaging):

            raise ValueError(
                "This has not been implemented yet."
            )

    def inversion(
        masked_interferometer,
        mapper,
        regularization,
        transformed_mapping_matrices,
        regularization_matrix,
        curvature_reg_matrix,
        reconstruction
    ):
        if al.__version__ in ["0.45.0"]:
            return aa.operators.inversion.inversions.InversionInterferometer(
                    visibilities=masked_interferometer.visibilities,
                    noise_map=masked_interferometer.noise_map,
                    mapper=mapper,
                    regularization=regularization,
                    transformed_mapping_matrices=transformed_mapping_matrices,
                    regularization_matrix=regularization_matrix,
                    curvature_reg_matrix=curvature_reg_matrix,
                    reconstruction=reconstruction,
                )
        if al.__version__ in ["1.8.1"]:
            return aa.inversion.inversions.InversionInterferometerMatrix(
                visibilities=masked_interferometer.visibilities,
                noise_map=masked_interferometer.noise_map,
                transformer=masked_interferometer.transformer,
                mapper=mapper,
                regularization=regularization,
                regularization_matrix=regularization_matrix,
                reconstruction=reconstruction,
                transformed_mapping_matrices=transformed_mapping_matrices,
                curvature_reg_matrix=curvature_reg_matrix,
                settings=al.SettingsInversion()
            )

    def helper(masked_interferometer, transformed_mapping_matrices):


        if al.__version__ in ["0.45.0"]:
            real_data_vector = aa.util.inversion_util.data_vector_from_transformed_mapping_matrix_and_data(
                transformed_mapping_matrix=transformed_mapping_matrices[0],
                visibilities=masked_interferometer.visibilities[:, 0],
                noise_map=masked_interferometer.noise_map[:, 0],
            )
            imag_data_vector = aa.util.inversion_util.data_vector_from_transformed_mapping_matrix_and_data(
                transformed_mapping_matrix=transformed_mapping_matrices[1],
                visibilities=masked_interferometer.visibilities[:, 1],
                noise_map=masked_interferometer.noise_map[:, 1],
            )

        if al.__version__ in ["1.8.1"]:
            real_data_vector = aa.util.inversion_util.data_vector_via_transformed_mapping_matrix_from(
                transformed_mapping_matrix=transformed_mapping_matrices[0],
                visibilities=masked_interferometer.visibilities[:, 0],
                noise_map=masked_interferometer.noise_map[:, 0],
            )
            imag_data_vector = aa.util.inversion_util.data_vector_via_transformed_mapping_matrix_from(
                transformed_mapping_matrix=transformed_mapping_matrices[1],
                visibilities=masked_interferometer.visibilities[:, 1],
                noise_map=masked_interferometer.noise_map[:, 1],
            )

        data_vector = np.add(
            real_data_vector,
            imag_data_vector
        )

        if al.__version__ in ["0.45.0"]:
            real_curvature_matrix = aa.util.inversion_util.curvature_matrix_from_transformed_mapping_matrix(
                transformed_mapping_matrix=transformed_mapping_matrices[0],
                noise_map=masked_interferometer.noise_map[:, 0],
            )
            imag_curvature_matrix = aa.util.inversion_util.curvature_matrix_from_transformed_mapping_matrix(
                transformed_mapping_matrix=transformed_mapping_matrices[1],
                noise_map=masked_interferometer.noise_map[:, 1],
            )
        if al.__version__ in ["1.8.1"]:
            real_curvature_matrix = aa.util.inversion_util.curvature_matrix_via_mapping_matrix_from(
                mapping_matrix=transformed_mapping_matrices[0],
                noise_map=masked_interferometer.noise_map[:, 0],
            )
            imag_curvature_matrix = aa.util.inversion_util.curvature_matrix_via_mapping_matrix_from(
                mapping_matrix=transformed_mapping_matrices[1],
                noise_map=masked_interferometer.noise_map[:, 1],
            )

        curvature_matrix = np.add(
            real_curvature_matrix,
            imag_curvature_matrix
        )

        return data_vector, curvature_matrix

    # NOTE: Find a way to generate a mapper given the lens_galaxies and the given pixelization
    # (essentially independant of regilarization)
    def temp(lens_galaxies, source_redshift, pixelization, grid):
        pass

    # --- #
    # NOTE: Can we make this more elegant?
    source_galaxy_temp = al.Galaxy(
        redshift=source_redshift,
        pixelization=pixelization,
        regularization=al.reg.Constant(
            coefficient=1.0
        ),
    )

    tracer_temp = al.Tracer.from_galaxies(
        galaxies=[*lens_galaxies, source_galaxy_temp]
    )

    mapper = autolens_tracer_utils.mapper_from_tracer_and_grid(
        tracer=tracer_temp,
        grid=masked_interferometer.grid
    )
    # --- #

    transformed_mapping_matrices = masked_interferometer.transformer.transformed_mapping_matrices_from_mapping_matrix(
        mapping_matrix=mapper.mapping_matrix
    )
    print("The transformed mapping matrices have been computed")

    data_vector, curvature_matrix = helper(
        masked_interferometer=masked_interferometer,
        transformed_mapping_matrices=transformed_mapping_matrices
    )


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    """
    # NOTE: development (IT IS CURRENTLY WORKING)

    # class main:
    #
    #     def __init__(self, masked_interferometer, transformed_mapping_matrices, mapper):
    #
    #         self.transformed_mapping_matrices = transformed_mapping_matrices
    #
    #         self.mapper = mapper
    #
    #     def inversion_from(regularization, reconstruction, curvature_matrix):
    #
    #         regularization_matrix = regularization.regularization_matrix_from_mapper(
    #             mapper=self.mapper
    #         )
    #
    #         return inversion(
    #             masked_interferometer=masked_interferometer,
    #             mapper=mapper,
    #             regularization=regularization,
    #             transformed_mapping_matrices=self.transformed_mapping_matrices,
    #             regularization_matrix=regularization_matrix,
    #             curvature_reg_matrix=np.add(
    #                 curvature_matrix, regularization_matrix
    #             ),
    #             reconstruction=reconstruction
    #         )

    def fun_minimize(log_coefficient, mapper, curvature_matrix, data_vector, transformed_mapping_matrices, masked_interferometer):

        print(log_coefficient[0])
        coefficient = 10.0**log_coefficient[0]

        regularization = al.reg.Constant(
            coefficient=coefficient
        )

        regularization_matrix = regularization.regularization_matrix_from_mapper(
            mapper=mapper
        )

        curvature_reg_matrix = np.add(
            curvature_matrix, regularization_matrix
        )

        reconstruction = np.linalg.solve(
            curvature_reg_matrix,
            data_vector
        )



        # except np.linalg.LinAlgError:
        #     raise Exception

        inv = inversion(
            masked_interferometer=masked_interferometer,
            mapper=mapper,
            regularization=regularization,
            transformed_mapping_matrices=transformed_mapping_matrices,
            regularization_matrix=regularization_matrix,
            curvature_reg_matrix=curvature_reg_matrix,
            reconstruction=reconstruction
        )

        #print(inv.reconstruction)

        f = fit_from_masked_dataset_and_inversion(
            masked_dataset=masked_interferometer,
            inversion=inv
        )
        #exit()

        return -f.evidence

    # NOTE:
    # 1) Why method='COBYLA'
    # 2) Pass a class with all the attributes
    res = optimize.minimize(
        fun_minimize,
        x0=1.0,
        args=(mapper, curvature_matrix, data_vector, transformed_mapping_matrices, masked_interferometer),
        method='COBYLA'
    )
    print(res)
    # fun_minimize(coefficient=1.0, mapper=mapper, curvature_matrix=curvature_matrix, data_vector=data_vector, transformed_mapping_matrices=transformed_mapping_matrices, masked_interferometer=masked_interferometer)
    # #print(res)
    exit()
    """
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #






    min_coefficient = 10**-2.0
    max_coefficient = 10**8.0
    # min_coefficient = 10**1.0
    # max_coefficient = 10**4.0
    #min_coefficient = 10**5.0
    #max_coefficient = 10**7.0
    coefficients = np.logspace(
        np.log10(min_coefficient),
        np.log10(max_coefficient),
        25
    )

    likelihoods, evidences = np.zeros(
        shape=(2, coefficients.shape[0])
    )

    max_values = []
    list_of_reconstruction = []

    array_term_1 = []
    array_term_2 = []
    array_term_3 = []
    array_term_4 = []
    array_term_5 = []

    for i, coefficient in enumerate(coefficients):
        print(i, coefficient)
        temp = False

        # source_galaxy = al.Galaxy(
        #     redshift=source_redshift,
        #     pixelization=pixelization,
        #     regularization=al.reg.Constant(
        #         coefficient=coefficient
        #     ),
        # )
        #
        # tracer = al.Tracer.from_galaxies(
        #     galaxies=[*lens_galaxies, source_galaxy]
        # )


        regularization = al.reg.Constant(
            coefficient=coefficient
        )

        regularization_matrix = regularization.regularization_matrix_from_mapper(
            mapper=mapper
        )


        # plt.figure()
        # plt.imshow(curvature_matrix)
        # plt.colorbar()
        # plt.show()
        # exit()


        # NOTE: The "curvature_matrix" has already been computed ...
        curvature_reg_matrix = np.add(
            curvature_matrix, regularization_matrix
        )

        try:
            values = np.linalg.solve(
                curvature_reg_matrix,
                data_vector
            )

            temp = True
        except:
            print("Can not perform the inversion ...")

        # except np.linalg.LinAlgError:
        #     raise Exception

        if temp:
            inv = inversion(
                masked_interferometer=masked_interferometer,
                mapper=mapper,
                regularization=regularization,
                transformed_mapping_matrices=transformed_mapping_matrices,
                regularization_matrix=regularization_matrix,
                curvature_reg_matrix=curvature_reg_matrix,
                reconstruction=values
            )

            #print(inv.reconstruction)

            f = fit_from_masked_dataset_and_inversion(
                masked_dataset=masked_interferometer,
                inversion=inv
            )

            # #autolens_plot_utils.plot_fit(fit=f)
            #
            # print(i, coefficient, f.figure_of_merit)
            # # inversion = al.Inversion(
            # #     noise_map=masked_interferometer.noise_map,
            # #     mapper=mapper,
            # #     regularization=regularization,
            # #     regularization_matrix=regularization_matrix,
            # #     curvature_reg_matrix=curvature_reg_matrix,
            # #     reconstruction=values
            # # )
            #

            reconstruction = f.inversion.reconstruction
            max_values.append(np.max(reconstruction))
            list_of_reconstruction.append(reconstruction)


            #likelihoods[i] = f.likelihood

            if al.__version__ in ["0.45.0"]:
                evidences[i] = f.evidence

                # term_1, term_2, term_3, term_4, term_5 = f.evidence_terms

            if al.__version__ in ["1.8.1"]:
                evidences[i] = f.log_evidence

                term_1, term_2, term_3, term_4, term_5 = f.log_evidence_terms


            # term_1, term_2, term_3, term_4, term_5 = f.evidence_terms

            array_term_1.append(term_1)
            array_term_2.append(term_2)
            array_term_3.append(term_3)
            array_term_4.append(term_4)
            array_term_5.append(term_5)

        else:
            evidences[i] = np.nan





    # plt.figure()
    # plt.plot(coefficients, np.asarray(array_term_1), label=r"$term_1$")
    # plt.plot(coefficients, np.asarray(array_term_2), label=r"$term_2$")
    # plt.plot(coefficients, np.asarray(array_term_3), label=r"$term_3$")
    # plt.plot(coefficients, np.asarray(array_term_4), label=r"$term_4$")
    # plt.plot(coefficients, np.asarray(array_term_5), label=r"$term_5$")
    # #plt.plot(coefficients, likelihoods, label="likelihood")
    # #plt.plot(coefficients, evidences, label="evidence")
    # plt.xscale("log")
    # plt.yscale("symlog")
    # plt.xlabel("Regularization Coefficient", fontsize=15)
    # #plt.ylabel("Bayesian Evidence", fontsize=15)
    # plt.legend()
    # plt.show()
    # exit()

    # figure, axes = plt.subplots(nrows=1, ncols=5)
    # axes[0].plot(coefficients, np.asarray(array_term_1), label=r"$term_1$")
    # axes[1].plot(coefficients, np.asarray(array_term_2), label=r"$term_2$")
    # axes[2].plot(coefficients, np.asarray(array_term_3), label=r"$term_3$")
    # axes[3].plot(coefficients, np.asarray(array_term_4), label=r"$term_4$")
    # axes[4].plot(coefficients, np.asarray(array_term_5), label=r"$term_5$")
    #
    # for i in range(axes.shape[0]):
    #     axes[i].set_xscale("log")
    # plt.show()

    # plt.figure()
    # plt.plot(coefficients, evidences)
    # plt.xscale("log")
    # plt.xlabel(
    #     "Regularization Coefficient", fontsize=15
    # )
    # plt.ylabel(
    #     "Bayesian Evidence", fontsize=15
    # )
    # plt.show()
    # exit()

    #print(coefficients[np.where(evidences == np.max(evidences))])

    return coefficients, evidences, array_term_1, array_term_2, array_term_3, array_term_4, array_term_5, list_of_reconstruction, max_values
