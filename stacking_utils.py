import os

import numpy as np

import matplotlib.pyplot as plt

from astropy import units, \
                    constants
from astropy.io import fits


if __name__ == "__main__":

    uv_taper = "500klambda"
    niter = 5000

    if niter == 0:
        filename_1 = "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_{}.clean.cube.image.pbcor.fits".format(uv_taper)
    else:
        filename_1 = "/Volumes/Elements_v1/SDP81/SDP81_Band4_CalibratedData/SDP.81/CO54/uvcontsub/SDP.81_{}_niter_{}.clean.cube.image.pbcor.fits".format(
            uv_taper, niter
        )
    if niter == 0:
        filename_2 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}.clean.cube.image.pbcor.fits".format(uv_taper)
    else:
        filename_2 = "/Volumes/Elements_v1/SDP81/SDP81_Band6_CalibratedData/SDP.81/CO87/uvcontsub/SDP.81_{}_niter_{}.clean.cube.image.pbcor.fits".format(
            uv_taper, niter
        )

    data_1 = fits.getdata(filename=filename_1)
    data_1 = np.squeeze(data_1)
    data_2 = fits.getdata(filename=filename_2)
    data_2 = np.squeeze(data_2)

    data_median = np.median(
        a=np.stack(arrays=(data_1, data_2), axis=0),
        axis=0
    )

    for i in range(data_median.shape[0]):

        figure, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 6))

        vmin = np.min([np.nanmin(data_1[i, ...]), np.nanmin(data_2[i, ...])])
        vmax = np.min([np.nanmax(data_1[i, ...]), np.nanmax(data_2[i, ...])])

        axes[0].imshow(
            data_1[i, ...], cmap="jet", origin="lower", vmin=vmin, vmax=vmax)
        axes[1].imshow(
            data_2[i, ...], cmap="jet", origin="lower", vmin=vmin, vmax=vmax)
        axes[2].imshow(
            data_median[i, ...], cmap="jet", origin="lower", vmin=vmin, vmax=vmax)

        for j in range(axes.shape[0]):
            axes[j].set_xticks([])
            axes[j].set_yticks([])

        plt.subplots_adjust(wspace=0.0, left=0.01, right=0.99, bottom=0.01, top=0.99)
        plt.show()
