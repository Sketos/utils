import os
import sys


def helper(arg, list_of_args):

    if arg in list_of_args:
        _arg = arg
    else:
        raise ValueError(
            "The {} is not supported".format(arg)
        )

    return _arg


# NOTE: ...
if len(sys.argv) != 4:
    raise ValueError(
        "The script s expecting 3 arguments to be passed, {} were given".format(
            len(sys.argv) - 1
        )
    )

arg1 = helper(
    arg=sys.argv[1],
    list_of_args=[
        "5.8",
        "5.9",
        "5.10"
    ]
)

arg2 = helper(
    arg=sys.argv[2],
    list_of_args=[
        "120s",
        "10800s"
    ]
)

arg3 = helper(
    arg=sys.argv[3],
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

# NOTE:
directory = "/cosma/home/durham/dc-amvr1/simulations/"

# NOTE:
out = "{}/output__{}__{}__{}__%A.out".format(
    directory, arg1, arg2, arg3
)
err = "{}/output__{}__{}__{}__%A.err".format(
    directory, arg1, arg2, arg3
)

sbatch_filename = "sbatch_cosma7_for_wrapper"
if not os.path.isfile(sbatch_filename):
    raise IOError(
        "The sbatch script {} does not exist".format(sbatch_filename)
    )

command = "sbatch --export=ALL,arg1={},arg2={},arg3={} --output={} --error={} {}".format(
    arg1,
    arg2,
    arg3,
    out,
    err,
    sbatch_filename
)
os.system(command)
