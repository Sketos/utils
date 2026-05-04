import numpy as np

from astropy import units


def axis_ratio_and_phi_from(elliptical_comps):
    """
    Convert the ellipitical components e1 and e2 to an axis ratio (0.0 > q > 1.0) and rotation position angle
    defined counter clockwise from the positive x-axis(0.0 > angle > 180) to .

    Parameters
    ----------
    elliptical_comps : (float, float)
        The first and second ellipticity components of the elliptical coordinate system, where
        fac = (1 - axis_ratio) / (1 + axis_ratio), ellip_y = fac * sin(2*angle) and ellip_x = fac * cos(2*angle).
    """
    angle = np.arctan2(elliptical_comps[0], elliptical_comps[1]) / 2
    angle *= 180.0 / np.pi
    fac = np.sqrt(elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2)
    if fac > 0.999:
        fac = 0.999  # avoid unphysical solution
    # if fac > 1: print('unphysical e1,e2')
    axis_ratio = (1 - fac) / (1 + fac)

    return axis_ratio, angle

def shear_magnitude_and_phi_from(elliptical_comps):
    """
    :param e1: ellipticity component
    :param e2: ellipticity component
    :return: angle and abs value of ellipticity
    """
    angle = np.arctan2(elliptical_comps[0], elliptical_comps[1]) / 2 * 180.0 / np.pi
    magnitude = np.sqrt(elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2)
    if angle < 0:
        return magnitude, angle + 180.0
    else:
        return magnitude, angle


def elliptical_comps_from(axis_ratio, angle):
    """
    Convert an input axis ratio (0.0 > q > 1.0) and rotation position angle defined counter clockwise from the
    positive x-axis(0.0 > angle > 180) to the (y,x) ellipitical components e1 and e2.

    Parameters
    ----------
    axis_ratio : float
        Ratio of light profiles ellipse's minor and major axes (b/a).
    angle : float
        Rotation angle of light profile counter-clockwise from positive x-axis.
    """
    angle *= np.pi / 180.0
    fac = (1 - axis_ratio) / (1 + axis_ratio)
    ellip_y = fac * np.sin(2 * angle)
    ellip_x = fac * np.cos(2 * angle)
    return (ellip_y, ellip_x)

def shear_elliptical_comps_from(magnitude, angle):
    """
    :param angle: angel
    :param magnitude: ellipticity
    :return:
    """
    ellip_y = magnitude * np.sin(2 * angle * np.pi / 180.0)
    ellip_x = magnitude * np.cos(2 * angle * np.pi / 180.0)
    return (ellip_y, ellip_x)


# # NOTE: OLD
# def multipole_parameters_from(elliptical_comps):
#
#     phi_m = np.arctan(
#         elliptical_comps[0] / elliptical_comps[1]
#     ) * units.rad.to(units.deg)
#     k_m = np.sqrt(
#         elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
#     )
#
#     if phi_m < 0.:
#         return k_m, phi_m + 90.0
#     return k_m, phi_m

# NOTE: DELETE
# def multipole_parameters_from(elliptical_comps):
#
#     phi_m = np.arctan2(
#         elliptical_comps[0],
#         elliptical_comps[1]
#     ) * 180.0 / np.pi
#     k_m = np.sqrt(
#         elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
#     )
#
#     return k_m, phi_m

def multipole_m1_parameters_from(elliptical_comps):
    phi_m = np.arctan2(
        elliptical_comps[0],
        elliptical_comps[1]
    ) * 180.0 / np.pi
    k_m = np.sqrt(
        elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
    )

    return k_m, phi_m
def multipole_m2_parameters_from(elliptical_comps):
    phi_m = np.arctan2(
        elliptical_comps[0],
        elliptical_comps[1]
    ) / 2.0 * 180.0 / np.pi
    k_m = np.sqrt(
        elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
    )

    return k_m, phi_m
def multipole_m3_parameters_from(elliptical_comps):
    phi_m = np.arctan2(
        elliptical_comps[0],
        elliptical_comps[1]
    ) / 3.0 * 180.0 / np.pi
    k_m = np.sqrt(
        elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
    )

    return k_m, phi_m
def multipole_m4_parameters_from(elliptical_comps):
    phi_m = np.arctan2(
        elliptical_comps[0],
        elliptical_comps[1]
    ) / 4.0 * 180.0 / np.pi
    k_m = np.sqrt(
        elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
    )

    return k_m, phi_m
def multipole_m_parameters_from(elliptical_comps, m):
    phi_m = np.arctan2(
        elliptical_comps[0],
        elliptical_comps[1]
    ) * 180.0 / np.pi / float(m)
    k_m = np.sqrt(
        elliptical_comps[1] ** 2 + elliptical_comps[0] ** 2
    )

    return k_m, phi_m


def elliptical_comps_multipole_from(k_m, phi_m):

    elliptical_comp_0 = k_m * np.sin(phi_m * units.deg.to(units.rad))
    elliptical_comp_1 = k_m * np.cos(phi_m * units.deg.to(units.rad))

    return (
        elliptical_comp_0,
        elliptical_comp_1
    )
