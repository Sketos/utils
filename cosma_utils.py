import os

hosts = {
    "COSMA":"dc-amvr1@login.cosma.dur.ac.uk:",
    "COSMA5":"dc-amvr1@login5.cosma.dur.ac.uk:",
    "COSMA5a":"dc-amvr1@login5a.cosma.dur.ac.uk:",
    "COSMA5b":"dc-amvr1@login5b.cosma.dur.ac.uk:",
    "COSMA6":"dc-amvr1@login6.cosma.dur.ac.uk:",
    "COSMA7":"dc-amvr1@login7.cosma.dur.ac.uk:",
    "COSMA7a":"dc-amvr1@login7a.cosma.dur.ac.uk:",
    "COSMA7b":"dc-amvr1@login7b.cosma.dur.ac.uk:"
}

def rsync(
    local_path_to_file,
    host_path_to_file,
    host="COSMA",
    update=True
):
    if update:
        os.system("rsync --update -v -r " \
            + local_path_to_file \
            + " " \
            + hosts[host] \
            + host_path_to_file
        )
        print("rsync --update -v -r " \
            + local_path_to_file \
            + " " \
            + hosts[host] \
            + host_path_to_file)
    else:
        os.system("rsync -v -r " \
            + local_path_to_file \
            + " " \
            + hosts[host] \
            + host_path_to_file
        )
        print("rsync -v -r " \
            + local_path_to_file \
            + " " \
            + hosts[host] \
            + host_path_to_file)

def rsync_host_to_local(
    host_path_to_file,
    local_path_to_file,
    host="COSMA7a",
    update=True
):
    if update:
        os.system("rsync --update -v -r " \
            + hosts[host] \
            + host_path_to_file \
            + " " \
            + local_path_to_file
        )
    else:
        os.system("rsync -v -r " \
            + hosts[host] \
            + host_path_to_file \
            + " " \
            + local_path_to_file
        )


if __name__ == "__main__":



    package = "UVgalpak3D"
    local_path_to_file = "/Users/ccbh87/Desktop/GitHub/utils/emcee_wrapper_results.py"
    host_path_to_file = "/cosma/home/durham/dc-amvr1/MyProjects/testing_emcee_wrapper/"

    # script = "emcee_wrapper.py"
    # local_path_to_file = "/Users/ccbh87/Desktop/GitHub/" + package + "/optimizer/" + script
    # host_path_to_file = "/cosma/home/durham/dc-amvr1/MyProjects/" + package + "/optimizer"

    # #script = "model_class.py"
    # script = "model_sersic3d.py"
    # local_path_to_file = "/Users/ccbh87/Desktop/GitHub/" + package + "/galpak/" + script
    # host_path_to_file = "/cosma/home/durham/dc-amvr1/MyProjects/" + package + "/galpak"

    # script = "fit_test.py"
    # local_path_to_file = "/Users/ccbh87/Desktop/GitHub/" + package + "/" + script
    # host_path_to_file = "/cosma/home/durham/dc-amvr1/MyProjects/" + package + "/"

    rsync(
        local_path_to_file=local_path_to_file,
        host_path_to_file=host_path_to_file,
        host="COSMA7a",
        update=True
    )
