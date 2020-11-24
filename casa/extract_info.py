

def getvarcol_wrapper(ms, table, colname):

    if os.path.isdir(ms):
        tb.open(
            "{}/{}".format(ms, table)
        )

        if tb.isvarcol(colname):
            col = np.squeeze(
                tb.getvarcol(colname)
            )
        else:
            raise ValueError(
                "The column, named \'{}\', is not variable".format(colname)
            )

        tb.close()
    else:
        raise IOError(
            "{} does not exist".format(ms)
        )

    return col


def get_chan_freq(vis):

    tb.open(
        "{}/SPECTRAL_WINDOW".format(vis)
    )

    chan_freq = np.squeeze(
        tb.getcol("CHAN_FREQ")
    )

    tb.close()

    return chan_freq


def spw_frequencies(col, structure):
    pass


def structure_iterator(structure):

    iterator = []
    for key, value in structure.items():
        iterator.append((key, value))

    return iterator


if __name__ == "__main__":
    pass

    # ms = "uid___A002_Xc8ed16_X8a0.ms"
    #
    # a = getvarcol_wrapper(ms=ms, table="SPECTRAL_WINDOW", colname="CHAN_FREQ")
    #
    # print(a)

    structure = {
        "r1":2,
        "r2":3,
        "r3":0,
        "r4":1,
    }
