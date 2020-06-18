import os

import cosma_utils as cosma_utils
import directory_utils as directory_utils


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




    rsync_local_to_host(
        path_to_file_local="{}/".format(
            path_to_file_local,
        ),
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
    if not os.path.isfile(path_to_file_local):
        raise IOError(
            "The file {} does not exist".format(path_to_file_local)
        )

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
    #rsync_filename_autofit_tutorials(n=6, filename="runner__lens__powerlaw__source__kinematics__data__lens__powerlaw__source__kinematics.py")

    #rsync_config(version="0.45.0")

    # package = "autolens"
    # #package = "autoarray"
    # rsync_packages_from_venv(autolens_version="0.45.0", package=package)

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/GitHub/utils/alma_tickets/downloadRequest1653617499451.sh",
    #     path_to_file_host="{}/{}".format(os.environ["COSMA7_DATA_host"], "ALMA_archive_data"),
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_local_to_host(
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/ms.py",
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5",
    #     host="COSMA7",
    #     update=True
    # )

    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/width_128/uv_wavelengths_spw_23.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X31/group.uid___A001_X894_X32/member.uid___A001_X894_X33/calibrated_5.1.1-5/",
    #     host="COSMA7",
    #     update=True
    # )

    rsync_host_to_local(
        path_to_file_host="/cosma7/data/dp004/dc-amvr1/tutorials/autofit/tutorial_6/output/runner__lens__powerlaw__source__kinematics__data__lens__powerlaw__source__kinematics",
        path_to_file_local="/Users/ccbh87/Desktop/GitHub/tutorials/autofit/tutorial_6/output_cosma",
        host="COSMA7",
        update=True
    )


    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/product/member.uid___A001_X894_X39._SPT-S_J053816-5030.8__sci.spw21_23_25_27.cont.I.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X39/product/",
    #     host="COSMA7",
    #     update=True
    # )
    # rsync_host_to_local(
    #     path_to_file_host="/cosma7/data/dp004/dc-amvr1/ALMA_archive_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X3b/product/uid___A001_X894_X3b._SPT-S_J053816-5030.8__sci.spw21_23_25_27.cont.I.pbcor.fits",
    #     path_to_file_local="/Users/ccbh87/Desktop/ALMA_data/2016.1.01374.S/science_goal.uid___A001_X894_X37/group.uid___A001_X894_X38/member.uid___A001_X894_X3b/product/",
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
    # #script_filename = "calibration_utils.py"
    # #script_filename = "random_utils.py"
    # script_filename = "casa_utils.py"
    #
    # rsync_scripts_from_github_directory__utils(
    #     script_filename=script_filename
    # )

    # script_filename = "autolens_plot_utils.py"
    # #script_filename = "autolens_tracer_utils.py"
    #
    # rsync_scripts_from_github_directory__autolens_utils(
    #     script_filename=script_filename
    # )

    # #script_filename = "autolens_plot_utils.py"
    # script_filename = "load_utils.py"
    #
    # rsync_scripts_from_github_directory__interferometry_utils(
    #     script_filename=script_filename
    # )
