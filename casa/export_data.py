
def getcol_wrapper(ms, table, colname):

    if os.path.isdir(ms):
        tb.open(
            "{}/{}".format(ms, table)
        )

        col = np.squeeze(
            tb.getcol(colname)
        )

        tb.close()
    else:
        raise IOError(
            "{} does not exist".format(ms)
        )

    return col


def get_chan_freq(ms):

    return getcol_wrapper(
        ms=ms,
        table="SPECTRAL_WINDOW",
        colname="CHAN_FREQ"
    )


def get_visibilities(ms):

    if os.path.isdir(ms):
        data = getcol_wrapper(
            ms=ms,
            table="",
            colname="DATA"
        )
    else:
        raise IOError(
            "{} does not exisxt".format(ms)
        )

    visibilities = np.stack(
        arrays=(data.real, data.imag),
        axis=-1
    )

    return visibilities


# def export_visibilities_from_ms(vis, width, spw, contsub):
#
#     filename = "width_{}/visibilities_spw_{}{}.fits".format(
#         width,
#         spw,
#         ".contsub" if contsub else ''
#     )
#     if os.path.isfile(filename):
#         print(
#             "{} already exists".format(filename)
#         )
#     else:
#         visibilities = get_visibilities(
#             ms="width_{}/{}".format(
#                 width,
#                 vis if vis.endswith(".statwt") else "{}.statwt".format(vis)
#             )
#         )
#
#         # NOTE:
#         visibilities = np.average(
#             a=visibilities,
#             axis=0
#         )
#
#         print(
#             "shape (visibilities):", visibilities.shape
#         )
#         fits.writeto(
#             filename=filename,
#             data=visibilities,
#             overwrite=True
#         )




def get_uv_wavelengths(ms):

    def convert_array_to_wavelengths(array, frequency):

        array_converted = (
            (array * units.m) * (frequency * units.Hz) / constants.c
        ).decompose()

        return array_converted.value


    if os.path.isdir(ms):
        uvw = getcol_wrapper(
            ms=ms,
            table="",
            colname="UVW"
        )
    else:
        raise IOError(
            "{} does not exisxt".format(ms)
        )

    chan_freq = get_chan_freq(
        ms=ms
    )

    chan_freq_shape = np.shape(chan_freq)
    if np.shape(chan_freq):

        u_wavelengths, v_wavelengths = np.zeros(
            shape=(
                2,
                chan_freq_shape[0],
                uvw.shape[1]
            )
        )

        for i in range(chan_freq_shape[0]):
            u_wavelengths[i, :] = convert_array_to_wavelengths(array=uvw[0, :], frequency=chan_freq[i])
            v_wavelengths[i, :] = convert_array_to_wavelengths(array=uvw[1, :], frequency=chan_freq[i])

    else:

        u_wavelengths = convert_array_to_wavelengths(array=uvw[0, :], frequency=chan_freq)
        v_wavelengths = convert_array_to_wavelengths(array=uvw[1, :], frequency=chan_freq)


    uv_wavelengths = np.stack(
        arrays=(u_wavelengths, v_wavelengths),
        axis=-1
    )

    return uv_wavelengths


# def export_uv_wavelengths_from_ms(ms, width, spw, contsub):
#
#     filename = "width_{}/uv_wavelengths_spw_{}{}.fits".format(
#         width,
#         spw,
#         ".contsub" if contsub else ''
#     )
#     if os.path.isfile(filename):
#         print(
#             "{} already exists".format(filename)
#         )
#     else:
#         uv_wavelengths = get_uv_wavelengths(
#             ms="width_{}/{}".format(
#                 width,
#                 ms if ms.endswith(".statwt") else "{}.statwt".format(ms)
#             )
#         )
#
#         print(
#             "shape (uv_wavelengths):", uv_wavelengths.shape
#         )
#         fits.writeto(
#             filename=filename,
#             data=uv_wavelengths,
#             overwrite=True
#         )


def get_suffix(spw, contsub):

    return "spw_{}{}".format(
        spw,
        ".contsub" if contsub else ''
    )


def export_uv_wavelengths(uv_wavelengths, output_directory, suffix):

    filename = "{}/uv_wavelengths_{}.fits".format(
        output_directory, suffix
    )

    if os.path.isfile(filename):
        print(
            "{} already exists".format(filename)
        )
    else:
        fits.writeto(
            filename=filename,
            data=uv_wavelengths,
            overwrite=True
        )


def get_sigma(ms):

    if os.path.isdir(ms):
        sigma = getcol_wrapper(
            ms=ms,
            table="",
            colname="SIGMA"
        )
    else:
        raise IOError(
            "{} does not exisxt".format(ms)
        )

    return sigma


def average(array, n_elements):

    if len(array) % n_elements == 0:
        array_averaged = np.mean(
            a=array.reshape(-1, n_elements),
            axis=1
        )
    else:
        raise ValueError(
            "The length of the array is not divisible by {}".format(n_elements)
        )

    return array_averaged


# def export_sigma(ms, width, spw, contsub):
#
#     filename = "width_{}/sigma_spw_{}{}.fits".format(
#         width,
#         spw,
#         ".contsub" if contsub else ''
#     )
#     if os.path.isfile(filename):
#         print(
#             "{} already exists".format(filename)
#         )
#     else:
#         sigma = get_sigma(
#             ms="width_{}/{}".format(
#                 width,
#                 ms if ms.endswith(".statwt") else "{}.statwt".format(ms)
#             )
#         )
#
#         sigma = np.average(
#             a=sigma,
#             axis=0
#         )
#
#         num_chan = getcol_wrapper(
#             ms=ms,
#             table="SPECTRAL_WINDOW",
#             colname="NUM_CHAN"
#         )
#
#         if num_chan == width:
#             pass
#         else:
#             sigma = np.tile(
#                 A=sigma,
#                 reps=(
#                     int(num_chan / width), 1
#                 )
#             )
#
#         sigma = np.stack(
#             arrays=(sigma, sigma),
#             axis=-1
#         )
#
#         print(
#             "shape (sigma):", sigma.shape
#         )
#         fits.writeto(
#             filename=filename,
#             data=sigma,
#             overwrite=True
#         )


def get_frequencies(uid, field, spw):

    ms = "{}_field_{}_spw_{}.ms.split.cal".format(
        uid,
        field,
        spw
    )

    if os.path.isdir(ms):
        chan_freq = getcol_wrapper(
            ms=ms,
            table="SPECTRAL_WINDOW",
            colname="CHAN_FREQ"
        )
    else:
        raise IOError(
            "{} does not exist".format(ms)
        )

    return chan_freq
