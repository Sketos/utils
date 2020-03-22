import os
import numpy as np

from directory_utils import *


# TODO: raise error when args not in dictionary
# TODO: change the name of this function to be more descriptive:
def get_output_from_nested_dictionary(dictionary, *args):
    
    if args and dictionary:
        element = args[0]
        if element:
            value = dictionary.get(element)
            if len(args) == 1:
                return value
            else:
                return get_output_from_nested_dictionary(value, *args[1:])


# ----------------------- #
#
# ----------------------- #


def test__get_output_from_nested_dictionary():
    dictionary = {
        "model_1":{
            "parameters":[0.0, 0.1]
        },
        "model_2":{
            "parameters":[1.0, 0.0]}
    }
    output = get_output_from_nested_dictionary(
        dictionary, *["model_1", "parameters"]
    )
    print(output)


# ----------------------- #
#
# ----------------------- #


def run_tests():
    test__get_output_from_nested_dictionary()


if __name__ == "__main__":
    #run_tests()



    directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer"
    directory_trees = [
        x[0]
        for x in os.walk(directory)
    ]

    # directory_trees_after_filtering = filter_input_list_of_strings_after_split_with_string(
    #     input_list_of_strings=directory_trees, split_character="/", string="lens_sie__source_gaussian"
    # )

    directory_trees_after_filtering = filter_input_list_of_strings_after_split_with_list_of_string(
        input_list_of_strings=directory_trees,
        split_character="/",
        list_of_string=[
            "lens_sie__source_gaussian",
            "phase_2__lens_sie__source_inversion__from_parametric"
        ]
    )

    directory_trees_after_filtering = filter_input_list_of_strings_after_split_with_ending_string(
        input_list_of_strings=directory_trees_after_filtering, split_character="/", ending_string="width"
    )

    for i in range(len(directory_trees_after_filtering)):
        print(i, directory_trees_after_filtering[i])





    # directory = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/interferometer/"
    #
    # pipeline = "lens_sie__source_gaussian"
    # directory += pipeline
    # phase = "phase_2__lens_sie__source_inversion__from_parametric"
    # string = "phase_tag"
    # subdirectories = [x[0] for x in os.walk(directory)]
    # subdirectories_temp = []
    # for i, subdirectory in enumerate(subdirectories):
    #     #print(i, subdirectory.split("/"))
    #     subdirectory_splitted = subdirectory.split("/")
    #     if pipeline in subdirectory_splitted:
    #         #print(subdirectory_splitted[-1])
    #         if subdirectory_splitted[-1].startswith(phase):
    #             subdirectories_temp.append(subdirectory)
    #             print(subdirectory)
    #
    # _totaltime = [
    #     "120s",
    #     "240s",
    #     "360s",
    #     "480s",
    #     "600s",
    #     "1200s",
    #     "1800s",
    #     "2400s",
    #     "3000s",
    #     "3600s"
    # ]


    #print(subdirectories_temp, len(subdirectories_temp))


    # def filter_with_string(string):
    #     pass
    #
    # def filter_with_list_of_strings(list_of_strings):
    #     pass
    #
    #
    # def gather_output_directories(directory, pipeline, phase):
    #     pass
