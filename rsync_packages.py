import os

def func(autolens_version, packages):
    pass

packages = ["pip", "pip-9.0.3.dist-info", "setuptools", "setuptools-39.0.1.dist-info", "pkg_resources", "__pycache__"]

autolens_version = "0.46.2"

directory_i = "/cosma/home/dp004/dc-nigh1/PyAutoLens/lib/python3.6/site-packages"

command = "rsync --update -avr {} {}* {}".format(
    " ".join(['''--exclude="{}"'''.format(package)
        for package in packages]
    ),
    "{}/*".format(directory_i),
    "./autolens_{}/lib/python3.6/site-packages/".format(
        autolens_version
    )
)
os.system(command)


# module load python/3.6.5
# module load multinest/oct2018
# export PYTHONPATH=$HOME/autolens_envs_from_James/autolens_0.46.2
# export WORKSPACE=$HOME/autolens_envs_from_James/autolens_0.46.2/workspace
# export SYMDIR="/cosma7/data/dp004/dc-amvr1/autolens/.autolens"
