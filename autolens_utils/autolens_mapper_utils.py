import autolens as al

from autoarray.util import inversion_util


def mapped_reconstruction(mapper, reconstruction):
    mapped_reconstructed_image = inversion_util.mapped_reconstructed_data_from_mapping_matrix_and_reconstruction(
        mapping_matrix=mapper.mapping_matrix,
        reconstruction=reconstruction,
    )

    return mapper.grid.mapping.array_stored_1d_from_array_1d(
        array_1d=mapped_reconstructed_image
    )
