import os

import cosma_utils as cosma_utils
import directory_utils as directory_utils
import string_utils as string_utils

# NOTE: Useful command for donlwoadinng results from cosma and excluting certain pipelines / folder, for example if you only want the results of a 'pipeline_mass' but not a 'pipeline_source' (for faster DL times and reduced hard disc use.
#rsync --update -v -r --exclude='pipeline_source*' dc-nigh1@login7.cosma.dur.ac.uk:/cosma7/data/dp004/dc-ethe1/output/slacs_models_noise_full_1 .

# export COSMA_HOME_local=$HOME/Desktop/COSMA/cosma/home/durham/dc-amvr1
# export COSMA_HOME_host=/cosma/home/durham/dc-amvr1
# export COSMA7_DATA_local=$HOME/Desktop/COSMA/cosma7/data/dp004/dc-amvr1
# export COSMA7_DATA_host=/cosma7/data/dp004/dc-amvr1

hosts = {
    "COSMA":"dc-amvr1@login.cosma.dur.ac.uk",
    "COSMA5":"dc-amvr1@login5.cosma.dur.ac.uk",
    "COSMA5a":"dc-amvr1@login5a.cosma.dur.ac.uk",
    "COSMA5b":"dc-amvr1@login5b.cosma.dur.ac.uk",
    "COSMA6":"dc-amvr1@login6.cosma.dur.ac.uk",
    "COSMA7":"dc-amvr1@login7.cosma.dur.ac.uk",
    "COSMA7a":"dc-amvr1@login7a.cosma.dur.ac.uk",
    "COSMA7b":"dc-amvr1@login7b.cosma.dur.ac.uk"
}



def rsync_local_to_host(
    path_to_file_local,
    path_to_file_host,
    host="COSMA7",
    update=True
):

    if update:
        os.system(
            "rsync --update -v -r {} {}:{}".format(
                path_to_file_local,
                hosts[host],
                path_to_file_host
            )
        )
    else:
        os.system(
            "rsync -v -r {} {}:{}".format(
                path_to_file_local,
                hosts[host],
                path_to_file_host
            )
        )

def rsync_host_to_local(
    path_to_file_host,
    path_to_file_local,
    host="COSMA7a",
    update=True
):
    if update:
        os.system(
            "rsync --update -v -r {}:{} {}".format(
                hosts[host],
                path_to_file_host,
                path_to_file_local,
            )
        )
    else:
        os.system(
            "rsync -v -r {}:{} {}".format(
                hosts[host],
                path_to_file_host,
                path_to_file_local,
            )
        )






def rsync_from_HOME_workspace(path_to_file):

    path_to_file_local = "{}/workspace/{}".format(
        os.environ["COSMA_HOME_local"],
        path_to_file
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    path_to_file_host = "{}/workspace/{}".format(
        os.environ["COSMA_HOME_host"],
        path_to_file
    )

    return path_to_file_local, path_to_file_host


def rsync_from_DATA_workspace(path_to_file="", cosma_server="7"):

    path_to_file_local = "{}/workspace/{}".format(
        os.environ["COSMA{}_DATA_local".format(cosma_server)],
        path_to_file
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    path_to_file_host = "{}/workspace/{}".format(
        os.environ["COSMA{}_DATA_host".format(cosma_server)],
        path_to_file
    )

    return path_to_file_local, path_to_file_host


def rsync_alma_datasets(source_name, source_alma_id, width=None, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_from_DATA_workspace(
        path_to_file="alma_datasets",
        cosma_server=cosma_server
    )

    path_to_file_local = "{}/{}/{}".format(
        path_to_file_local,
        source_name,
        source_alma_id
    )
    if not os.path.isdir(path_to_file_local):
        raise IOError(
            "The directory {} does not exist".format(path_to_file_local)
        )

    path_to_file_host = "{}/{}/{}".format(
        path_to_file_host,
        source_name,
        source_alma_id
    )

    if width is not None:
        path_to_file_local = "{}/width_{}".format(
            path_to_file_local,
            width
        )
        if not os.path.isdir(path_to_file_local):
            raise IOError(
                "The directory {} does not exist".format(path_to_file_local)
            )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )


def rsync_workspace_scripts(path_to_file):

    path_to_file_local = "{}/workspace/{}".format(
        os.environ["COSMA_HOME_local"],
        path_to_file
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    path_to_file_host = "{}/workspace/{}".format(
        os.environ["COSMA_HOME_host"],
        path_to_file
    )

    return path_to_file_local, path_to_file_host


def rsync_runners_from_workspace_scripts(filename, host="COSMA7", update=True):

    path_to_file_local, path_to_file_host = rsync_workspace_scripts(
        path_to_file="runners/interferometer/"
    )
    if not os.path.isdir(path_to_file_local):
        raise IOError(
            "{} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local="{}/{}".format(
            directory_utils.sanitize_directory(path_to_file_local),
            filename
        ),
        path_to_file_host=path_to_file_host,
        host=host,
        update=update
    )


def rsync_config(version, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_from_DATA_workspace(
        cosma_server=cosma_server
    )

    path_to_file_local = "{}/config_{}".format(
        path_to_file_local,
        version
    )
    if not os.path.isdir(path_to_file_local):
        raise IOError(
            "The directory {} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )





# def rsync_github_scripts(path_to_file):
#
#     path_to_file_local = "{}/{}".format(
#         os.environ["GitHub"],
#         path_to_file
#     )
#     if not os.path.isdir(path_to_file_local):
#         print(
#             "{} does not exist".format(path_to_file_local)
#         )
#
#     path_to_file_host = "{}/GitHub/{}".format(
#         os.environ["COSMA_HOME_host"],
#         path_to_file
#     )
#
#     return path_to_file_local, path_to_file_host
#
#
# def rsync_github_scripts_from_autolens_workspace(filename, host="COSMA7", update=True):
#
#     path_to_file_local, path_to_file_host = rsync_github_scripts(
#         path_to_file="autolens_workspace/"
#     )
#     if not os.path.isdir(path_to_file_local):
#         raise IOError(
#             "{} does not exist".format(path_to_file_local)
#         )
#
#     rsync_local_to_host(
#         path_to_file_local="{}/{}*".format(
#             directory_utils.sanitize_directory(path_to_file_local),
#             filename
#         ),
#         path_to_file_host=path_to_file_host,
#         host=host,
#         update=update
#     )





def rsync_scripts_from_github_directory(directory):

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(
            directory=os.environ["GitHub"]
        ),
        directory
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    path_to_file_host = "{}/GitHub/{}".format(
        directory_utils.sanitize_directory(
            directory=os.environ["COSMA_HOME_host"]
        ),
        directory
    )

    return path_to_file_local, path_to_file_host


def rsync_scripts_from_github_directory__utils(script_filename, host="COSMA7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_github_directory(
        directory="utils"
    )

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(directory=path_to_file_local),
        script_filename
    )
    if not os.path.isfile(path_to_file_local):
        raise IOError(
            "The file {} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host=host,
        update=update
    )


def rsync_scripts_from_github_directory__autolens_utils(script_filename, host="COSMA7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_github_directory(
        directory="utils/autolens_utils"
    )

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(directory=path_to_file_local),
        script_filename
    )
    if not os.path.isfile(path_to_file_local):
        raise IOError(
            "The file {} does not exist".format(path_to_file_local)
        )

    # print(
    #     "path_to_file_local = {}".format(path_to_file_local)
    # )
    # print(
    #     "path_to_file_host = {}".format(path_to_file_host)
    # )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host=host,
        update=update
    )


def rsync_scripts_from_github_directory__interferometry_utils(script_filename, host="COSMA7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_github_directory(
        directory="utils/interferometry_utils"
    )

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(directory=path_to_file_local),
        script_filename
    )
    if not os.path.isfile(path_to_file_local):
        raise IOError(
            "The file {} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host=host,
        update=update
    )


