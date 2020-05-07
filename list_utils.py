# NOTE: ...

import os
import numpy as np

# NOTE: filter can be turner into a class and also filtering string can be turned into a class


def filter_input_list_of_strings_after_split_with_string(input_list_of_strings, split_character, string):
    """Short summary.

    Parameters
    ----------
    input_list_of_strings : type
        Description of parameter `input_list_of_strings`.
    split_character : type
        Description of parameter `split_character`.
    string : type
        Description of parameter `string`.

    Returns
    -------
    type
        Description of returned object.

    """

    output_list_of_strings = []
    for i, i_string in enumerate(input_list_of_strings):
        i_string_splitted = i_string.split(split_character)
        if string in i_string_splitted:
            output_list_of_strings.append(i_string)

    return output_list_of_strings


def filter_input_list_of_strings_after_split_with_ending_string(input_list_of_strings, split_character, ending_string):

    output_list_of_strings = []
    for i, i_string in enumerate(input_list_of_strings):
        i_string_splitted = i_string.split(split_character)
        if i_string_splitted[-1].startswith(ending_string):
            output_list_of_strings.append(i_string)

    return output_list_of_strings


def filter_input_list_of_strings_after_split_with_starting_string(input_list_of_strings, split_character, starting_string):

    output_list_of_strings = []
    for i, i_string in enumerate(input_list_of_strings):
        i_string_splitted = i_string.split(split_character)
        for j, j_string_splitted in enumerate(i_string_splitted):
            if j_string_splitted.startswith(starting_string):
                output_list_of_strings.append(i_string)

    return output_list_of_strings


def filter_input_list_of_strings_with_starting_string(input_list_of_strings, starting_string):

    output_list_of_strings = []
    for i, i_string in enumerate(input_list_of_strings):
        if i_string.startswith(starting_string):
            output_list_of_strings.append(i_string)

    return output_list_of_strings


def filter_input_list_of_strings_after_split_with_string_and_ending_string(input_list_of_strings, split_character, string, ending_string):

    input_list_of_strings_filtered = filter_input_list_of_strings_after_split_with_string(
        input_list_of_strings=input_list_of_strings, split_character=split_character, string=string
    )

    return filter_input_list_of_strings_after_split_with_ending_string(
        input_list_of_strings=input_list_of_strings_filtered, split_character=split_character, ending_string=ending_string
    )


def filter_input_list_of_strings_after_split_with_list_of_string(input_list_of_strings, split_character, list_of_string):

    output_list_of_strings = []
    for i, i_string in enumerate(input_list_of_strings):
        i_string_splitted = i_string.split(split_character)

        if all([
            string in i_string_splitted
            for string in list_of_string
        ]):
            output_list_of_strings.append(i_string)

    return output_list_of_strings


def filter_input_list_of_strings_after_split_with_list_of_string_and_ending_string(input_list_of_strings, split_character, list_of_string, ending_string):

    input_list_of_strings_filtered = filter_input_list_of_strings_after_split_with_list_of_string(
        input_list_of_strings=input_list_of_strings, split_character=split_character, list_of_string=list_of_string
    )

    return filter_input_list_of_strings_after_split_with_ending_string(
        input_list_of_strings=input_list_of_strings_filtered, split_character=split_character, ending_string=ending_string
    )


# ----------------------- #
# Tests
# ----------------------- #



# ----------------------- #
# Run
# ----------------------- #


if __name__ == "__main__":

    directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer"
    pipeline = "lens_sie__source_gaussian"
    directory += "/" + pipeline
    directory_trees = [
        x[0]
        for x in os.walk(directory)
    ]

    # directory_trees_after_filtering = filter_input_list_of_strings_after_split_with_string_and_ending_string(
    #     input_list_of_strings=directory_trees,
    #     split_character="/",
    #     string="phase_1__lens_sie__source_gaussian",
    #     ending_string="width"
    # )

    # directory_trees_after_filtering = filter_input_list_of_strings_after_split_with_string(
    #     input_list_of_strings=directory_trees,
    #     split_character="/",
    #     string="t_tot__360s"
    # )
    #
    # for i in range(len(directory_trees_after_filtering)):
    #     print(i, directory_trees_after_filtering[i][:200])

    directory_trees_after_filtering = filter_input_list_of_strings_after_split_with_list_of_string(
        input_list_of_strings=directory_trees,
        split_character="/",
        list_of_string=[
            "phase_1__lens_sie__source_gaussian",
            "t_tot__360s"
        ]
    )

    for i in range(len(directory_trees_after_filtering)):
        print(i, directory_trees_after_filtering[i])
