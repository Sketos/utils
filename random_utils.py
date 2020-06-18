import random
import time


def seed_generator():

    R = random.SystemRandom(
        time.time()
    )

    seed = int(R.random() * 100000)

    return seed


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
        "#{}".format(
            ''.join([
                random.choice('0123456789ABCDEF') for j in range(6)
            ])
        )
        for i in range(length_of_list)
    ]

    return list_of_random_colors


if __name__ == "__main__":

    print(
        generate_list_of_random_colors(length_of_list=2)
    )
