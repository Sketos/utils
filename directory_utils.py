import os


def get_list_of_directory_trees_in_directory(directory):
    return [
        x[0]
        for x in os.walk(directory)
    ]


def create_directory_tree_from_list_of_strings(list_of_strings, base_directory_of_directory_tree=''):

    directory_tree = base_directory_of_directory_tree

    for name in list_of_strings:
        if name:
            directory_tree += "/" + name
            if not os.path.isdir(directory_tree):
                os.system(
                    "mkdir {}".format(directory_tree)
                )


def directory_update_with_folder_names(directory, folder_names, create_directory=False):

    directory = sanitize_directory(
        directory=directory
    )

    for name in folder_names:
        directory += "/" + name
        if create_directory:
            if not os.path.isdir(directory):
                os.system(
                    "mkdir {}".format(directory)
                )

    return directory


def sanitize_directory(directory):

    if directory[-1] == "/":
        return directory[:-1]
    return directory


def move_directory_to_path(directory, path):

    if os.path.isdir(directory):
        if os.path.isdir(path):
            os.system("mv {} {}".format(directory, path))


# ---------------------------------------------------------------------------- #


def test__sanitize_directory():

    directory_i = "./folder1/folder2/"
    directory_o = "./folder1/folder2"

    directory_i = sanitize_directory(
        directory=directory_i
    )

    if directory_i != directory_o:
        raise ValueError


# ---------------------------------------------------------------------------- #


def run_tests():

    test__sanitize_directory()



if __name__ == "__main__":
    #run_tests()

    # move_directory_to_path(
    #     directory="./wrappers/",
    #     path="./dir_test/dir_level_0__1/dir_level_1__1/"
    # )

    for directory in get_list_of_directory_trees_in_directory(directory="/Users/ccbh87/"):
        if directory.endswith("HATLAS_J091043-000322"):
            print(directory)
