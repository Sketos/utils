import re

def sanitize_string(string):

    for char in ["(", ")", ",", "#", "%"]:
        string = string.replace(char, "")

    return string


def sanitize_list_of_strings(list_of_strings):

    list_of_strings_temp = []

    for string in list_of_strings:
        list_of_strings_temp.append(
            sanitize_string(string=string)
        )

    return list_of_strings_temp



# NOTE: VERY UGLY
def read_lens_model_parameters_from_model_info(filename):

    if filename.endswith("model.info"):

        f = open(filename, "r")
        lines = f.readlines()

        checks = {"lens":False}
        dict_temp = {}
        for line in lines:

            line_splitted = sanitize_list_of_strings(
                list_of_strings=line.split()
            )

            if "lens" in line_splitted:
                dict_temp["lens"] = {}
                checks["lens"] = True

            if "mass" in line_splitted and checks["lens"]:
                dict_temp["lens"]["mass"] = {}

            if line_splitted[0] in ["centre", "axis_ratio", "phi", "einstein_radius", "slope"]:

                if line_splitted[0] == "centre":
                    #print(line_splitted)
                    # dict_temp["lens"]["mass"][line_splitted[0]] = (
                    #     float(line_splitted[1]),
                    #     float(line_splitted[2])
                    # )

                    for i in range(len(line_splitted) - 1):
                        dict_temp["lens"]["mass"]["{}_{}".format(line_splitted[0], i)] = float(line_splitted[i+1])
                    #dict_temp["lens"]["mass"][line_splitted[0] + "_0"] = float(line_splitted[1])
                    #dict_temp["lens"]["mass"][line_splitted[0] + "_1"] = float(line_splitted[2])

                else:
                    dict_temp["lens"]["mass"][line_splitted[0]] = float(line_splitted[1])

            if "subhalo" in line_splitted:
                break


        return dict_temp

    else:
        raise ValueError()


if __name__ == "__main__":

    pass

    list_of_strings = ['(0.53#45%', '(0.53#45%', '(0.53#45%']


    list_of_strings = sanitize_list_of_strings(list_of_strings=list_of_strings)
    print(list_of_strings)
