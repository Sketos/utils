import numpy as np

import matplotlib.pyplot as plt

r_21 = 0.9
r_31 = 0.60
r_41 = 0.32

sources = {
    "006.1": {
        "z":2.3368,
        "SNR":10.4,
        "M_gas":None,
        "M_star":10**10.83,
        "LCO10":7.349885322482861E10,
        "effective_radius":0.246,
        "inclination":51.942,
        "maximum_velocity":586.769,
        "velocity_dispersion":180.071,
        "ML":{
            "effective_radius":0.230,
            "effective_radius_1sigma_upper":0.268,
            "effective_radius_1sigma_lower":0.196,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":521.997,
            "maximum_velocity_1sigma_upper":611.004,
            "maximum_velocity_1sigma_lower":435.494,
            "velocity_dispersion":165.827,
            "velocity_dispersion_1sigma_upper":146.522,
            "velocity_dispersion_1sigma_lower":197.940,
        }
    },
    "017.1": {
        "z":1.5383,
        "SNR":45.4,
        "M_gas":None,
        "M_star":10**11.37,
        "LCO10":2.251621229139973E10,
        "effective_radius":0.376,
        "inclination":31.810,
        "maximum_velocity":494.103,
        "velocity_dispersion":59.585,
        "ML":{
            "effective_radius":0.410,
            "effective_radius_1sigma_upper":0.465,
            "effective_radius_1sigma_lower":0.344,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":417.381,
            "maximum_velocity_1sigma_upper":569.24,
            "maximum_velocity_1sigma_lower":318.200,
            "velocity_dispersion":72.946,
            "velocity_dispersion_1sigma_upper":89.037,
            "velocity_dispersion_1sigma_lower":56.809,
        }
    },
    "041.1": {
        "z":2.5470,
        "SNR":8.2,
        "M_gas":None,
        "M_star":10**11.35,
        "LCO10":2.9 * 10**10 * r_31,
        "effective_radius":0.295,
        "inclination":71.556,
        "maximum_velocity":376.778,
        "velocity_dispersion":54.027,
        "ML":{
            "effective_radius":0.277,
            "effective_radius_1sigma_upper":0.294,
            "effective_radius_1sigma_lower":0.259,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":391.073,
            "maximum_velocity_1sigma_upper":404.659,
            "maximum_velocity_1sigma_lower":376.233,
            "velocity_dispersion":48.399,
            "velocity_dispersion_1sigma_upper":54.879,
            "velocity_dispersion_1sigma_lower":41.699,
        }
    },
    # "049.1": {
    #     "z":2.9451,
    #     "SNR":10.0,
    #     "M_gas":None,
    #     "M_star":None,
    #     "effective_radius":0.0,
    #     "inclination":0.0,
    #     "maximum_velocity":0.0,
    #     "velocity_dispersion":0.0
    # },
    "062.2": {
        "z":1.3620,
        "SNR":15.9,
        "M_gas":None,
        "M_star":None,
        "LCO10":4.0939875280275734E10,
        "effective_radius":0.277,
        "inclination":76.376,
        "maximum_velocity":241.358,
        "velocity_dispersion":92.782,
        "ML":{
            "effective_radius":0.279,
            "effective_radius_1sigma_upper":0.343,
            "effective_radius_1sigma_lower":0.126,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":254.117,
            "maximum_velocity_1sigma_upper":317.444,
            "maximum_velocity_1sigma_lower":87.202,
            "velocity_dispersion":99.172,
            "velocity_dispersion_1sigma_upper":122.141,
            "velocity_dispersion_1sigma_lower":32.648,
        }
    },
    "065.1": {
        "z":4.4454,
        "SNR":14.0,
        "M_gas":None,
        "M_star":10**10.74,
        "LCO10":8.296110565525145E10,
        "effective_radius":0.177,
        "inclination":52.175,
        "maximum_velocity":434.200,
        "velocity_dispersion":25.391,
        "ML":{
            "effective_radius":0.207,
            "effective_radius_1sigma_upper":0.246,
            "effective_radius_1sigma_lower":0.157,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":430.702,
            "maximum_velocity_1sigma_upper":509.558,
            "maximum_velocity_1sigma_lower":350.077,
            "velocity_dispersion":41.303,
            "velocity_dispersion_1sigma_upper":64.659,
            "velocity_dispersion_1sigma_lower":12.718,
        }
    },
    "066.1": {
        "z":2.5526,
        "SNR":29.8,
        "M_gas":None,
        "M_star":10**10.07,
        "LCO10":4.979984938883548E10,
        "effective_radius":0.384,
        "inclination":46.675,
        "maximum_velocity":481.201,
        "velocity_dispersion":87.632,
        "ML":{
            "effective_radius":0.426,
            "effective_radius_1sigma_upper":0.493,
            "effective_radius_1sigma_lower":0.357,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":419.704,
            "maximum_velocity_1sigma_upper":558.355,
            "maximum_velocity_1sigma_lower":296.912,
            "velocity_dispersion":91.916,
            "velocity_dispersion_1sigma_upper":110.431,
            "velocity_dispersion_1sigma_lower":73.676,
        }
    },
    "071.1": {
        "z":3.7089,
        "SNR":4.8,
        "M_gas":None,
        "M_star":10**11.39,
        "LCO10":4.5 * 10**10 * r_41,
        "effective_radius":0.426,
        "inclination":62.488,
        "maximum_velocity":389.650,
        "velocity_dispersion":39.332,
        "ML":{
            "effective_radius":0.482,
            "effective_radius_1sigma_upper":0.538,
            "effective_radius_1sigma_lower":0.426,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":367.951,
            "maximum_velocity_1sigma_upper":390.404,
            "maximum_velocity_1sigma_lower":349.093,
            "velocity_dispersion":67.193,
            "velocity_dispersion_1sigma_upper":91.112,
            "velocity_dispersion_1sigma_lower":43.046,
        }
    },
    "075.1": {
        "z":2.5521,
        "SNR":8.0,
        "M_gas":None,
        "M_star":10**10.48,
        "LCO10":3.4 * 10**10 * r_31,
        "effective_radius":0.318,
        "inclination":51.459,
        "maximum_velocity":373.606,
        "velocity_dispersion":110.944,
        "ML":{
            "effective_radius":0.318,
            "effective_radius_1sigma_upper":0.336,
            "effective_radius_1sigma_lower":0.301,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":385.580,
            "maximum_velocity_1sigma_upper":413.386,
            "maximum_velocity_1sigma_lower":349.242,
            "velocity_dispersion":107.637,
            "velocity_dispersion_1sigma_upper":116.674,
            "velocity_dispersion_1sigma_lower":98.323,
        }
    },
    "098.1": {
        "z":1.3739,
        "SNR":12.7,
        "M_gas":None,
        "M_star":10**11.87,
        "LCO10":9.821001334082928E10,
        "effective_radius":0.221,
        "inclination":38.135,
        "maximum_velocity":579.436,
        "maximum_velocity_error":0.0,
        "velocity_dispersion":20.703,
        "ML":{
            "effective_radius":0.222,
            "effective_radius_1sigma_upper":0.235,
            "effective_radius_1sigma_lower":0.209,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":555.133,
            "maximum_velocity_1sigma_upper":602.689,
            "maximum_velocity_1sigma_lower":531.371,
            "velocity_dispersion":26.489,
            "velocity_dispersion_1sigma_upper":43.175,
            "velocity_dispersion_1sigma_lower":9.025,
        }
    },
    "101.1": {
        "z":2.3531,
        "SNR":14.7,
        "M_gas":None,
        "M_star":None,
        "LCO10":6.21751350038522E10,
        "effective_radius":0.461,
        "inclination":54.040,
        "maximum_velocity":526.367,
        "velocity_dispersion":171.298,
        "ML":{
            "effective_radius":0.422,
            "effective_radius_1sigma_upper":0.479,
            "effective_radius_1sigma_lower":0.346,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":524.231,
            "maximum_velocity_1sigma_upper":594.363,
            "maximum_velocity_1sigma_lower":471.001,
            "velocity_dispersion":163.364,
            "velocity_dispersion_1sigma_upper":201.163,
            "velocity_dispersion_1sigma_lower":153.442,
        }
    },
    "112.1": {
        "z":2.3135,
        "SNR":17.3,
        "M_gas":None,
        "M_star":10**11.01,
        "LCO10":7.489146404175594E10,
        "effective_radius":0.283,
        "inclination":55.538,
        "maximum_velocity":465.731,
        "velocity_dispersion":173.600,
        "ML":{
            "effective_radius":0.268,
            "effective_radius_1sigma_upper":0.305,
            "effective_radius_1sigma_lower":0.232,
            "inclination":0.0,
            "inclination_1sigma_upper":0.0,
            "inclination_1sigma_lower":0.0,
            "maximum_velocity":494.359,
            "maximum_velocity_1sigma_upper":559.465,
            "maximum_velocity_1sigma_lower":437.326,
            "velocity_dispersion":167.582,
            "velocity_dispersion_1sigma_upper":192.965,
            "velocity_dispersion_1sigma_lower":148.786,
        }
    },
}


