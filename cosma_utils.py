import os


def running_on_cosma():

    if os.environ["HOME"].startswith("/cosma"):
        return True
    return False


if __name__ == "__main__":

    if running_on_cosma():
        print(
            "This script is running on cosma"
        )
    else:
        print(
            "This script is NOT running on cosma"
        )
