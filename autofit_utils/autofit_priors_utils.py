import autolens as al
import autofit as af


def set_prior_init(type, **kwargs):

    prior = getattr(
        af, "{}Prior".format(type)
    )

    if type in ["Gaussian"]:
        if not all(
            key in kwargs
            for key in ("mean", "sigma")
        ):
            raise ValueError(
                "{} and {}".format("mean", "sigma")
            )
    elif type in ["Uniform", "LogUniform"]:
        if not all(
            key in kwargs
            for key in ("lower_limit", "upper_limit")
        ):
            raise ValueError(
                "{} and {}".format("lower_limit", "upper_limit")
            )
    else:
        raise ValueError(
            "{} is not supported".format(type)
        )

    return prior(**kwargs)


def set_priors_helper(dict):

    if "type" in dict.keys():
        type = dict["type"]
    else:
        raise ValueError("...")

    kwargs = {
        x: dict[x] for x in dict
        if x not in ["type"]
    }

    return set_prior_init(
        type, **kwargs
    )


# NOTE: Make it so that the GalaxyModel can recognise if the mass profile belongs to subhalo or a SIE. Atm it does not recognise if
# it is applied to the lens or a subhalo

def set_priors_for_GalaxyModel(GalaxyModel, priors=None):

    if not isinstance(GalaxyModel, al.GalaxyModel):
        raise ValueError("...")

    if priors is not None: # TODO: Check is priors is a dictionary

        for i_key in priors.keys():

            if hasattr(GalaxyModel, i_key):

                if isinstance(priors[i_key], dict):

                    for j_key, priors_dict in priors[i_key].items():

                        if hasattr(
                            getattr(GalaxyModel, i_key),
                            j_key
                        ):

                            setattr(
                                getattr(GalaxyModel, i_key),
                                j_key,
                                set_priors_helper(
                                    dict=priors_dict
                                )
                            )

def set_priors(GalaxyModels, priors=None):

    if isinstance(GalaxyModels, list):
        for GalaxyModel in GalaxyModels:
            if not isinstance(GalaxyModel, al.GalaxyModel):
                raise ValueError("...")
    else:
        raise ValueError(
            "must be a list."
        )

    if priors is not None: # TODO: Check is priors is a dictionary

        for i_key in priors.keys():

            for GalaxyModel in GalaxyModels:

                if hasattr(GalaxyModel, i_key):

                    if isinstance(priors[i_key], dict):

                        for j_key, priors_dict in priors[i_key].items():

                            if hasattr(
                                getattr(GalaxyModel, i_key),
                                j_key
                            ):

                                setattr(
                                    getattr(GalaxyModel, i_key),
                                    j_key,
                                    set_priors_helper(
                                        dict=priors_dict
                                    )
                                )
