import json
import numpy as np


def get_antennas_names(ms):

    tb.open(ms + "/ANTENNA")

    # NOTE: ...
    antenna_names = np.squeeze(
        tb.getcol("NAME")
    )

    tb.close()

    return antenna_names



def load_antenna_names(directory):

    antenna_names = np.genfromtxt(
        "{}/antenna_names.txt".format(directory),
        dtype=np.str
    )

    return antenna_names


def load_baseline_lengths(filename):

    # NOTE: It is not nessesary that the file is "".json" type
    if filename.endswith(".json"):
        with open(filename, "r") as file:
            baseline_lengths = json.loads(
                file.read()
            )

            return baseline_lengths
