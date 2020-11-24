import numpy as np

import matplotlib.pyplot as plt

filename = "/Users/ccbh87/Desktop/GitHub/utils/database/Reuter_et_al_2020_Table_D1.txt"

f_3000, f_2000, f_1400 = np.loadtxt(
    filename, usecols=(2, 4, 6), unpack=True
)
#, usecols=(0, 1, 2)

x_min = 10**-1.0
x_max = 10**2.0

x = np.logspace(np.log10(x_min), np.log10(x_max), 20)

plt.hist(f_3000, bins=x, label=r"$\lambda$ = 3000 $\mu$m", alpha=0.85)
plt.hist(f_2000, bins=x, label=r"$\lambda$ = 2000 $\mu$m", alpha=0.85)
plt.hist(f_1400, bins=x, label=r"$\lambda$ = 1400 $\mu$m", alpha=0.85)
plt.xscale("log")
plt.xlabel("$F_{\lambda}$ (mJy)", fontsize=15)
plt.legend(fontsize=15)
plt.show()
