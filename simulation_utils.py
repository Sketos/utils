from astropy import units


import casa_utils as casa_utils


def generate_uv_wavelengths(
    uv,
    central_frequency,

):

    if uv.shape[0] == 2:
        if len(uv.shape) < 2 or len(uv.shape) > 3:
            raise ValueError(
                "The shape is not right ..."
            )
        if len(uv.shape) == 2:
            pass
        if len(uv.shape) == 3:
            raise ValueError(
                "This is not implemented yet"
            )
    else:
        raise ValueError(
            "The shape is not right ..."
        )

    return casa_utils.convert_uv_coords_from_meters_to_wavelengths(
        uv=uv,
        frequencies=central_frequency.to(units.Hz).value
    )