def rsync_scripts_from_github_directory__autofit_utils(script_filename, host="COSMA7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_github_directory(
        directory="utils/autofit_utils"
    )

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(directory=path_to_file_local),
        script_filename
    )
    if not os.path.isfile(path_to_file_local):
        raise IOError(
            "The file {} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host=host,
        update=update
    )



def rsync_runners(filename, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_from_HOME_workspace(
        path_to_file="runners/interferometer"
    )

    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    print(path_to_file_local, path_to_file_host)

    # rsync_local_to_host(
    #     path_to_file_local=path_to_file_local,
    #     path_to_file_host=path_to_file_host,
    #     host="COSMA{}".format(
    #         cosma_server
    #     ),
    #     update=update
    # )

def rsync_source_runner(source_name, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_from_HOME_workspace(
        path_to_file="runners/interferometer"
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(directory=path_to_file_local),
        source_name
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )


def rsync_scripts_from_directory_on_github(directory):

    path_to_file_local = "{}/{}".format(
        directory_utils.sanitize_directory(
            directory=os.environ["GitHub"]
        ),
        directory
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    path_to_file_host = "{}/GitHub/{}".format(
        directory_utils.sanitize_directory(
            directory=os.environ["COSMA_HOME_host"]
        ),
        directory
    )

    return path_to_file_local, path_to_file_host


def rsync_pipelines_from_autolens_workspace_on_github(autolens_version, pipeline_type, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_directory_on_github(
        directory="autolens_workspace/pipelines/{}/interferometer".format(
            autolens_version,
        )
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    if pipeline_type in [
        "source",
        "mass"
    ]:
        path_to_file_local = "{}/{}".format(
            directory_utils.sanitize_directory(directory=path_to_file_local),
            pipeline_type
        )
        if not os.path.isdir(path_to_file_local):
            print(
                "{} does not exist".format(path_to_file_local)
            )
    else:
        raise ValueError(
            "{} is not supported".format(pipeline_type)
        )

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )



def rsync_python_packages_from_github(package_name, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_directory_on_github(
        directory="/packages/python"
    )

    path_to_file_local = "{}/{}".format(
        path_to_file_local, package_name
    )
    if not os.path.isdir(path_to_file_local):
        print(
            "{} does not exist".format(path_to_file_local)
        )

    rsync_local_to_host(
        path_to_file_local="{}*".format(path_to_file_local),
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )


def rsync_packages_from_venv(autolens_version, package, update=False):

    if package not in [
        "autolens",
        "autogalaxy",
        "autoarray",
    ]:
        raise ValueError("...")

    path_to_file_local = "/opt/anaconda3/envs/autolens_{}/".format(
        autolens_version
    )
    if not os.path.isdir(path_to_file_local):
        raise IOError("The directory {} does not exist")
    else:
        path_to_file_local = "{}/lib/python3.7/site-packages/{}".format(
            path_to_file_local,
            package
        )
        if not os.path.isdir(path_to_file_local):
            raise IOError("The directory {} does not exist")

    path_to_file_host = "{}/autolens_envs/autolens_{}_modified/lib/python3.6/site-packages".format(
        os.environ["COSMA_HOME_host"],
        autolens_version
    )

    rsync_local_to_host(
        path_to_file_local="{}/*".format(
            directory_utils.sanitize_directory(
                directory=path_to_file_local
            )
        ),
        path_to_file_host="{}/{}".format(
            directory_utils.sanitize_directory(
                directory=path_to_file_host
            ),
            package
        ),
        host="COSMA7",
        update=update
    )


def rsync_autofit_tutorials(n, version=None, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_github_directory(
        directory="tutorials/autofit/tutorial_{}".format(n)
    )

    # # NOTE: This has been added.
    # path_to_file_host = string_utils.remove_substring_from_end_of_string(
    #     string=path_to_file_host,
    #     substring="tutorial_{}".format(n)
    # )

    # path_to_file_local="{}/config_0.45.0/".format(
    #     path_to_file_local,
    # )

    print(path_to_file_local, path_to_file_host)
    exit()

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )

def rsync_filename_autofit_tutorials(n, filename, version=None, cosma_server="7", update=True):

    path_to_file_local, path_to_file_host = rsync_scripts_from_github_directory(
        directory="tutorials/autofit/tutorial_{}".format(n)
    )

    path_to_file_local = "{}/{}".format(
        path_to_file_local,
        filename
    )

    if os.path.isfile(path_to_file_local):
        pass
    elif os.path.isdir(path_to_file_local):
        pass
    else:
        raise IOError(
            "The file {} does not exist".format(path_to_file_local)
        )

    # print(path_to_file_local, path_to_file_host)
    # exit()

    rsync_local_to_host(
        path_to_file_local=path_to_file_local,
        path_to_file_host=path_to_file_host,
        host="COSMA{}".format(
            cosma_server
        ),
        update=update
    )


if __name__ == "__main__":
    pass

    #rsync_autofit_tutorials(n=0)

    # # n = 0
    # #filename = "runner_utils.py"
    # #filename = "runner_with_selfcal__lens__sie__source__ellipticalsersic__data__len__sie__source__ellipticalsersic__phase_errors.py"
    # #filename = "runner_with_selfcal__lens__sie__source__ellipticalsersic__data__len__sie_and_subhalo__source__ellipticalsersic__phase_errors.py"
    # filename = "runner_with_selfcal__lens_and_subhalo__sie__source__ellipticalsersic__data__len__sie_and_subhalo__source__ellipticalsersic__phase_errors.py"
    # #filename = "src"
    #
    # rsync_filename_autofit_tutorials(
    #     n=0,
    #     filename=filename
    # )

    # filename = "NUFFT_test.py"
    # rsync_filename_autofit_tutorials(
    #     n=3,
    #     filename=filename
    # )

    #exit()
    #rsync_filename_autofit_tutorials(n=6, filename="runner__lens__powerlaw__source__kinematics__data__lens__powerlaw__source__kinematics.py")

    #rsync_config(version="0.45.0")

    # package = "autolens"
    # #package = "autoarray"
    # rsync_packages_from_venv(autolens_version="0.45.0", package=package)

    # PIPELINES - SOURCE - INVERSION - FROM_PARAMETRIC
    # pipeline = "lens_instance__source_inversion.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/inversion/{}".format(pipeline),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/inversion",
    #     host="COSMA7",
    #     update=True
    # )

    # # PIPELINES - SOURCE - INVERSION - FROM_PARAMETRIC
    # pipeline = "lens_sie_x2__source_inversion.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/inversion/from_parametric/{}".format(pipeline),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/inversion/from_parametric",
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Downloads/casa-release-4.7.0-el7.tar",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/casa",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/simobserve",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub",
    #     host="COSMA7",
    #     update=True
    # )

    # # # NOTE: SPT-0418 & SPT-0532
    #
    # source = "SPT-0418"
    # #source = "SPT-0532"
    #
    # #filename = "runner_with_fixvis.py"
    # filename = "runner_from.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/{}".format(
    #         source,
    #         filename
    #     ),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}".format(
    #         source
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/SPT-0532/runner_with_fixvis.py",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/SPT-0532",
    #     host="COSMA7",
    #     update=True
    # )





    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/calibrated/numpy_to_fits.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/calibrated",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/calibrated/uid___A002_Xbab09c_Xcb6_spw_0_frequencies.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/calibrated/",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/imaging/imaging.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/imaging",
    #     host="COSMA7",
    #     update=True
    # )

    # #filename = "ALESS41_spw_2.clean.cube.image.pbcor.fits"
    # #filename = "ALESS41_spw_2.clean.cube.image.pbcor.reframe.image.pbcor.fits"
    # #filename = "ALESS41_spw_2.clean.cube.image.pbcor.mom_2.fits"
    #
    # #filename = "ALESS49_spw_1.clean.cube.image.pbcor.fits"
    # filename = "ALESS49_spw_1.clean.cube.image.pbcor.reframe.image.pbcor.mom_0.fits"
    #
    # #filename = "ALESS75_spw_2.clean.cube.image.pbcor.fits"
    # #filename = "ALESS75_spw_2.clean.cube.image.pbcor.reframe.image.pbcor.fits"
    # #filename = "ALESS75_spw_2.clean.cube.image.pbcor.reframe.image.pbcor.mom_0.fits"
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/imaging/{}".format(filename),
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/imaging",
    #     host="COSMA7",
    #     update=True
    # )

    # filename = "member.uid___A001_X87a_Xa7.ALESS71_COJ4-3.clean.image.pbcor.fits"
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/product/{}".format(filename),
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/product",
    #     host="COSMA7",
    #     update=True
    # )



    # autolens_version = "0.45.0"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/autolens_workspace/pipelines/{}/interferometer/source/parametric/lens_instance__source_parametric.py".format(
    #         autolens_version
    #     ),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/autolens_workspace/pipelines/{}/interferometer/source/parametric/".format(
    #         autolens_version
    #     ),
    #     host="COSMA7",
    #     update=True
    # )


    # # #ticket_id =
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/utils/alma_tickets/downloadRequest1653716962820.sh",
    #     path_to_file_host="{}/{}".format(
    #         os.environ["COSMA7_DATA_host"],
    #         "ALMA_archive_data"
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # # filename = "ms.py"
    # filename = "numpy_to_fits.py"
    # # #filename = "fixvis.py"
    # # #filename = "skycoords.txt"
    # # rsync_local_to_host(
    # #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/{}".format(
    # #         filename
    # #     ),
    # #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5",
    # #     host="COSMA7",
    # #     update=True
    # # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2d/calibrated_5.1.1-5/{}".format(
    #         filename
    #     ),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X2b/group.uid___A001_X894_X2c/member.uid___A001_X894_X2d/calibrated_5.1.1-5",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/calibrated_5.1.1-5/{}".format(
    #         filename
    #     ),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/calibrated_5.1.1-5",
    #     host="COSMA7",
    #     update=True
    # )



    # filename = "ms.py"
    # #filename = "numpy_to_fits.py"
    # #filename = "fixvis.py"
    # #filename = "skycoords.txt"
    #
    # tree = "2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/{}/calibrated/{}".format(
    #         tree,
    #         filename
    #     ),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/{}/calibrated".format(
    #         tree
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # # casa
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/utils/casa/extract_info.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/calibrated/",
    #     host="COSMA7",
    #     update=True
    # )


    # 2016.1.01374.S
    #
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/uid___A002_Xc6ff69_X274a_field_SPT-0532.ms.split.cal.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging/ALESS71_spw_0.clean.cube.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging/imaging.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xa5/group.uid___A001_X87a_Xa6/member.uid___A001_X87a_Xa7/imaging/",
    #     host="COSMA7",
    #     update=True
    # )


    # field = "ALESS41"
    # #field = "ALESS49"
    # #field = "ALESS75"
    # #uid = "uid___A002_Xbadc30_X1bc1"
    # #uid = "uid___A002_Xbadc30_X1fd8"
    # #uid = "uid___A002_Xbae7da_X3df"
    # #uid = "uid___A002_Xbae7da_X10f"
    # #uid = "uid___A002_Xbaedce_X1a8f"
    # #uid = "uid___A002_Xbaedce_X169a"
    # uid = "uid___A002_Xbaedce_Xe8c"
    # width = 1
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/calibrated/width_{}/{}/*.fits".format(
    #         width,
    #         "{}_field_{}".format(uid, field)
    #     ),
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/calibrated/width_{}/{}".format(
    #         width,
    #         "{}_field_{}".format(uid, field)
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # #ms = "uid___A002_Xc46ab2_X21ee_field_SPT-0532"
    # #ms = "uid___A002_Xc483da_X2e83_field_SPT-0532"
    # ms = "uid___A002_Xc6ff69_X274a_field_SPT-0532"
    # #ms = "uid___A002_Xc6ff69_X274a_field_J0531-4827"
    #
    # #type = "uv_wavelengths"
    # #type = "uv_wavelengths_fixvis"
    # #type = "visibilities"
    # #type = "visibilities_fixvis"
    # type = "sigma"
    # #type = "sigma_fixvis"
    #
    # width = 128
    # spw = 23
    #
    # # width = 480
    # # spw = 25
    #
    #
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/width_{}/{}/{}_spw_{}.fits".format(
    #         width,
    #         ms,
    #         type,
    #         spw
    #     ),
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/width_{}/{}/".format(
    #         width,
    #         ms
    #     ),
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/uid___A002_Xc6ff69_X274a_field_SPT-0532.ms.split.cal.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/uid___A002_Xc6ff69_X274a.cfg",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/uid___A002_Xc6ff69_X274a_field_J0531-4827.ms.split.cal.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/calibrated/*frequencies.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/calibrated",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/product/member.uid___A001_X87a_Xaf.ALESS41_spw2.clean.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/product",
    #     host="COSMA7",
    #     update=True
    # )

    # 2017.1.00027.S
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/product/member.uid___A001_X1273_X697.G09v1.40_sci.spw0_1_2_3.mfs.I.manual.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/product/",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6b1/group.uid___A001_X1273_X6b2/member.uid___A001_X1273_X6b3/product/member.uid___A001_X1273_X6b3.HELMS-8_sci.spw0_1_2_3.mfs.I.manual.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6b1/group.uid___A001_X1273_X6b2/member.uid___A001_X1273_X6b3/product/",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6a9/group.uid___A001_X1273_X6aa/member.uid___A001_X1273_X6ab/product/member.uid___A001_X1273_X6ab.HELMS-45_sci.spw19_21_23_25.mfs.I.manual.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6a9/group.uid___A001_X1273_X6aa/member.uid___A001_X1273_X6ab/product",
    #     host="COSMA7",
    #     update=True
    # )

    # NOTE: 2018.1.01140.S
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2018.1.01140.S/science_goal.uid___A001_X133d_X3b1d/group.uid___A001_X133d_X3b1e/member.uid___A001_X133d_X3b1f/product/member.uid___A001_X133d_X3b1f._ALESS.65.1__sci.spw23.cube.I.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2018.1.01140.S/science_goal.uid___A001_X133d_X3b1d/group.uid___A001_X133d_X3b1e/member.uid___A001_X133d_X3b1f/product",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2018.1.01140.S//science_goal.uid___A001_X133d_X3b16/group.uid___A001_X133d_X3b17/member.uid___A001_X133d_X3b18/product/member.uid___A001_X133d_X3b18._ALESS.65.1__sci.spw9_11_15_17.cont.I.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2018.1.01140.S//science_goal.uid___A001_X133d_X3b16/group.uid___A001_X133d_X3b17/member.uid___A001_X133d_X3b18/product",
    #     host="COSMA7",
    #     update=True
    # )

    # #source = "SPT-S_J053816-5030.8"
    # source = "SPT-0418"
    # #source = "SPT-0532"
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/workspace/output/{}".format(source),
    #     path_to_file_local=" /Users/ccbh87/Desktop/COSMA/cosma7/data/dp004/dc-amvr1/workspace/output/COSMA",
    #     host="COSMA7",
    #     update=True
    # )

    # # NOTE: tutorial: 0
    # #runner = "runner_with_selfcal__lens__sie__source__ellipticalsersic__data__len__sie__source__ellipticalsersic__phase_errors"
    # #runner = "runner_with_selfcal__lens__sie__source__ellipticalsersic__data__len__sie_and_subhalo__source__ellipticalsersic__phase_errors"
    # runner = "runner_with_selfcal__lens_and_subhalo__sie__source__ellipticalsersic__data__len__sie_and_subhalo__source__ellipticalsersic__phase_errors"
    # # rsync_host_to_local(
    # #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_0/output/{}/data_with_phase_errors/phase_errors_type_stochastic".format(runner),
    # #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0/output/{}/data_with_phase_errors".format(runner),
    # #     host="COSMA7",
    # #     update=True
    # # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_0/output/{}/".format(runner),
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0/output/{}/".format(runner),
    #     host="COSMA7",
    #     update=True
    # )
    # # rsync_host_to_local(
    # #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_0/output/{}/data_with_phase_errors/phase_errors_type_stochastic/model_with_selfcal/evidence_tolerance__100.0/self_calibration_method__least_squares/n_scans_12".format(runner),
    # #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0/output/{}/data_with_phase_errors/phase_errors_type_stochastic/model_with_selfcal/evidence_tolerance__100.0/self_calibration_method__least_squares/".format(runner),
    # #     host="COSMA7",
    # #     update=True
    # # )

    # NOTE: tutorial_0_multiple_datasets

    # NOTE: Scripts in simulations
    # #filename = "generate_phases_from_phase_screen.py"
    # filename = "generate_dataset.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/simulations/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/simulations",
    #     host="COSMA7",
    #     update=True
    # )
    # filename = "model_utils.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/simulations/utils/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/simulations/utils",
    #     host="COSMA7",
    #     update=True
    # )

    # filename = "runner_single_dataset.py"
    # #filename = "runner_single_dataset_temp.py"
    # #filename = "plotter_single_dataset.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/runners/simulations/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/runners/simulations",
    #     host="COSMA7",
    #     update=True
    # )

    # #filename = "sbatch_for_wrapper_runner_single_dataset"
    # filename = "sbatch_wrapper_multi_runner_single_dataset.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/",
    #     host="COSMA7",
    #     update=True
    # )

    # filename = "delete_phase_screens.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/simulations/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/simulations",
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_0_multiple_datasets/output/*",
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/output/COSMA",
    #     host="COSMA7",
    #     update=True
    # )



    # NOTE: rsync the sbatch_wrapper to "/cosma/home/durham/dc-amvr1/simulations/"
    # filename = "sbatch_wrapper_multi_generate_dataset.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/utils/cosma/generate_dataset/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/simulations/",
    #     host="COSMA7",
    #     update=True
    # )

    # # NOTE: rsync the sbatch_wrapper to "/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/"
    # #filename = "sbatch_wrapper_multi_runner_single_dataset.py"
    # filename = "sbatch_for_wrapper_runner_single_dataset"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/utils/cosma/runners/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0_multiple_datasets",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit",
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0_multiple_datasets",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/runners/simulations/runner_single_dataset.py",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_0_multiple_datasets/runners/simulations/",
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00754.S/science_goal.uid___A001_X87a_Xad/group.uid___A001_X87a_Xae/member.uid___A001_X87a_Xaf/calibrated",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6b1/group.uid___A001_X1273_X6b2/member.uid___A001_X1273_X6b3/calibrated/calibrated.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6b1/group.uid___A001_X1273_X6b2/member.uid___A001_X1273_X6b3/calibrated",
    #     host="COSMA7",
    #     update=True
    # )

    # NOTE: 2016.1.00564.S
    # --------------------- #

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/examine.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/imaging.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/imaging",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/imaging_concatenated.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/imaging",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/preprocessing/preprocessing.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/preprocessing",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/concatenated/ALESS031.1.ms.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/concatenated",
    #     host="COSMA7",
    #     update=True
    # )

    # source = "ALESS031.1"
    # directory = "width_100_km_per_s"
    # #filename = "ALESS031.1_spw_1.clean.cube.image.fits"
    # filename = "ALESS031.1_spws_2_and_1.clean.cube.image.pbcor.fits"

    # source = "ALESS022.1"
    # directory = "width_50_km_per_s"
    # #filename = "ALESS031.1_spw_1.clean.cube.image.fits"
    # filename = "ALESS022.1_spw_3.clean.cube.image.pbcor.fits"

    # source = "ALESS009.1"
    # #directory = "width_50_km_per_s"
    # #directory = "width_100_km_per_s"
    # directory = "width_125_km_per_s"
    # #filename = "ALESS031.1_spw_1.clean.cube.image.fits"
    # filename = "ALESS009.1_spws_3_and_1.clean.cube.image.pbcor.fits"
    #
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/imaging/{}/cube/{}/{}".format(
    #         source, directory, filename
    #     ),
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/{}/cube/{}".format(
    #         source, directory
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/science_goal.uid___A001_X879_Xcb/group.uid___A001_X879_Xcc/member.uid___A001_X879_Xcd/product/member.uid___A001_X879_Xcd._ALESS035.1__sci.spw27.cube.I.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xcb/group.uid___A001_X879_Xcc/member.uid___A001_X879_Xcd/product",
    #     host="COSMA7",
    #     update=True
    # )




    # id = "2017.1.01163.S"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/{}/clean.py".format(id),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/{}/".format(id),
    #     host="COSMA7",
    #     update=True
    # )




    # NOTE: Calibrated
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xb7/group.uid___A001_X879_Xb8/member.uid___A001_X879_Xb9/calibrated/calibrated.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/science_goal.uid___A001_X879_Xb7/group.uid___A001_X879_Xb8/member.uid___A001_X879_Xb9/calibrated",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xc3/group.uid___A001_X879_Xc4/member.uid___A001_X879_Xc5/calibrated/calibrated.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/science_goal.uid___A001_X879_Xc3/group.uid___A001_X879_Xc4/member.uid___A001_X879_Xc5/calibrated",
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/science_goal.uid___A001_X879_Xbf/group.uid___A001_X879_Xc0/member.uid___A001_X879_Xc1/product/member.uid___A001_X879_Xc1.ALESS031.1_spw2.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xbf/group.uid___A001_X879_Xc0/member.uid___A001_X879_Xc1/product",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/imaging/ALESS031.1/cube/concatenated/width_100_km_per_s/ALESS031.1.clean.cube.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS031.1/cube/concatenated/width_100_km_per_s",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/imaging/ALESS031.1/cube/width_4/ALESS031.1_spws_2_and_1.clean.cube.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS031.1/cube/width_4",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/imaging/ALESS031.1/cube/width_50_km_per_s/ALESS031.1_spws_2_and_1.clean.cube.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/imaging/ALESS031.1/cube/width_50_km_per_s",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/science_goal.uid___A001_X879_Xc3/group.uid___A001_X879_Xc4/member.uid___A001_X879_Xc5/product/member.uid___A001_X879_Xc5.ALESS031.1_continuum.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xc3/group.uid___A001_X879_Xc4/member.uid___A001_X879_Xc5/product",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00564.S/science_goal.uid___A001_X879_Xc3/group.uid___A001_X879_Xc4/member.uid___A001_X879_Xc5/calibrated/uid___A002_Xbc5a0f_X590.ms.split.cal.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00564.S/science_goal.uid___A001_X879_Xc3/group.uid___A001_X879_Xc4/member.uid___A001_X879_Xc5/calibrated",
    #     host="COSMA7",
    #     update=True
    # )



    # #
    # #filename = "ALESS71.py"
    # #filename = "plotter.py"
    # #filename = "tutorial_3_main.py"
    # #filename = "src"
    # #filename = "ALESS75_updated.py"
    # #filename = "ALESS_112.1.py"
    # filename = "noise.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_3",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/compute_sigma.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01163.S",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/simulations/delete_phase_screens.py",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/simulations",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/SPT-S_J053816-5030/loader.py",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/SPT-S_J053816-5030",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/phase_screens/",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/simobserve/simobserve.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/simulations",
    #     host="COSMA7",
    #     update=True
    # )

    # #source = "ALESS_006.1"
    # #source = "ALESS_017.1"
    # #source = "ALESS_062.2"
    # #source = "ALESS_065.1"
    # #source = "ALESS_066.1"
    # #source = "ALESS_098.1"
    # #source = "ALESS_101.1"
    # #source = "ALESS_112.1"
    # #source = "ALESS41__priors_from_phase_1"
    # #source = "ALESS49__priors_from_phase_1"
    # #source = "ALESS75__priors_from_phase_1"
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_3/output/phase_1__{}".format(source),
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/output/COSMA",
    #     host="COSMA7",
    #     update=True
    # )

    # #filename = "plotter_utils.py"
    # #filename = "utils.py"
    # filename = "plotter.py"
    # #filename = "ALESS49_plotter.py"
    # #filename = "ALESS_006.1_plotter.py"
    # #filename = "ALESS_017.1_plotter.py"
    # #filename = "ALESS_049.1.py"
    # #filename = "ALESS_062.2_plotter.py"
    # #filename = "ALESS_065.1_plotter.py"
    # #filename = "ALESS_066.1_plotter.py"
    # #filename = "ALESS_098.1_plotter.py"
    # #filename = "ALESS_101.1_plotter.py"
    # #filename = "ALESS_112.1_plotter.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_3",
    #     host="COSMA7",
    #     update=True
    # )

    # #source = "ALESS41"
    # #source = "ALESS49"
    # source = "ALESS75"
    # #source = "ALESS_006.1"
    # #source = "ALESS_017.1"
    # #source = "ALESS_062.2"
    # #source = "ALESS_065.1"
    # #source = "ALESS_066.1"
    # #source = "ALESS_098.1"
    # #source = "ALESS_101.1"
    # #source = "ALESS_112.1"
    # rsync_host_to_local(
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_3/metadata/*{}*".format(source),
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata",
    #     host="COSMA7",
    #     update=True
    # )

    # source = "ALESS49"
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_3/output/phase_2__{}__priors_from_phase_1".format(source),
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/output/COSMA",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/tutorials/autofit/tutorial_3/metadata/*.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_3/metadata",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_0/output/runner_with_selfcal__lens_and_subhalo__sie__source__ellipticalsersic__data__len__sie_and_subhalo__source__ellipticalsersic__phase_errors",
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_0/output_cosma",
    #     host="COSMA7",
    #     update=True
    # )



    # # NOTE: Download product files ... 2016.1.01374.S
    #
    # # rsync_host_to_local(
    # #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/product/member.uid___A001_X894_X39._SPT-S_J053816-5030.8__sci.spw21_23_25_27.cont.I.pbcor.fits",
    # #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/product/",
    # #     host="COSMA7",
    # #     update=True
    # # )
    # # rsync_host_to_local(
    # #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X3b/product/uid___A001_X894_X3b._SPT-S_J053816-5030.8__sci.spw21_23_25_27.cont.I.pbcor.fits",
    # #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X3b/product/",
    # #     host="COSMA7",
    # #     update=True
    # # )
    #
    # # science_goal = "uid___A001_X894_X31"
    # # group = "uid___A001_X894_X32"
    # # member = "uid___A001_X894_X33"
    #
    # science_goal = "uid___A001_X894_X37"
    # group = "uid___A001_X894_X38"
    # member = "uid___A001_X894_X39"
    #
    # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc49eba_X38a1_field_SPT-S_J053816-5030.8"
    # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc67b7e_X265e_field_SPT-S_J053816-5030.8"
    # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc68b3e_X1309_field_SPT-S_J053816-5030.8"
    # directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc65717_X2bd2_field_SPT-S_J053816-5030.8"
    #
    # # science_goal = "uid___A001_X894_X2b"
    # # group = "uid___A001_X894_X2c"
    # # member = "uid___A001_X894_X2d"
    # #
    # # directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc46ab2_X1b0a_field_SPT-0418"
    # # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc483da_X2544_field_SPT-0418"
    # # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc483da_X2a29_field_SPT-0418"
    # # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc49eba_X2aaf_field_SPT-0418"
    # # #directory = "calibrated_5.1.1-5/width_128/uid___A002_Xc68b3e_X187a_field_SPT-0418"
    #
    # spw = "23"
    # #filename = "uv_wavelengths_fixvis_spw_{}.fits".format(spw)
    # #filename = "visibilities_fixvis_spw_{}.fits".format(spw)
    # #filename = "sigma_fixvis_spw_{}.fits".format(spw)
    #
    # #filename = "uv_wavelengths_spw_{}.fits".format(spw)
    # #filename = "visibilities_spw_{}.fits".format(spw)
    # filename = "sigma_spw_{}.fits".format(spw)
    #
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.{}/group.{}/member.{}/{}/{}".format(
    #         science_goal,
    #         group,
    #         member,
    #         directory,
    #         filename
    #     ),
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.{}/group.{}/member.{}/{}/".format(
    #         science_goal,
    #         group,
    #         member,
    #         directory
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.{}/group.{}/member.{}/{}/{}".format(
    #         science_goal,
    #         group,
    #         member,
    #         directory,
    #         filename
    #     ),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.{}/group.{}/member.{}/{}/".format(
    #         science_goal,
    #         group,
    #         member,
    #         directory
    #     ),
    #     host="COSMA7",
    #     update=True
    # )


    # # NOTE: 2017.1.01512.S
    #
    # science_goal = "uid___A001_X1284_X1a7a"
    # group = "uid___A001_X1284_X1a7b"
    # member = "uid___A001_X1284_X1a7c"
    #
    # host_to_local = True
    # local_to_host = False
    # directory = "product"
    # filename = "member.uid___A001_X1284_X1a7c._ALESS041.1__sci.spw31.cube.I.pbcor.fits"
    #
    # # host_to_local = False
    # # local_to_host = True
    # # directory = "product"
    # # filename = "examine.py"
    #
    # if host_to_local:
    #     rsync_host_to_local(
    #         path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01512.S/science_goal.{}/group.{}/member.{}/{}/{}".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory,
    #             filename
    #         ),
    #         path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01512.S/science_goal.{}/group.{}/member.{}/{}/".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory
    #         ),
    #         host="COSMA7",
    #         update=True
    #     )
    #
    # if local_to_host:
    #     rsync_local_to_host(
    #         path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01512.S/science_goal.{}/group.{}/member.{}/{}/{}".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory,
    #             filename
    #         ),
    #         path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01512.S/science_goal.{}/group.{}/member.{}/{}/".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory
    #         ),
    #         host="COSMA7",
    #         update=True
    #     )


    # NOTE: 2017.1.01163.S

    # --- #

    # science_goal = "uid___A001_X1288_X123"
    # group = "uid___A001_X1288_X124"
    # member = "uid___A001_X1288_X125"
    #
    # #filename = "member.uid___A001_X1288_X125._ALESS_061.1__sci.spw23.cube.I.pbcor.fits"
    # #filename = "ms.py"
    #
    # # # local_to_host
    # # directory = "imaging"
    # # filename = "imaging.py"
    #
    # # host_to_local
    # host_to_local = True
    # local_to_host = False
    # # directory = "imaging/ALESS_061.1/"
    # # filename = "ALESS_061.1_spw_17.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_065.1/"
    # # filename = "ALESS_065.1_spw_17.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_034.1/"
    # # filename = "ALESS_034.1_spw_23.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_066.1/"
    # # filename = "ALESS_066.1_spw_21.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_062.2/"
    # # filename = "ALESS_062.2_spw_21.clean.cube.image.pbcor.fits"
    # directory = "imaging/ALESS_098.1/"
    # filename = "ALESS_098.1_spw_21.clean.cube.image.pbcor.fits"
    #
    # # #
    # # host_to_local = True
    # # local_to_host = False
    # # directory = "product/"
    # # #filename = "member.uid___A001_X1288_X125._ALESS_062.2__sci.spw21.cube.I.pbcor.fits"
    # # filename = "member.uid___A001_X1288_X125._ALESS_066.1__sci.spw21.cube.I.pbcor.fits"

    # --- #

    # science_goal = "uid___A001_X1288_X127"
    # group = "uid___A001_X1288_X128"
    # member = "uid___A001_X1288_X129"
    #
    # # # local_to_host
    # # directory = "calibrated"
    # # filename = "export_frequencies.py"
    # #
    # # # local_to_host
    # # directory = "imaging"
    # # filename = "imaging.py"
    #
    # # host_to_local
    # host_to_local = True
    # local_to_host = False
    # # directory = "imaging/ALESS_006.1/"
    # # filename = "ALESS_006.1_spw_23.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_017.1/"
    # # filename = "ALESS_017.1_spw_17.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_088.1/"
    # # filename = "ALESS_088.1_spw_23.clean.cube.image.pbcor.fits"
    # # directory = "imaging/ALESS_101.1/"
    # # filename = "ALESS_101.1_spw_23.clean.cube.image.pbcor.fits"
    # directory = "imaging/ALESS_112.1/"
    # filename = "ALESS_112.1_spw_23.clean.cube.image.pbcor.fits"
    #
    # # # host_to_local
    # # host_to_local = True
    # # local_to_host = False
    # # directory = "product"
    # # filename = "member.uid___A001_X1288_X129._ALESS_088.1__sci.spw21.cube.I.pbcor.fits"
    #
    # # # host_to_local
    # # host_to_local = True
    # # local_to_host = False
    # # directory = "calibrated"
    # # filename = "uid___A002_Xc99ad7_X6a09.ms.listobs"

    # --- #

    # science_goal = "uid___A001_X1288_X12b"
    # group = "uid___A001_X1288_X12c"
    # member = "uid___A001_X1288_X12d"
    #
    # filename = "member.uid___A001_X1288_X12d._ALESS_088.1__sci.spw21.cube.I.pbcor.fits"

    # if host_to_local:
    #     rsync_host_to_local(
    #         path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01163.S/science_goal.{}/group.{}/member.{}/{}/{}".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory,
    #             filename
    #         ),
    #         path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.{}/group.{}/member.{}/{}/".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory
    #         ),
    #         host="COSMA7",
    #         update=True
    #     )
    #
    # if local_to_host:
    #     rsync_local_to_host(
    #         path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.{}/group.{}/member.{}/{}/{}".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory,
    #             filename
    #         ),
    #         path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01163.S/science_goal.{}/group.{}/member.{}/{}/".format(
    #             science_goal,
    #             group,
    #             member,
    #             directory
    #         ),
    #         host="COSMA7",
    #         update=True
    #     )





    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/product/",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/product/",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/calibrated/uid___A002_Xc8ed16_X8a0.ms.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.01163.S/science_goal.uid___A001_X1288_X123/group.uid___A001_X1288_X124/member.uid___A001_X1288_X125/calibrated/",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6b1/group.uid___A001_X1273_X6b2/member.uid___A001_X1273_X6b3/calibrated/uid___A002_Xc6c0d5_X1b9.ms.split.cal.listobs",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6b1/group.uid___A001_X1273_X6b2/member.uid___A001_X1273_X6b3/calibrated/",
    #     host="COSMA7",
    #     update=True
    # )

    # PIPELINES
    # ============ #

    # # NOTE: parametric
    # #pipeline = "lens_sie__source_sersic.py"
    # pipeline = "lens_sie_x2__source_sersic.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/parametric/{}".format(pipeline),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/parametric",
    #     host="COSMA7",
    #     update=True
    # )

    # # NOTE: inversion (from_parametric)
    # pipeline = "lens_sie__source_inversion_from_setup.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/inversion/from_parametric/{}".format(pipeline),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/autolens_workspace/pipelines/0.45.0/interferometer/source/inversion/from_parametric",
    #     host="COSMA7",
    #     update=True
    # )

    #rsync_python_packages_from_github(package_name="galpak")

    #rsync_source_runner(source_name="HATLAS_J091043.0-000322")

    #rsync_pipelines_from_autolens_workspace_on_github(autolens_version="0.45.0", pipeline_type="source")


    #rsync_from_DATA_workspace(path_to_file="")
    # rsync_alma_datasets(
    #     source_name="HATLAS_J091043-000322",
    #     source_alma_id="2016.1.00282.S",
    #     width=128
    # )
    #rsync_datasets(source="HATLAS_J091043-000322", proposal_ID="2015.1.01362.S", width=1)


    #rsync_runners_from_workspace_scripts(filename="runner_test.py")
    #rsync_github_scripts_from_autolens_workspace(filename="pipelines")

    # #script_filename = "directory_utils.py"
    # #script_filename = "antenna_utils.py"
    # #script_filename = "phase_screen_utils.py"
    # #script_filename = "emcee_wrapper.py"
    # #script_filename = "directory_utils.py"
    # #script_filename = "string_utils.py"
    # #script_filename = "general_utils.py"
    # #script_filename = "autolens_init_utils.py"
    # #script_filename = "plot_utils.py"
    # #script_filename = "spectral_utils.py"
    # #script_filename = "dictionary_utils.py"
    # #script_filename = "list_utils.py"
    # #script_filename = "getdist_utils.py"
    # #script_filename = "voronoi_utils.py"
    # script_filename = "calibration_utils.py"
    # #script_filename = "calibration_plot_utils.py"
    # #script_filename = "corruption_utils.py"
    # #script_filename = "random_utils.py"
    # #script_filename = "casa_utils.py"
    # #script_filename = "matplotlib_utils.py"
    # #script_filename = "fits_utils.py"
    # #script_filename = "reshape_utils.py"
    #
    # rsync_scripts_from_github_directory__utils(
    #     script_filename=script_filename
    # )

    # script_filename = "autolens_plot_utils.py"
    # #script_filename = "autolens_tracer_utils.py"
    # #script_filename = "autolens_aggregator_utils.py"
    #
    # rsync_scripts_from_github_directory__autolens_utils(
    #     script_filename=script_filename
    # )

    # #script_filename = "autolens_plot_utils.py"
    # #script_filename = "load_utils.py"
    # #script_filename = "interferometry_general_utils.py"
    # #script_filename = "interferometry_noise_utils.py"
    # script_filename = "interferometry_plot_utils.py"
    # #script_filename = "interferometry_reshape_utils.py"
    # #script_filename = "interferometry_averaging_utils.py"
    #
    # rsync_scripts_from_github_directory__interferometry_utils(
    #     script_filename=script_filename
    # )

    # script_filename = "autofit_priors_utils.py"
    #
    # rsync_scripts_from_github_directory__autofit_utils(
    #     script_filename=script_filename
    # )



    # NOTE: Transfer raw ALMA data.

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00282.S/science_goal.uid___A001_X87c_X4cf/group.uid___A001_X87c_X4d0/member.uid___A001_X87c_X4d1/raw/uid___A002_Xbb12f0_X9e0.asdm.sdm",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00282.S/science_goal.uid___A001_X87c_X4cf/group.uid___A001_X87c_X4d0/member.uid___A001_X87c_X4d1/raw",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.00654.S",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/",
    #     host="COSMA7",
    #     update=True
    # )



    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/utils/cosma/*",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/GitHub/utils/cosma",
    #     host="COSMA7",
    #     update=True
    # )

    # 2013.1.00358.S
    # ================== #

    # # NOTE:
    # directory = "science_goal.{}/group.{}/member.{}/calibrated".format(
    #     "uid___A001_X13e_X4b",
    #     "uid___A001_X13e_X4c",
    #     "uid___A001_X13e_X4d"
    # )
    #
    # width = 128
    #
    # uid = "uid___A002_Xa5c7d4_X1ceb"
    # uid = "uid___A002_Xa80456_X16ef"
    #
    # #field = "HELMS-4"
    # field = "HELMS-8"
    # #field = "HELMS-9"
    # #field = "HELMS-45"
    #
    #
    # # directory = "science_goal.{}/group.{}/member.{}/calibrated".format(
    # #     "uid___A001_X13e_X4f",
    # #     "uid___A001_X13e_X50",
    # #     "uid___A001_X13e_X51"
    # # )
    # #
    # # width = 128
    # #
    # # uid = "uid___A002_Xa5df2c_X7a43"
    # #
    # # field = "HELMS-3"
    #
    # rsync_local_to_host(
    #     path_to_file_local="/Volumes/Elements_v1/2013.1.00358.S/{}/width_{}/{}_field_{}/*fits".format(
    #         directory, width, uid, field
    #     ),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2013.1.00358.S/{}/width_{}/{}_field_{}/".format(
    #         directory, width, uid, field
    #     ),
    #     host="COSMA7",
    #     update=True
    # )
    # #exit()


    # #field = "HELMS-3"
    # field = "HELMS-4"
    # #field = "HELMS-8"
    # #field = "HELMS-9"
    # #field = "HELMS-45"
    #
    # #filename = "loader.py"
    # filename = "runner.py"
    # #filename = "fit_plotter.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2013.1.00358.S/{}".format(field, filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2013.1.00358.S".format(field),
    #     host="COSMA7",
    #     update=True
    # )


    # #field = "HELMS-3"
    # #field = "HELMS-9"
    # field = "HELMS-45"
    #
    # #filename = "fit_subplots__phase_1.png"
    # filename = "fit_subplots__phase_2.png"
    #
    # rsync_host_to_local(
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2013.1.00358.S/{}".format(
    #         field, filename
    #     ),
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2013.1.00358.S".format(
    #         field
    #     ),
    #     host="COSMA7",
    #     update=True
    # )


    # 2016.1.01188.S
    # ================== #

    # # directory = "2016.1.01188.S/science_goal.{}/group.{}/member.{}/calibrated/".format(
    # #     "uid___A001_X87d_X53c",
    # #     "uid___A001_X87d_X53d",
    # #     "uid___A001_X87d_X53e"
    # # )
    # # filename = "uid___A002_Xc4f3ae_X1d26.ms.split.cal.listobs"
    #
    # directory = "2016.1.01188.S/science_goal.{}/group.{}/member.{}/calibrated/".format(
    #     "uid___A001_X87d_X544",
    #     "uid___A001_X87d_X545",
    #     "uid___A001_X87d_X546"
    # )
    # #filename = "uid___A002_Xc4d618_X64bc.ms.listobs"
    # filename = "uid___A002_Xc6141c_X3e12.ms.listobs"
    #
    #
    # # rsync_host_to_local(
    # #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/{}/{}".format(
    # #         directory, filename
    # #     ),
    # #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/{}".format(
    # #         directory
    # #     ),
    # #     host="COSMA7",
    # #     update=True
    # # )

    # filename = "calibrated.py"
    #
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/{}/{}".format(
    #         directory, filename
    #     ),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/{}/".format(
    #         directory
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # #filename = "runner.py"
    # #filename = "runner_from_setup.py"
    # filename = "fit_plotter.py"
    # # rsync_local_to_host(
    # #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-4/2016.1.01188.S/{}".format(filename),
    # #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-4/2016.1.01188.S",
    # #     host="COSMA7",
    # #     update=True
    # # )
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-2/2016.1.01188.S/{}".format(filename),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-2/2016.1.01188.S",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01188.S/science_goal.uid___A001_X87d_X53c/group.uid___A001_X87d_X53d/member.uid___A001_X87d_X53e/product/member.uid___A001_X87d_X53e.HELMS-2_sci.spw0_1_2_3.mfs.I.manual.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01188.S/science_goal.uid___A001_X87d_X53c/group.uid___A001_X87d_X53d/member.uid___A001_X87d_X53e/product",
    #     host="COSMA7",
    #     update=True
    # )

    # ID = "2016.1.01188.S"
    # source = "HELMS-2"
    # #source = "HELMS-4"

    # ID = "2017.1.00027.S"
    # source = "HELMS-8"
    #
    # #filename = "dirty_image.png"
    # filename = "fit_subplots__phase_1.png"
    # #filename = "dirty_image.fits"
    #
    # rsync_host_to_local(
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/{}/{}".format(source, ID, filename),
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/{}".format(source, ID),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/workspace/output/{}".format(source),
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/{}/output/COSMA".format(source, ID),
    #     host="COSMA7",
    #     update=True
    # )

    # 2016.1.00450.S
    # ================== #

    # source = "J142413.9+022304"
    #
    #
    # #filename = "loader.py"
    # filename = "runner.py"
    # #filename = "fit_plotter.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HATLAS_{}/2016.1.00450.S/{}".format(
    #         source, filename
    #     ),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2016.1.00450.S".format(source),
    #     host="COSMA7",
    #     update=True
    # )

    # 2017.1.00027.S
    # ================== #

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-2/2016.1.01188.S/plotter.py",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-2/2016.1.01188.S",
    #     host="COSMA7",
    #     update=True
    # )

    # #source = "G09v1.40"
    # source = "HELMS-8"
    #
    #
    # filename = "runner.py"
    # #filename = "fit_plotter.py"
    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2017.1.00027.S/{}".format(
    #         source, filename
    #     ),
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2017.1.00027.S".format(source),
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2017.1.00027.S/fit_subplots__phase_1.png".format(
    #         source
    #     ),
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/{}/2017.1.00027.S/".format(
    #         source
    #     ),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="",
    #     path_to_file_local="",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/imaging/imaging.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/imaging",
    #     host="COSMA7",
    #     update=True
    # )


    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/imaging/G09v1.40/cube/width_30/G09v1.40_spw_3.clean.cube.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/imaging/G09v1.40/cube/width_30",
    #     host="COSMA7",
    #     update=True
    # )

    rsync_local_to_host(
        path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/calibrated/calibrated.py",
        path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X695/group.uid___A001_X1273_X696/member.uid___A001_X1273_X697/calibrated",
        host="COSMA7",
        update=True
    )



    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6a1/group.uid___A001_X1273_X6a2/member.uid___A001_X1273_X6a3/product/member.uid___A001_X1273_X6a3.HELMS-3_sci.spw19_21_23_25.mfs.I.manual.image.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2017.1.00027.S/science_goal.uid___A001_X1273_X6a1/group.uid___A001_X1273_X6a2/member.uid___A001_X1273_X6a3/product",
    #     host="COSMA7",
    #     update=True
    # )


    # 2016.1.00450.S
    # ================== #

    # width = 30
    # rsync_local_to_host(
    #     path_to_file_local="/Volumes/Elements_v1/2016.1.00450.S/science_goal.uid___A001_X87d_X527/group.uid___A001_X87d_X528/member.uid___A001_X87d_X529/calibrated/width_{}/uid___A002_Xc39302_X4296_field_J142413.9+022304/*.fits".format(width),
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.00450.S/science_goal.uid___A001_X87d_X527/group.uid___A001_X87d_X528/member.uid___A001_X87d_X529/width_{}/uid___A002_Xc39302_X4296_field_J142413.9+022304".format(width),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-2/2016.1.01188.S/plotter.py",
    #     path_to_file_host="/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-2/2016.1.01188.S",
    #     host="COSMA7",
    #     update=True
    # )

    # ----- #

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/workspace/output/",
    #     path_to_file_local="/Users/ccbh87/Desktop/COSMA/cosma/home/durham/dc-amvr1/workspace/runners/interferometer/HELMS-4/2016.1.01188.S/output/COSMA/",
    #     host="COSMA7",
    #     update=True
    # )
