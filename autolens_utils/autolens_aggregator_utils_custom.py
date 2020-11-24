import os
import sys


sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)
import string_utils as string_utils

if __name__ == "__main__":

    filename = "/Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/GAMA15-1/2013.1.00358.S/pipeline_lens_sie_x2__source__sersic/general/source__EllipticalSersic__no_shear/phase_1__lens_sie_x2__source_EllipticalSersic/phase_tag__rs_shape_128x128__rs_pix_0.04x0.04__sub_1/model.results"
    #filename = "/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/output/COSMA/phase_1__ALESS_017.1/model.results"

    f = open(filename, "r")

    lines = f.readlines()
    #print(len(lines))

    #strings = ["profiles", "model_1"]

    string = "galaxies"

    MP = {}
    MP_1sigma_dict = {}
    MP_1sigma = False
    MP_1sigma_counter = 0
    MP_3sigma = False
    MP_3sigma_counter = 0

    MP_1sigma_stage_1 = False
    MP_1sigma_stage_2 = False
    MP_1sigma_stage_3 = False

    # ++++++++++++++++++++++++++++++++++++++++ #
    # NOTE: TESTING
    list1 = ['', '', '', '', 'a']

    # j = 0
    # for i in range(len(list1)):
    #     if list1[i]

    def all_same_to_value(items, value=''):
        return all(x == value for x in items)

    def string_startswidth_n_tabs(string, n=1, return_length=False):
        splitted_string = string.split(" ")


        #print(splitted_string)
        if all_same_to_value(items=splitted_string[:int(4 * n)], value=''):
            if return_length:
                return True, len(splitted_string)
            else:
                return True
            #print("True")
        else:
            if return_length:
                return False, len(splitted_string)
            else:
                return False
            #print("False")

        # if len(splitted_string) == int(4 * n + 1):
        #     #return True
        #     print("True")
        # else:
        #     #return False
        #     print("False")

    def string_startswidth_n_tabs_and_ends(string, n=1):

        condition, length = string_startswidth_n_tabs(
            string=string, n=n, return_length=True
        )

        if condition:
            if length == int(4 * n + 1):
                return True
            else:
                return False
        else:
            return False


    #exit()
    # ++++++++++++++++++++++++++++++++++++++++ #


    # ++++++++++++++++++++++++++++++++++++++++ #
    # NOTE: Dev
    def split_list_of_strings(list_of_strings, char):

        if char == "\t":
            return [string.split(char)[0] for string in list_of_strings]
        else:
            raise ValueError("This has not been implemented yet")

    lines_t_split = split_list_of_strings(
        list_of_strings=lines, char="\t"
    )

    n_i = 0
    n_j = 0

    base_condition = False
    condition_1 = False
    condition_2 = True

    counter = 0
    for i, line in enumerate(lines_t_split):

        if line.startswith('Most probable model'):
            #print(i, line)

            line_as_list_of_strings = line.split(" ")


            temp = string_utils.remove_list_of_chars_from_string(
                string=line_as_list_of_strings[3], chars=["(", ")", ","]
            )

            if temp == "1.0":
                n_i = i

                base_condition = True

        if base_condition:
            if line == "\n":
                counter += 1

        if counter == 2.0:
            n_j = i
            base_condition = False


        # if line == '\n':
        #     print(i)

    print(n_i, n_j)
    print(lines_t_split[n_i:n_j])
    exit()
    # ++++++++++++++++++++++++++++++++++++++++ #


    for i, line in enumerate(lines):

        # NOTE: Splitting the string in the manner there is no emprty list
        line_t_split = line.split("\t")[0]
        #print(line_as_list_of_strings, line_as_list_of_strings[0])

        #temp = line_as_list_of_strings[0].split(" ")

        #string_startswidth_tab(string=line_t_split)
        #exit()

        line_t_split_as_list_of_strings = line_t_split.split(" ")


        if line_t_split.startswith('Most probable model'):
            #print(line_t_split_as_list_of_strings)

            temp = string_utils.remove_list_of_chars_from_string(
                string=line_t_split_as_list_of_strings[3], chars=["(", ")", ","]
            )

            if temp == "1.0":
                MP_1sigma = True
            # if temp == 3.0:
            #     MP_3sigma = True
            #if line_as_list_of_strings[3]

        if MP_1sigma:
            print(line_t_split_as_list_of_strings)

            # # NOTE: Is this nessesary?
            # if line_t_split_as_list_of_strings[0].startswith(string):
            #     MP_1sigma_stage_1 = True

            # if MP_1sigma_stage_1:
            #     print(line_t_split_as_list_of_strings)

            if not MP_1sigma_stage_1:
                if string_startswidth_n_tabs_and_ends(string=line_t_split, n=1):

                    string_name = string_utils.remove_list_of_chars_from_string(
                        string=line_t_split_as_list_of_strings[-1], chars=["(", ")", ",", "\n"]
                    )
                    #print(string_temp)

                    MP_1sigma_dict[string_name] = {}

                    #exit()

                    MP_1sigma_stage_1 = True


    print(MP_1sigma_dict)



    #
    #
    #
    #
    #
    #
    #     # if list_of_strings[0].startswith((' ', '\t')) and list_of_strings[0].endswith("\n"):
    #     #     print(list_of_strings)
    #     """
    #     if len(list_of_strings) == 6:
    #         if list_of_strings[0] == 'Most' and list_of_strings[1] == 'probable' and list_of_strings[2] == 'model':
    #
    #             if list_of_strings[3].endswith("3.0"):
    #                 MP_3sigma = True#;print("3")
    #
    #
    #             if list_of_strings[3].endswith("1.0"):
    #                 MP_1sigma = True#;print("1")
    #
    #
    #
    #
    #             # print(list_of_strings)
    #             # # string = string_utils.remove_substrings_from_start_and_end_of_string(
    #             # #     string=list_of_strings[-1], substrings=["(", ")"]
    #             # # )
    #             # #
    #             # # print(string)
    #
    #     if not list_of_strings:
    #
    #         if MP_1sigma == True:
    #             if MP_1sigma_counter == 0:
    #                 MP_1sigma_counter += 1
    #             else:
    #                 MP_1sigma = False
    #
    #         if MP_3sigma == True:
    #             if MP_3sigma_counter == 0:
    #                 MP_3sigma_counter += 1
    #             else:
    #                 MP_3sigma = False
    #
    #     if MP_3sigma == True and len(list_of_strings) == 4:
    #         name = list_of_strings[0]
    #
    #         # NOTE: Turn this into a function ...
    #         MP[list_of_strings[0]] = {
    #             "mean":list_of_strings[1],
    #             "l":float(
    #                 string_utils.remove_list_of_chars_from_string(
    #                     string=list_of_strings[2], chars=["(", ")", ","]
    #                 )
    #             ),
    #             "h":float(
    #                 string_utils.remove_list_of_chars_from_string(
    #                     string=list_of_strings[3], chars=["(", ")", ","]
    #                 )
    #             ),
    #         }
    #
    #
    #     #print(list_of_strings, MP_3sigma, MP_1sigma)
    #     """
    # #print(MP)
