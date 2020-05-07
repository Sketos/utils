import autofit as af


# Priors_pixelization = {
#     "VoronoiMagnification":{
#         "shape_0":{
#             "type": "Uniform",
#             "lower_limit": 5.0,
#             "upper_limit": 50.0,
#         },
#         "shape_1":{
#             "type": "Uniform",
#             "lower_limit": 5.0,
#             "upper_limit": 50.0,
#         }
#     }
# }
#
# Priors_regularization = {
#     "Constant":{
#         "coefficient":{
#             "type": "LogUniform",
#             "lower_limit": 10**-1.0,
#             "upper_limit": 10**+5.0,
#         }
#     }
# }
#
# priors_temp = {
#     "SphericalNFWMCRLudlow":{
#         "mass_at_200":{
#             "type": "LogUniform",
#             "lower_limit": 1.0e6,
#             "upper_limit": 1.0e11,
#         },
#         "centre_0":{
#             "type": "Uniform",
#             "lower_limit": -2.0,
#             "upper_limit": 2.0,
#         },
#         "centre_1":{
#             "type": "Uniform",
#             "lower_limit": -2.0,
#             "upper_limit": 2.0,
#         }
#     }
# }
#
# priors = {
#     "EllipticalIsothermal":{
#         "einstein_radius":{
#             "type": "Uniform",
#             "lower_limit": -2.0,
#             "upper_limit": 2.0,
#         },
#     }
# }


def set_prior_helper(type, **kwargs):

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


def set_prior(dict):

    if "type" in dict.keys():
        type = dict["type"]
    else:
        raise ValueError("")

    kwargs = {
        x: dict[x] for x in dict
        if x not in ["type"]
    }

    return set_prior_helper(
        type, **kwargs
    )


# NOTE: Make it so that the GalaxyModel can be recognised. Atm it does not recognise if
# it is applied to the lens or a subhalo
# TODO: Take as input a list of GalaxyModels (e.g. for lens, subhalo, source)
def funcname(GalaxyModel, priors):

    if isinstance(GalaxyModel, al.GalaxyModel):
        pass
    else:
        raise ValueError

    if priors is not None:

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
                                set_prior(
                                    dict=priors_dict
                                )
                            )
