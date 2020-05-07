


def func(string_i, string_j, string):

    return string_i + string + string_j


def remove_substring_from_end_of_string(string, substring):

    if substring and string.endswith(substring):
        return string[:-len(substring)]
    else:
        raise ValueError


if __name__ == "__main__":

    print(func(string_i="a", string_j="b", string="__with__"))
