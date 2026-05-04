import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

filename = "./PSFSTD_WFC3IR_F110W.fits"

header = fits.getheader(filename=filename)
print(header["PIXSCALE"])
# psf = fits.getdata(filename=filename)
# print(psf.shape)