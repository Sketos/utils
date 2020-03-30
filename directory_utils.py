

def directory_update_with_folder_names(directory, folder_names):

    directory = sanitize_directory(
        directory=directory
    )

    for name in folder_names:
        directory += "/" + name

    return directory


def sanitize_directory(directory):

    if directory[-1] == "/":
        return directory[:-1]
    return directory


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
    run_tests()
