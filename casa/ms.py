
def remove_substring_from_end_of_string(string, substring):

    if substring and string.endswith(substring):
        return string[:-len(substring)]
    else:
        raise ValueError


def getvarcol_wrapper(ms, table, colname):

    if os.path.isdir(ms):
        tb.open(
            "{}/{}".format(ms, table)
        )

        if tb.isvarcol(colname):

            col = np.squeeze(
                b.getvarcol(colname)
            )
        else:
            raise ValueError("...")

        tb.close()
    else:
        raise IOError(
            "{} does not exist".format(ms)
        )

    return col


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


def get_spw_ids(ms):

    return getcol_wrapper(
        ms=ms,
        table="DATA_DESCRIPTION",
        colname="SPECTRAL_WINDOW_ID"
    )


def get_num_chan(ms):

    return getcol_wrapper(
        ms=ms,
        table="SPECTRAL_WINDOW",
        colname="NUM_CHAN"
    )


def initialize(uid, field):

    outputvis = "{}_field_{}.ms.split.cal".format(
        uid, field
    )

    if not os.path.isdir(outputvis):

        if os.path.isdir(
            "{}.ms.split.cal".format(uid)
        ):

            #NOTE: In this casa we are splitting out the data column
            split(
                vis="{}.ms.split.cal".format(
                    uid
                ),
                outputvis=outputvis,
                keepmms=True,
                field=field,
                spw="",
                datacolumn="data",
                keepflags=False
            )

        elif os.path.isdir(
            "{}.ms".format(uid)
        ):

            #NOTE: In this casa we are splitting out the corrected data column. Check to make sure that this exists
            split(
                vis="{}.ms".format(
                    uid
                ),
                outputvis=outputvis,
                keepmms=True,
                field=field,
                spw="",
                datacolumn="corrected",
                keepflags=False
            )

        else:
            raise ValueError("...")

    return outputvis


def main(vis, spw, width=None, contsub=False, outputvis_directory="."):

    outputvis = "{}_spw_{}.ms.split.cal".format(
        remove_substring_from_end_of_string(
            string=vis,
            substring=".ms.split.cal"
        ),
        spw
    )

    spw_ids = get_spw_ids(
        ms=vis,
    )

    if isinstance(spw_ids, (list, np.ndarray)):
        spw_ids_is_list = True

        if int(spw) in spw_ids:
            spw_idx = np.squeeze(
                np.where(
                    np.asarray(spw_ids) == int(spw)
                )
            )
        else:
            print(
                "spw={} is not in spw IDs".format(spw)
            )
    else:
        spw_ids_is_list = False

    num_chan = get_num_chan(
        ms=vis
    )

    if spw_ids_is_list:
        if len(spw_ids) == len(num_chan):
            spw_num_chan = num_chan[spw_idx]
        else:
            raise ValueError(
                "Something weird is going on ..."
            )
    else:
        spw_num_chan = num_chan


    if not os.path.isdir(outputvis):
        split(
            vis=vis,
            outputvis=outputvis,
            keepmms=True,
            field=field,
            spw=spw,
            datacolumn="data",
            keepflags=False
        )
    else:
        print(
            "{} already exist".format(outputvis)
        )

    # TODO: ...
    if not os.path.isdir(
        "{}.statwt".format(outputvis)
    ):
        os.system(
            "cp -r {} {}".format(
                outputvis,
                "{}.statwt".format(outputvis)
            )
        )

        # NOTE: timebin is not yet implemented.
        statwt(
            vis="{}.statwt".format(outputvis),
            datacolumn="data"
        )
    else:
        print(
            "{} already exist.".format(
                "{}.statwt".format(outputvis)
            )
        )

    outputvis = "{}.statwt".format(
        outputvis
    )

    if width > spw_num_chan:
        raise ValueError(
            "The width={} is larger than the number of channels (n={}) for spw={}".format(
                width,
                spw_num_chan,
                spw
            )
        )
    else:
        outputvis_directory = "{}/width_{}".format(
            outputvis_directory,
            width
        )

        # NOTE: ...
        if not os.path.isdir(outputvis_directory):
            os.system(
                "mkdir {}".format(outputvis_directory)
            )
        else:
            print(
                "{} already exist.".format(
                    outputvis_directory
                )
            )

        # NOTE: ...
        if not os.path.isdir(
            "{}/{}".format(
                outputvis_directory,
                outputvis
            )
        ):
            split(
                vis=outputvis,
                outputvis="{}/{}".format(
                    outputvis_directory,
                    outputvis
                ),
                keepmms=True,
                field=0,
                spw="0",
                width=width,
                datacolumn="data",
                keepflags=False
            )
        else:
            print(
                "{} already exist.".format(
                    "{}/{}".format(
                        outputvis_directory,
                        outputvis
                    )
                )
            )


def get_chan_freq(vis):

    tb.open(
        "{}/SPECTRAL_WINDOW".format(vis)
    )

    chan_freq = np.squeeze(
        tb.getcol("CHAN_FREQ")
    )

    tb.close()

    return chan_freq


def get_antennas(vis):

    tb.open(
        vis, nomodify=True
    )

    antenna1 = np.squeeze(
        tb.getcol("ANTENNA1")
    )
    antenna2 = np.squeeze(
        tb.getcol("ANTENNA2")
    )

    tb.close()

    return np.stack(
        arrays=(antenna1, antenna2),
        axis=-1
    )


def export_antennas(directory, antennas):

    if os.path.isdir(directory):
        fits.writeto(
            "{}/antennas.fits".format(
                sanitize_directory(directory=directory)
            ),
            data=antennas,
            overwrite=True
        )
    else:
        raise IOError(
            "The directory {} does not exist".format(directory)
        )


def export_antennas_from_vis(vis, directory, antennas):
    pass


def get_time(vis):

    tb.open(
        vis, nomodify=True
    )

    time = np.squeeze(
        tb.getcol("TIME")
    )

    tb.close()

    return time


def export_time(directory, time):

    if os.path.isdir(directory):
        fits.writeto(
            "{}/time.fits".format(
                sanitize_directory(directory=directory)
            ),
            data=time,
            overwrite=True
        )
    else:
        raise IOError(
            "The directory {} does not exist".format(directory)
        )


# def export_data(directory, name, data):
#
#     if os.path.isdir(directory):
#         fits.writeto(
#             "{}/{}.fits".format(
#                 sanitize_directory(
#                     directory=directory
#                 ),
#                 name
#             ),
#             data=data,
#             overwrite=True
#         )
#     else:
#         raise IOError(
#             "The directory {} does not exist".format(directory)
#         )
#
#
# def export_time(directory, time):
#
#     export_data(
#         directory=directory,
#         name="time",
#         data=time
#     )

if __name__ == "__main__":
    pass
