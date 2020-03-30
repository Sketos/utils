import random


# NOTE:
NUMBER_OF_CHARACTERS_FOR_COLOR_STRING = 6


def generate_list_of_random_colors(length_of_list):
    """Short summary.

    Parameters
    ----------
    length_of_list : type
        Description of parameter `length_of_list`.

    Returns
    -------
    type
        Description of returned object.

    """

    list_of_random_colors = [
        "#" + ''.join([
            random.choice('0123456789ABCDEF') for j in range(NUMBER_OF_CHARACTERS_FOR_COLOR_STRING)
        ])
        for i in range(length_of_list)
    ]

    return list_of_random_colors


if __name__ == "__main__":

    list_of_random_colors = generate_list_of_random_colors(
        length_of_list=10
    )
    print(list_of_random_colors)
