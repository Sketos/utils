import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# NOTE:
if os.environ.get("CONDA_DEFAULT_ENV") == "default":
    import stpsf   
else:
    print("stpsf is not installed")

# 
def get_nircam_psf_from_filter(
    filter="F444W"
):
    obj = stpsf.NIRCam()
    obj.filter = filter
    psf = obj.calc_psf(oversample=1)
    
    return psf[-1]

if __name__ == "__main__":
    for filter in [
        "F200W",
        "F356W",
        "F444W",
    ]:
        filename = "./psf_nircam_{}.fits".format(filter)
        if os.path.isfile(filename):
            print(
                "The filename, \'{}\', already exists.".format(filename)
            )
        else:
            psf = get_nircam_psf_from_filter(
                filter=filter
            )
            # plt.figure()
            # print(
            #     "pixel_scale =", psf.header["PIXELSCL"]
            # )
            # plt.imshow(
            #     np.log10(psf.data), cmap="jet",
            # )
            # plt.show();exit()
            fits.writeto(
                "./psf_nircam_{}.fits".format(filter), 
                data=psf.data, 
                header=psf.header,
                overwrite=False
            )