import os
import sys
import numpy as np

from astropy.io import fits

sys.path.append(
    "{}/utils".format(os.environ["GitHub"])
)
import directory_utils as directory_utils


def load_list_of_arrays(directory, widths, spws, contsub, array_name):

    if isinstance(spws, list):
        if isinstance(widths, list):
            if len(widths) != len(spws):
                raise ValueError("...")
        elif isinstance(widths, np.int):
            widths = [widths
                for i in range(len(spws))
            ]
        else:
            raise ValueError("...")
    else:
        raise ValueError(
            "must be a list"
        )

    list_of_arrays = []

    for width, spw in zip(widths, spws):

        filename = "{}/{}".format(
            "{}/width_{}".format(
                directory,
                width
            ),
            "{}_spw_{}{}.fits".format(
                array_name,
                spw,
                ".contsub" if contsub is True else ""
            )
        )
        if not os.path.isfile(filename):
            raise IOError(
                "The file {} does not exist".format(filename)
            )

        array = fits.getdata(
            filename=filename
        )
        print(
            "The shape of the {} array is: {}".format(
                array_name, array.shape
            )
        )
        list_of_arrays.append(array)

    return list_of_arrays


def load_uv_wavelengths(directory, widths, spws, contsub, array_name="uv_wavelengths"):

    return load_list_of_arrays(directory, widths, spws, contsub, array_name)


def load_visibilities(directory, widths, spws, contsub, array_name="visibilities"):

    return load_list_of_arrays(directory, widths, spws, contsub, array_name)


# def update_phase_folders(phase_folders, contsub, spws):
#
#     if contsub:
#         phase_folders.append("contsub")
#
#     phase_folders.append(
#         "spws_{}".format('_'.join(spws))
#     )
#
#     return phase_folders

# def load_data(spws, contsub):
#     pass
#
# def get_alma_data_directory(alma_dataset_dirrectory, name, id):
#
#     directory = directory_utils.directory_update_with_folder_names(
#         directory=alma_dataset_dirrectory,
#         folder_names=[name, id]
#     )

# names = [
#     "visibilities",
#     "uv_wavelengths",
#     "sigma"
# ]
#
# data = {}
# for name in names:
#     #data[name] = np.empty((0, 2))
#     data[name] = {}

# class Data:
#
#     def __init__(self):
#         pass


# print(directory);exit()
#
#     # if contsub:
#     #     phase_folders.append("contsub")
#     #
#     # phase_folders.append(
#     #     "spws_{}".format('_'.join(spws))
#     # )
#
#
#
#     # for spw in spws:
#     #     for i, name in enumerate(names):
#     #         array_temp = fits.getdata(
#     #             filename="{}/{}".format(
#     #                 directory,
#     #                 "{}_spw_{}{}.fits".format(
#     #                     name,
#     #                     spw,
#     #                     ".contsub" if contsub else ''
#     #                 )
#     #             )
#     #         )
#     #         data[name]["spw_{}".format(spw)]=array_temp
#     #         #print(array_temp.shape)
#     #
#     # #         data[name] = np.concatenate(
#     # #             [data[name], array_temp],
#     # #             axis=0
#     # #         )
#     # #
#     # print(data["visibilities"].keys())
#
#     def load(directory, spws, contsub, name):
#         pass
#
#         list_of_arrays = []
#         for spw in spws:
#             list_of_arrays.append(
#                 fits.getdata(
#                     filename="{}/{}".format(
#                         directory,
#                         "{}_spw_{}{}.fits".format(
#                             name,
#                             spw,
#                             ".contsub" if contsub else ''
#                         )
#                     )
#                 )
#             )
#
#         return list_of_arrays
#
#     def load_uv_wavelengths(directory, spws, contsub, name="uv_wavelengths"):
#
#         return load(directory, spws, contsub, name)
#
#
#     list_of_arrays = load_uv_wavelengths(
#         directory=directory,
#         spws=spws,
#         contsub=contsub
#     )


if __name__ == "__main__":


    if os.environ["HOME"] == "/Users/ccbh87":
        COSMA_HOME = os.environ["COSMA_HOME_local"]
        COSMA_DATA = os.environ["COSMA7_DATA_local"]
    elif os.environ["HOME"] == "/cosma/home/durham/dc-amvr1":
        COSMA_HOME = os.environ["COSMA_HOME_host"]
        COSMA_DATA = os.environ["COSMA7_DATA_host"]
    else:
        raise ValueError("...")

    workspace_HOME_directory = "{}/workspace".format(COSMA_HOME)
    workspace_DATA_directory = "{}/workspace".format(COSMA_DATA)

    directory = directory_utils.directory_update_with_folder_names(
        directory="{}/{}".format(
            workspace_DATA_directory,
            "alma_datasets"
        ),
        folder_names=["HATLAS_J091043-000322", "2015.1.01362.S"]
    )

    width = 8

    uv_wavelengths = load_uv_wavelengths(
        directory="{}/width_{}".format(
            directory,
            width
        ),
        spws=["0"],
        contsub=False,
        array_name="uv_wavelengths"
    )

    print(np.shape(uv_wavelengths))
