import os


def get_workspace_paths(cosma_server="7"):

    workspace_paths = {
        "HOME":"",
        "DATA":""
    }
    for key in workspace_paths.keys():
        if os.environ["HOME"].startswith("/cosma"):
            workspace_paths[key] = os.environ[
                "COSMA{}_{}_host".format(
                    "" if key == "HOME" else cosma_server,
                    key
                )
            ]
        else:
            workspace_paths[key] = os.environ[
                "COSMA{}_{}_local".format(
                    "" if key == "HOME" else cosma_server,
                    key
                )
            ]

        workspace_paths[key] = "{}/workspace".format(
            workspace_paths[key]
        )

        if not os.path.isdir(workspace_paths[key]):
            raise IOError(
                "{} does not exist".format(workspace_paths[key])
            )

    return workspace_paths


if __name__ == "__main__":

    workspace_paths = get_workspace_paths()
