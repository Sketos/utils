

def get_config_path(autolens_version):

    if autolens_version is None:
        raise ValueError
    elif autolens_version in [
        "0.40.0"
    ]:
        pass
    else:
        raise ValueError

    "config_" + autolens_version
