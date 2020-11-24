import os
import sys

import autofit as af
import autolens as al

sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)
import string_utils as string_utils
import list_utils as list_utils
import directory_utils as directory_utils


def aggregator_wrapper(output_directory, phase_folders, pipeline, phase, ending_string="optimizer_backup", return_agg=False):

    directory_updated_with_folder_names = directory_utils.directory_update_with_folder_names(
        directory=output_directory,
        folder_names=phase_folders
    )

    list_of_directory_trees_after_filtering = list_utils.filter_input_list_of_strings_after_split_with_list_of_string_and_ending_string(
        input_list_of_strings=directory_utils.get_list_of_directory_trees_in_directory(
            directory=directory_updated_with_folder_names
        ),
        split_character="/",
        list_of_string=[
            pipeline,
            phase
        ],
        ending_string=ending_string
    )

    if len(list_of_directory_trees_after_filtering) == 1:
        agg = af.Aggregator(
            directory=string_utils.remove_substring_from_end_of_string(
                string=list_of_directory_trees_after_filtering[0],
                substring="/{}".format(ending_string)
            ),
        )
    else:
        raise ValueError(
            "{}".format(len(list_of_directory_trees_after_filtering))
        )

    if return_agg:
        return agg



    # # NOTE:
    # galaxies = [out.most_likely_instance for out in agg.values("output")]
    #
    # if len(galaxies) == 1:
    #     galaxies = galaxies[0]
    # else:
    #     raise ValueError
    #
    # return galaxies


def tracer_from_agg(agg):

    galaxies = [out.most_likely_instance for out in agg.values("output")]

def tracer_from_phase(phase_directory):

    agg = af.Aggregator(directory=phase_directory, )

    ml_instance = [out.most_likely_instance
        for out in agg.values("output")
    ]
    ml_instance = ml_instance[0]

    return al.Tracer.from_galaxies(
        galaxies=ml_instance.galaxies
    )


if __name__ == "__main__":

    pass