# NOTE: most likely model, most probable model (in this case have errors as well)



if __name__ == "__main__":

    a = sources.keys()

    # x_property = "z"; xlabel = "z"
    # y_property = "maximum_velocity"; ylabel=r"$V_{max}$ (km /s)"
    #
    # x = []
    # y = []
    # for key in a:
    #     if key in sources.keys():
    #         source_properies = sources[key]
    #
    #         x.append(source_properies[x_property])
    #         y.append(source_properies[y_property])


    # x_property = "z"; xlabel = "z"
    # y1_property = "maximum_velocity";y1label=r"$V_{max}$"
    # y2_property = "velocity_dispersion";y2label=r"$\sigma$"
    # ylabel = "{} / {}".format(y1label, y2label)
    # xlim = (1.0, 5.0)
    #
    # x = []
    # y1 = []
    # y2 = []
    # for key in a:
    #     if key in sources.keys():
    #         source_properies = sources[key]
    #
    #         x.append(source_properies[x_property])
    #         y1.append(source_properies[y1_property])
    #         y2.append(source_properies[y2_property])
    #
    # plt.figure()
    # plt.plot(x, np.asarray(y1) / np.asarray(y2), linestyle="None", marker="o", markersize=10, color="b")
    # plt.xlabel(xlabel, fontsize=15)
    # plt.ylabel(ylabel, fontsize=15)
    # plt.xlim(xlim)
    # plt.show()



    x = []

    y1 = []
    y1_error_upper = []
    y1_error_lower = []
    y2 = []
    y2_error_upper = []
    y2_error_lower = []

    z = []



    for key in a:
        if key in sources.keys():
            source_properies = sources[key]

            _x = source_properies["z"]
            #_x = source_properies["M_star"]

            if _x is not None:
                x.append(_x)

                source_properies_MP = source_properies["ML"]

                y1.append(source_properies_MP["maximum_velocity"])
                y1_error_upper.append(
                    abs(source_properies_MP["maximum_velocity_1sigma_upper"] - source_properies_MP["maximum_velocity"])
                )
                y1_error_lower.append(
                    abs(source_properies_MP["maximum_velocity_1sigma_lower"] - source_properies_MP["maximum_velocity"])
                )

                y2.append(source_properies_MP["velocity_dispersion"])
                y2_error_upper.append(
                    abs(source_properies_MP["velocity_dispersion_1sigma_upper"] - source_properies_MP["velocity_dispersion"])
                )
                y2_error_lower.append(
                    abs(source_properies_MP["velocity_dispersion_1sigma_lower"] - source_properies_MP["velocity_dispersion"])
                )

                z.append(source_properies_MP["effective_radius"])

    # =====
    # NOTE: TEST

    M1 = []
    M2 = []

    z_temp = []

    for key in a:
        if key in sources.keys():
            source_properies = sources[key]

            if source_properies["M_star"] is not None:
                print(key)
                _M1 = source_properies["LCO10"] * 1.36
                _M2 = source_properies["M_star"]

                M1.append(_M1)
                M2.append(_M2)

                source_properies_MP = source_properies["ML"]
                z_temp.append(source_properies_MP["maximum_velocity"])


    M1 = np.asarray(M1)
    M2 = np.asarray(M2)
    z_temp = np.asarray(z_temp)

    data = np.array([
        [2.092573402417962, 9.620353982300884],
        [2.1036269430051817, 9.648672566371681],
        [2.0994818652849743, 9.691150442477877],
        [2.167184801381693, 9.641592920353983],
        [2.1796200345423147, 9.765486725663717],
        [2.204490500863558, 9.846902654867257],
        [2.116062176165803, 9.804424778761062],
        [2.2487046632124352, 9.967256637168141],
        [2.306735751295337, 10.045132743362831],
        [2.2639032815198616, 10.087610619469027],
        [2.2473229706390327, 10.169026548672566],
        [2.1340241796200345, 10.204424778761062],
        [2.233506044905009, 10.285840707964601],
        [2.2791018998272885, 10.285840707964601],
        [2.3081174438687393, 10.324778761061946],
        [2.3288428324697756, 10.204424778761062],
        [2.360621761658031, 10.165486725663717],
        [2.3329879101899826, 10.409734513274337],
        [2.3233160621761657, 10.487610619469027],
        [2.3813471502590673, 10.526548672566372],
        [2.4352331606217614, 10.406194690265487],
        [2.436614853195164, 10.565486725663717],
        [2.4573402417962003, 10.728318584070797],
        [2.4849740932642486, 10.884070796460177],
        [2.5236614853195163, 10.84867256637168],
        [2.5443868739205526, 10.965486725663716],
        [2.690846286701209, 10.887610619469026],
        [2.4379965457685664, 11.043362831858406],
    ])


    plt.figure()
    plt.plot(data[:, 0], data[:, 1], linestyle="None", marker="o", markersize=2.5, color="black", label="ETG (z = 0)")
    #plt.errorbar(x, y1, yerr=(y1_error_lower, y1_error_upper), linestyle="None", marker="o", markersize=10, color="b")
    plt.plot(np.log10(z_temp), np.log10(M1 + M2), linestyle="None", marker="o", markersize=10, color="b", label="This work")
    #plt.xlabel("z", fontsize=15)
    #plt.ylabel(r"$R_{eff}$ (arcsec)", fontsize=15)
    plt.xlim((2.0, 3.0))
    plt.ylim((9.5, 12.0))

    plt.xlabel(r"$\log_{10}(V_{max})$ (km / s)", fontsize=15)
    plt.ylabel(r"$\log_{10}(M_{gas} + M_{star}) \,\, (M_{\odot})$", fontsize=15)
    plt.legend()
    plt.show()

    # =====



    def error_propagation(A, B, A_error, B_error):

        return np.sqrt(
            (A / B)**2.0 * ((A_error / A)**2.0 + (B_error / B)**2.0)
        )

    y = np.asarray(y1) / np.asarray(y2)
    y_error_upper = error_propagation(
        A=np.asarray(y1),
        B=np.asarray(y2),
        A_error=np.asarray(y1_error_upper),
        B_error=np.asarray(y2_error_upper)
    )
    y_error_lower = error_propagation(
        A=np.asarray(y1),
        B=np.asarray(y2),
        A_error=np.asarray(y1_error_lower),
        B_error=np.asarray(y2_error_lower)
    )

    # plt.figure()
    # plt.errorbar(x, y1, yerr=(y1_error_lower, y1_error_upper), linestyle="None", marker="o", markersize=10, color="b")
    # #plt.xlabel(xlabel, fontsize=15)
    # ##plt.ylabel(ylabel, fontsize=15)
    # #plt.xlim(xlim)
    # plt.show()

    # plt.figure()
    # #plt.errorbar(x, y1, yerr=(y1_error_lower, y1_error_upper), linestyle="None", marker="o", markersize=10, color="b")
    # plt.plot(x, z, linestyle="None", marker="o", markersize=10, color="b")
    # plt.xlabel("z", fontsize=15)
    # plt.ylabel(r"$R_{eff}$ (arcsec)", fontsize=15)
    # #plt.xlim(xlim)
    # plt.show()



    # plt.figure()
    # plt.errorbar(x, y, yerr=(y_error_lower, y_error_upper), linestyle="None", marker="o", markersize=5, color="b")
    #
    # xlabel = "z"
    #
    # # xlabel = "$M_{\star}$ ($M_{\odot}$)"
    # # plt.xscale("log")
    #
    # plt.xlabel(xlabel, fontsize=15)
    #
    #
    # ylabel = r"$V_{max} / \sigma$"
    # plt.ylabel(ylabel, fontsize=15)
    # plt.show()