def elliptical_comps_multipole_m_from(k_m, phi_m, m):

    elliptical_comp_0 = k_m * np.sin(phi_m * float(m) * units.deg.to(units.rad))
    elliptical_comp_1 = k_m * np.cos(phi_m * float(m) * units.deg.to(units.rad))

    return (
        elliptical_comp_0,
        elliptical_comp_1
    )

def a_m(elliptical_comps, m, einstein_radius, slope):

    k_m, phi_m = multipole_m_parameters_from(
        m=m, elliptical_comps=elliptical_comps,
    )

    return einstein_radius**(slope - 1.0) / 2.0 * k_m * np.cos(phi_m * float(m) * units.deg.to(units.rad))

def b_m(elliptical_comps, m, einstein_radius, slope):


    k_m, phi_m = multipole_m_parameters_from(
        m=m, elliptical_comps=elliptical_comps,
    )

    return einstein_radius**(slope - 1.0) / 2.0 * k_m * np.sin(phi_m * float(m) * units.deg.to(units.rad))


if __name__ == "__main__":

    # NOTE: SPT-2147
    multipole_m1_elliptical_comps = (-0.0185, 0.0922)
    einstein_radius = 1.1960
    slope = 2.1503
    a_1 = a_m(
        m=1,
        elliptical_comps=multipole_m1_elliptical_comps,
        einstein_radius=einstein_radius,
        slope=slope
    )
    b_1 = b_m(
        m=1,
        elliptical_comps=multipole_m1_elliptical_comps,
        einstein_radius=einstein_radius,
        slope=slope
    )
    print(a_1, b_1, np.hypot(a_1, b_1))
    exit()

    # NOTE: HerBS-155
    elliptical_comps = (0.144, -0.123) # NOTE: parametric
    axis_ratio, angle = axis_ratio_and_phi_from(
        elliptical_comps=elliptical_comps
    )
    print(axis_ratio, angle);exit()

    # SPT-0418 (Qiuhan vs Aris; jwst f444)
    elliptical_comps = (0.013, 0.022) # Sam
    elliptical_comps = (0.040, 0.057) # Qiuhan
    elliptical_comps = (0.020, -0.023) # Aris -
    #elliptical_comps = (0.016, -0.036) # Aris - DelaunayMagnification_and_ConstantSplit
    #elliptical_comps = (0.019, -0.029) # Aris - VoronoiNNMagnification_and_ConstantSplit
    #elliptical_comps = (0.027, -0.040) # Aris - VoronoiNNMagnification_and_Vernardos
    # SPT-2147 (lens light)
    elliptical_comps = (0.043, -0.051) # Aris -
    print(
        axis_ratio_and_phi_from(
            elliptical_comps=elliptical_comps
        )
    )
    exit()

    # # NOTE: SPT-2147
    # # elliptical_comps = (0.032, -0.087) # SAM
    # # print(
    # #     axis_ratio_and_phi_from(
    # #         elliptical_comps=elliptical_comps
    # #     )
    # # )
    # # elliptical_comps = (0.107, -0.085) # ARIS
    # # print(
    # #     axis_ratio_and_phi_from(
    # #         elliptical_comps=elliptical_comps
    # #     )
    # # )
    #
    # elliptical_comps = (-0.014, 0.030) # SAM
    # print(
    #     shear_magnitude_and_phi_from(
    #         elliptical_comps=elliptical_comps
    #     )
    # )
    # elliptical_comps = (0.028, 0.026) # ARIS
    # print(
    #     shear_magnitude_and_phi_from(
    #         elliptical_comps=elliptical_comps
    #     )
    # )
    # exit()


    # # NOTE: SPT-0532; lres
    # #elliptical_comps=(0.023, 0.011) # from_source_inversion[2]_VoronoiNNBrightnessImage_and_AdaptiveBrightnessSplit/mass_total[1]_mass[total]_source
    # #elliptical_comps=(0.01855222789129933, 0.006930084477014688)
    # for elliptical_comps in [(0.023, 0.011), (0.01855222789129933, 0.006930084477014688)]:
    #     print(
    #         shear_magnitude_and_phi_from(
    #             elliptical_comps=elliptical_comps
    #         )
    #     )

    # # NOTE: SPT-0418; lres (subhalo)
    # for elliptical_comps in [(-0.0101, 0.010), (-0.005, -0.003)]:
    #     print(
    #         shear_magnitude_and_phi_from(
    #             elliptical_comps=elliptical_comps
    #         )
    #     )

    # NOTE: SPT-0538; lres (subhalo)
    for elliptical_comps in [
        #(-0.008, 0.005), (0.010, 0.007) # NOTE: VoronoiNNBrightnessImage & AdaptiveBrightnessSplit (x1 lenses vs x2 lenses)
        (0.010, 0.002), (0.013, -0.007) #NOTE: DelaunayMagnification & ConstantSplit (x1 lenses vs x2 lenses)
    ]:
        print(
            shear_magnitude_and_phi_from(
                elliptical_comps=elliptical_comps
            )
        )
    exit()


    # NOTE: Stacey et al. (2021)
    # mass_axis_ratio = 0.843
    # mass_angle = 90.0 - 25.5
    # print(
    #     elliptical_comps_from(
    #         axis_ratio=mass_axis_ratio,
    #         angle=mass_angle
    #     )
    # )
    # shear_magnitude = 0.0112
    # shear_angle = 90 - 24.0
    # print(
    #     shear_elliptical_comps_from(
    #         magnitude=shear_magnitude,
    #         angle=shear_angle
    #     )
    # )
    # exit()



    # # SPT-0532; phase 2 (inversion with fixed pixelization; (50, 50))
    # elliptical_comps_0 = 0.069
    # elliptical_comps_1 = -0.046
    # # SPT-0532; phase 2 (inversion)
    #elliptical_comps_0 = 0.076
    #elliptical_comps_1 =  -0.057
    # elliptical_comps_0 = 0.073
    # elliptical_comps_1 =  -0.050
    # HELMS-34; phase 1 (parametric)
    #elliptical_comps_0 = 0.357
    #elliptical_comps_1 = -0.027
    # # HELMS-34; phase 1 (parametric; lens:sie; with priors on centre)
    # elliptical_comps_0 = -0.042
    # elliptical_comps_1 = 0.107
    # HELMS-34; phase 1 (parametric; lens:sie + shear; with priors on centre)
    elliptical_comps_0 = -0.241
    elliptical_comps_1 = -0.019
    # SDP11 (2016.1.000282);
    elliptical_comps_0 = 0.351
    elliptical_comps_1 = -0.141
    # SDP11 (2015.1.01362);
    elliptical_comps_0 = 0.303
    elliptical_comps_1 = -0.408
    print(
        axis_ratio_and_phi_from(
            elliptical_comps=(
                elliptical_comps_0,
                elliptical_comps_1
            )
        )
    )
    #exit()


    # SPT-0532; phase 2 (inversion with fixed pixelization; (50, 50))
    # shear_elliptical_comps_0 = -0.001
    # shear_elliptical_comps_1 = 0.007
    # SPT-0532; phase 2 (inversion)
    #shear_elliptical_comps_0 = 0.004
    #shear_elliptical_comps_1 = 0.004
    # HELMS-34; phase 1 (parametric)
    #shear_elliptical_comps_0 = 0.184
    #shear_elliptical_comps_1 = -0.199
    # HELMS-34; phase 1 (parametric; lens:sie + shear; with priors on centre)
    shear_elliptical_comps_0 = -0.115
    shear_elliptical_comps_1 = -0.066
    # SDP11 (2016.1.000282);
    shear_elliptical_comps_0 = 0.200
    shear_elliptical_comps_1 = -0.034
    # SDP11 (2015.1.01362);
    shear_elliptical_comps_0 = 0.198
    shear_elliptical_comps_1 = -0.200
    print(
        shear_magnitude_and_phi_from(
            elliptical_comps=(
                shear_elliptical_comps_0,
                shear_elliptical_comps_1
            )
        )
    )
    exit()

    def elliptical_comps_for_simulations(model):

        if model in [
            "model_1",
            "model_2",
            "model_3",
            "model_4",
            "model_5"
        ]:
            if model == "model_1":
                mass_profile_axis_ratio = 0.75
                mass_profile_phi = 120.0

                shear_profile_magnitude = 0.05
                shear_profile_phi = 120.0

            if model == "model_2":
                raise NotImplementedError()

            if model == "model_3":
                raise NotImplementedError()

            if model == "model_4":
                raise NotImplementedError()

            if model == "model_5":
                raise NotImplementedError()
        else:
            raise NotImplementedError()

        mass_profile_elliptical_comps = elliptical_comps_from(
            axis_ratio=mass_profile_axis_ratio,
            angle=mass_profile_phi
        )
        shear_profile_elliptical_comps = shear_elliptical_comps_from(
            magnitude=shear_profile_magnitude,
            angle=shear_profile_phi
        )

        print(
            mass_profile_elliptical_comps,
            shear_profile_elliptical_comps
        )

        mass_profile_axis_ratio_from, mass_profile_phi_from = axis_ratio_and_phi_from(
            elliptical_comps=mass_profile_elliptical_comps
        )
        shear_profile_magnitude_from, shear_profile_phi_from = shear_magnitude_and_phi_from(
            elliptical_comps=shear_profile_elliptical_comps
        )

        print(mass_profile_axis_ratio, mass_profile_axis_ratio_from)
        print(mass_profile_phi, mass_profile_phi_from)
        print(shear_profile_magnitude, shear_profile_magnitude_from)
        print(shear_profile_phi, shear_profile_phi_from)


    elliptical_comps_for_simulations(model="model_1")
