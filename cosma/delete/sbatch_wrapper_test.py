import os
import sys

sbatch_filename = "sbatch_cosma7"
#sbatch_filename = "sbatch_cosma7_for_wrapper"

# arg1 = "arg1"
# arg2 = "arg2"
# arg3 = "arg3"

if len(sys.argv) != 4:
    raise ValueError(
        "The script is expecting 3 arguments to be passed, {} were given".format(
            len(sys.argv) - 1
        )
    )

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]

command = "sbatch --export=ALL,arg1={},arg2={},arg3={} {}".format(
    arg1,
    arg2,
    arg3,
    sbatch_filename
)
os.system(command)
