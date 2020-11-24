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
    if len(args) != 5:
        raise ValueError(
            "The script s expecting 3 arguments to be passed, {} were given".format(
                len(args) - 1
            )
        )
    else:

        arg0 = helper(
            arg=args[0], list_of_args=["5.8", "5.9", "5.10"]
        )

        arg1 = helper(
            arg=args[1], list_of_args=["10800s"]
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
            list_of_args=["None", "1e8", "1e9", "1e10",]
        )

        arg4 = helper(
            arg=args[4], list_of_args=["T", "F"]
        )


        # NOTE:
        out = "{}/output__{}__{}__{}__{}{}%A.out".format(
            directory, arg0, arg1, arg2, arg3, "__" if arg4 == "F" else "_averaged_"
        )
        err = "{}/output__{}__{}__{}__{}{}%A.err".format(
            directory, arg0, arg1, arg2, arg3, "__" if arg4 == "F" else "_averaged_"
        )

        #print(out, err);exit()

        sbatch_filename = "sbatch_for_wrapper_runner_single_dataset"
        if not os.path.isfile(sbatch_filename):
            raise IOError(
                "The sbatch script {} does not exist".format(sbatch_filename)
            )

        command = "sbatch --export=ALL,arg0={},arg1={},arg2={},arg3={},arg4={} --output={} --error={} {}".format(
            arg0,
            arg1,
            arg2,
            arg3,
            arg4,
            out,
            err,
            sbatch_filename
        )
        #print(command)
        os.system(command)


if __name__ == "__main__":

    directory = "{}/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/".format(
        os.environ["COSMA_HOME_host"]
    )


    # NOTE: I can have this script take an input "T" or "F" to run the averaged of not datasets...

    # list_of_args = [
    #     ["5.8", "10800s", "model_1", "None", "T"],
    #     ["5.8", "10800s", "model_1", "1e8", "T"],
    #     ["5.8", "10800s", "model_1", "1e9", "T"],
    #     ["5.8", "10800s", "model_1", "1e10", "T"],
    #     ["5.9", "10800s", "model_1", "None", "T"],
    #     ["5.9", "10800s", "model_1", "1e8", "T"],
    #     ["5.9", "10800s", "model_1", "1e9", "T"],
    #     ["5.9", "10800s", "model_1", "1e10", "T"],
    #     ["5.10", "10800s", "model_1", "None", "T"],
    #     ["5.10", "10800s", "model_1", "1e8", "T"],
    #     ["5.10", "10800s", "model_1", "1e9", "T"],
    #     ["5.10", "10800s", "model_1", "1e10", "T"],
    # ]

    # list_of_args = [
    #     ["5.8", "10800s", "model_1", "None", "F"],
    #     ["5.8", "10800s", "model_1", "1e8", "F"],
    #     ["5.8", "10800s", "model_1", "1e9", "F"],
    #     ["5.8", "10800s", "model_1", "1e10", "F"],
    #     ["5.9", "10800s", "model_1", "None", "F"],
    #     ["5.9", "10800s", "model_1", "1e8", "F"],
    #     ["5.9", "10800s", "model_1", "1e9", "F"],
    #     ["5.9", "10800s", "model_1", "1e10", "F"],
    #     ["5.10", "10800s", "model_1", "None", "F"],
    #     ["5.10", "10800s", "model_1", "1e8", "F"],
    #     ["5.10", "10800s", "model_1", "1e9", "F"],
    #     ["5.10", "10800s", "model_1", "1e10", "F"],
    # ]

    list_of_args = [
        ["5.8", "10800s", "model_2", "None", "T"],
        ["5.8", "10800s", "model_2", "1e8", "T"],
        ["5.8", "10800s", "model_2", "1e9", "T"],
        ["5.8", "10800s", "model_2", "1e10", "T"],
        ["5.9", "10800s", "model_2", "None", "T"],
        ["5.9", "10800s", "model_2", "1e8", "T"],
        ["5.9", "10800s", "model_2", "1e9", "T"],
        ["5.9", "10800s", "model_2", "1e10", "T"],
        ["5.10", "10800s", "model_2", "None", "T"],
        ["5.10", "10800s", "model_2", "1e8", "T"],
        ["5.10", "10800s", "model_2", "1e9", "T"],
        ["5.10", "10800s", "model_2", "1e10", "T"],
        ["5.8", "10800s", "model_3", "None", "T"],
        ["5.8", "10800s", "model_3", "1e8", "T"],
        ["5.8", "10800s", "model_3", "1e9", "T"],
        ["5.8", "10800s", "model_3", "1e10", "T"],
        ["5.9", "10800s", "model_3", "None", "T"],
        ["5.9", "10800s", "model_3", "1e8", "T"],
        ["5.9", "10800s", "model_3", "1e9", "T"],
        ["5.9", "10800s", "model_3", "1e10", "T"],
        ["5.10", "10800s", "model_3", "None", "T"],
        ["5.10", "10800s", "model_3", "1e8", "T"],
        ["5.10", "10800s", "model_3", "1e9", "T"],
        ["5.10", "10800s", "model_3", "1e10", "T"],
        ["5.8", "10800s", "model_4", "None", "T"],
        ["5.8", "10800s", "model_4", "1e8", "T"],
        ["5.8", "10800s", "model_4", "1e9", "T"],
        ["5.8", "10800s", "model_4", "1e10", "T"],
        ["5.9", "10800s", "model_4", "None", "T"],
        ["5.9", "10800s", "model_4", "1e8", "T"],
        ["5.9", "10800s", "model_4", "1e9", "T"],
        ["5.9", "10800s", "model_4", "1e10", "T"],
        ["5.10", "10800s", "model_4", "None", "T"],
        ["5.10", "10800s", "model_4", "1e8", "T"],
        ["5.10", "10800s", "model_4", "1e9", "T"],
        ["5.10", "10800s", "model_4", "1e10", "T"],
        ["5.8", "10800s", "model_5", "None", "T"],
        ["5.8", "10800s", "model_5", "1e8", "T"],
        ["5.8", "10800s", "model_5", "1e9", "T"],
        ["5.8", "10800s", "model_5", "1e10", "T"],
        ["5.9", "10800s", "model_5", "None", "T"],
        ["5.9", "10800s", "model_5", "1e8", "T"],
        ["5.9", "10800s", "model_5", "1e9", "T"],
        ["5.9", "10800s", "model_5", "1e10", "T"],
        ["5.10", "10800s", "model_5", "None", "T"],
        ["5.10", "10800s", "model_5", "1e8", "T"],
        ["5.10", "10800s", "model_5", "1e9", "T"],
        ["5.10", "10800s", "model_5", "1e10", "T"],
    ]

    for args in list_of_args:
        sbatch_wrapper(
            args=args, directory=directory,
        )
