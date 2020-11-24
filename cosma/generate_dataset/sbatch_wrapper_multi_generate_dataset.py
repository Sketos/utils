import os
import sys


def sbatch_wrapper(args, directory):

    def helper(arg, list_of_args):

        if arg in list_of_args:
            _arg = arg
        else:
            raise ValueError(
                "The {} is not supported".format(arg)
            )

        return _arg


    # NOTE: ...
    if len(args) != 4:
        raise ValueError(
            "The script s expecting 3 arguments to be passed, {} were given".format(
                len(args) - 1
            )
        )

    arg0 = helper(
        arg=args[0],
        list_of_args=[
            "5.8",
            "5.9",
            "5.10"
        ]
    )

    arg1 = helper(
        arg=args[1],
        list_of_args=["10800s"]
    )

    arg2 = helper(
        arg=args[2],
        list_of_args=[
            "model_1",
            "model_1_with_src_clumps",
            "model_2",
            "model_2_with_src_clumps",
            "model_3",
            "model_3_with_src_clumps",
            "model_4",
            "model_4_with_src_clumps",
            "model_5",
            "model_5_with_src_clumps",
        ]
    )

    arg3 = helper(
        arg=args[3],
        list_of_args=[
            "None",
            "1e8",
            "1e9",
            "1e10",
        ]
    )


    # NOTE:
    out = "{}/output__{}__{}__{}__{}__%A.out".format(
        directory, arg0, arg1, arg2, arg3
    )
    err = "{}/output__{}__{}__{}__{}__%A.err".format(
        directory, arg0, arg1, arg2, arg3
    )

    sbatch_filename = "sbatch_for_wrapper_generate_dataset"
    if not os.path.isfile(sbatch_filename):
        raise IOError(
            "The sbatch script {} does not exist".format(sbatch_filename)
        )

    command = "sbatch --export=ALL,arg0={},arg1={},arg2={},arg3={} --output={} --error={} {}".format(
        arg0,
        arg1,
        arg2,
        arg3,
        out,
        err,
        sbatch_filename
    )
    os.system(command)


if __name__ == "__main__":

    directory = "/cosma/home/durham/dc-amvr1/simulations/"

    list_of_args = [
        ["5.8", "10800s", "model_1", "None"],
        ["5.8", "10800s", "model_1", "1e8"],
        ["5.8", "10800s", "model_1", "1e9"],
        ["5.8", "10800s", "model_1", "1e10"],
        ["5.9", "10800s", "model_1", "None"],
        ["5.9", "10800s", "model_1", "1e8"],
        ["5.9", "10800s", "model_1", "1e9"],
        ["5.9", "10800s", "model_1", "1e10"],
        ["5.10", "10800s", "model_1", "None"],
        ["5.10", "10800s", "model_1", "1e8"],
        ["5.10", "10800s", "model_1", "1e9"],
        ["5.10", "10800s", "model_1", "1e10"],
    ]

    for args in list_of_args:
        sbatch_wrapper(
            args=args, directory=directory,
        )
