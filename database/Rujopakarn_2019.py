import numpy as np

import matplotlib.pyplot as plt

from astropy import units
from astropy.cosmology import FlatLambdaCDM

# NOTE: We did not iclude of the clumps listed in ALESS009.1 because it was more extended than the main components

sources = {
    "ALESS003.1":{
        "redshift":3.374,
        "main_ext":{"centre":(0.014, 0.009)},
        "main_com":{"centre":(-0.006, -0.006)},
        "clump_1":{"centre":(0.011, 0.199)},
        "clump_2":{"centre":(-0.329, 0.365)},
        "clump_3":{"centre":(-0.289, 0.164)},
    },
    "ALESS009.1":{
        "redshift":4.867,
        "main_ext":{"centre":(-0.009, 0.003)},
        "main_com":{"centre":(-0.022, -0.004)},
        "clump_1":{"centre":(0.177, 0.085)},
        "clump_2":{"centre":(-0.243, -0.177)},
        "clump_3":{"centre":(0.332, -0.002)},
        "clump_4":{"centre":(-0.149, -0.158)},
    },
    "ALESS015.1":{
        "redshift":2.67,
        "main_ext":{"centre":(0.001, 0.003)},
        "main_com":{"centre":(-0.002, 0.003)},
        "clump_1":{"centre":(0.162, -0.205)},
        "clump_2":{"centre":(-0.446, 0.372)},
        "clump_3":{"centre":(-0.072, 0.242)},
        "clump_4":{"centre":(0.337, -0.295)},
    },
    "ALESS017.1":{
        "redshift":1.539,
        "main_ext":{"centre":(0.024, 0.015)},
        "main_com":{"centre":(0.007, 0.005)},
        "clump_1":{"centre":(0.206, 0.118)},
        "clump_2":{"centre":(-0.166, -0.102)},
        "clump_3":{"centre":(0.772, 0.361)},
    },
}


cosmo = FlatLambdaCDM(H0=70, Om0=0.3, Tcmb0=2.725)



# NOTE: In units of kpc
separations = []

for name, components in sources.items():

    z = components["redshift"];print(z)

    main_com_centre = components["main_com"]["centre"]

    for component, component_properties in components.items():

        if component.startswith("clump"):
            clump_centre = component_properties["centre"]

            separation = np.hypot(
                main_com_centre[0] - clump_centre[0],
                main_com_centre[1] - clump_centre[1],
            )

            separations.append(separation * cosmo.kpc_proper_per_arcmin(z=z).to(units.kpc / units.arcsec).value)

separations = np.asarray(separations)

z = 2.0
separations *= cosmo.arcsec_per_kpc_proper(z=z).value

plt.hist(separations, bins=10, histtype="step", linewidth=4,)
plt.xlabel("d (arcsec)", fontsize=15)
plt.show()
