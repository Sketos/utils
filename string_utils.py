

def remove_substring_from_end_of_string(string, substring):

    if substring and string.endswith(substring):
        return string[:-len(substring)]
    else:
        raise ValueError(
            "{} does not end with {}".format(string, substring)
        )


def remove_substring_from_start_of_string(string, substring):

    if substring and string.startswith(substring):
        return string[len(substring):]
    else:
        raise ValueError(
            "{} does not start with {}".format(string, substring)
        )


if __name__ == "__main__":

    string = "hello"
    substring = "he"
    string_after = remove_substring_from_start_of_string(
        string=string, substring=substring
    )
    print(string, string_after)

    string_after = remove_substring_from_end_of_string(
        string=string, substring="lo"
    )
    print(string, string_after)
