import numpy as np
import matplotlib.pyplot as plt

import autofit as af
import autolens as al

# NOTE:
plt_args = {
    "DFT":{
        "color":"b",
        "markersize":10,
        "alpha":0.5
    },
    "NUFFT":{
        "color":"r",
        "markersize":5,
        "alpha":1.0
    }
}

def get_transformer_key(transformer=None):

    if transformer is None:
        raise ValueError("...")
    elif issubclass(transformer, al.TransformerDFT):
        return "DFT"
    elif issubclass(transformer, al.TransformerNUFFT):
        return "NUFFT"
    else:
        pass

        
# def compare(uv_wavelengths, grid, image, transformers=[al.TransformerDFT, al.TransformerNUFFT]):
#
#     visibilities = np.zeros(
#         shape=(
#             (len(transformers),) + uv_wavelengths.shape
#         )
#     )
#     for i, transformer in enumerate(transformers):
#
#         transformer_temp = transformer(
#             uv_wavelengths=uv_wavelengths,
#             grid=grid.in_radians
#         )
#
#         #transformer_temp.transformed_mapping_matrices_from_mapping_matrix(mapping_matrix=mapping_matrix)
#
#         visibilities[i] = transformer_temp.visibilities_from_image(
#             image=image
#         )
#
#     plt.figure()
#     for i in range(visibilities.shape[0]):
#         plt.plot(
#             visibilities[i, :, 0],
#             visibilities[i, :, 1],
#             linestyle="None",
#             marker="o",
#             alpha=0.5
#         )
#     plt.show()

def func(uv_wavelengths, grid, mapping_matrix, transformers=[al.TransformerDFT, al.TransformerNUFFT]):

    transformed_mapping_matrices = np.zeros(
        shape=(
            (len(transformers), mapping_matrix.shape[1]) + uv_wavelengths.shape
        )
    )

    for i, transformer in enumerate(transformers):

        transformer_temp = transformer(
            uv_wavelengths=uv_wavelengths,
            grid=grid.in_radians
        )

        transformed_mapping_matrices_temp = transformer_temp.transformed_mapping_matrices_from_mapping_matrix(
            mapping_matrix=mapping_matrix
        )
        real_transformed_mapping_matrix = transformed_mapping_matrices_temp[0]
        imag_transformed_mapping_matrix = transformed_mapping_matrices_temp[1]

        transformed_mapping_matrices[i, :, :, 0] = real_transformed_mapping_matrix.T
        transformed_mapping_matrices[i, :, :, 1] = imag_transformed_mapping_matrix.T

    # NOTE:
    for j in range(transformed_mapping_matrices.shape[1]):

        plt.figure()
        for i in range(transformed_mapping_matrices.shape[0]):

            args = plt_args[
                get_transformer_key(transformer=transformers[i])
            ]

            plt.plot(
                transformed_mapping_matrices[i, j, :, 0],
                transformed_mapping_matrices[i, j, :, 1],
                linestyle="None",
                marker="o",
                markersize=args["markersize"],
                color=args["color"],
                alpha=args["alpha"]
            )
        plt.show()
