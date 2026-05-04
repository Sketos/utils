"""Helpers for reading and manipulating FITS headers and image products."""

import copy
import os
import tempfile
import warnings
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as au
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS


DEFAULT_2D_HEADER_KEYS = [
    "BMAJ",
    "BMIN",
    "BPA",
    "PC1_1",
    "PC2_1",
    "PC1_2",
    "PC2_2",
    "CTYPE1",
    "CRVAL1",
    "CDELT1",
    "CRPIX1",
    "CUNIT1",
    "CTYPE2",
    "CRVAL2",
    "CDELT2",
    "CRPIX2",
    "CUNIT2",
]

SANITIZE_FITS_KEYS = list(DEFAULT_2D_HEADER_KEYS)

SANITIZE_FITS_WITH_SCALING_KEYS = [
    "BSCALE",
    "BZERO",
    "BUNIT",
    "RADESYS",
    "SPECSYS",
    "OBSRA",
    "OBSDEC",
    "OBSGEO-X",
    "OBSGEO-Y",
    "OBSGEO-Z",
] + SANITIZE_FITS_KEYS

DEFAULT_TEST_FITS_FILENAME = (
    "member.uid___A001_X1465_X2ef7.SPT2147-50_sci.spw21_23_25_27.cont.I.pbcor.fits"
)


def _extract_required_keys(header, keys):
    """Return a dict of required header values or raise if any are missing."""
    missing_keys = [key for key in keys if key not in header]
    if missing_keys:
        missing_keys_str = ", ".join(missing_keys)
        raise ValueError(f"Missing required FITS header keys: {missing_keys_str}")
    return {key: header[key] for key in keys}


def _convert_deg_value(value, units):
    """Convert a scalar expressed in degrees into the requested angular units."""
    if units == "deg":
        return value
    if units == "arcsec":
        return value * au.deg.to(au.arcsec)
    raise NotImplementedError(f"Unsupported units: {units}")


def cutout(
    hdu,
    xmin=None,
    xmax=None,
    ymin=None,
    ymax=None,
    return_products=False,
    filename=None
):
    """Extract a rectangular image cutout and shift CRPIX to the new origin."""
    header = hdu.header
    required_keys = _extract_required_keys(
        header,
        ["CRVAL1", "CRVAL2", "CRPIX1", "CRPIX2"],
    )
    CRPIX1 = required_keys["CRPIX1"]
    CRPIX2 = required_keys["CRPIX2"]
    header_cutout = copy.deepcopy(header)
    data = hdu.data
    data_cutout = data[ymin:ymax, xmin:xmax]

    CRPIX1_cutout = CRPIX1 - xmin
    CRPIX2_cutout = CRPIX2 - ymin
    header_cutout["CRPIX1"] = CRPIX1_cutout
    header_cutout["CRPIX2"] = CRPIX2_cutout

    if return_products:
        return data_cutout, header_cutout, ymin, ymax, xmin, xmax
    return data_cutout, header_cutout


def angle_from_header(header):
    """Return the image rotation angle inferred from PC or CD matrix terms."""
    if np.logical_and("PC1_1" in header, "PC1_2" in header):
        PC1_2 = header["PC1_2"]
        PC1_1 = header["PC1_1"]
        angle = np.degrees(np.arctan2(PC1_2, PC1_1))
    elif np.logical_and("CD1_1" in header, "CD1_2" in header):
        CD1_1 = header["CD1_1"]
        CD1_2 = header["CD1_2"]
        angle = np.degrees(np.arctan2(CD1_2, CD1_1))
    else:
        raise ValueError("Header does not contain a supported rotation matrix.")
    return angle

def get_beam_from_header(header, units="arcsec"):
    """Compute the beam area from `BMAJ` and `BMIN` header keywords."""
    beam = _extract_required_keys(header, ["BMAJ", "BMIN"])
    beam_x = _convert_deg_value(beam["BMAJ"], units)
    beam_y = _convert_deg_value(beam["BMIN"], units)
    return np.pi * (beam_x * beam_y)

def get_beam_from_fits(filename, ext=0, units="arcsec"):
    """Load a header from disk and compute its beam area."""
    header = fits.getheader(filename=filename, ext=ext)
    return get_beam_from_header(header=header, units=units)

def get_pixel_scale_from_header(header, units="deg"):
    """Infer a representative pixel scale from common FITS WCS keywords."""
    if all([
        key in header
        for key in [
            "CD1_1",
            "CD1_2",
            "CD2_1",
            "CD2_2"
        ]
    ]):
        _arg = np.arctan(
            header["CD2_1"] / header["CD1_1"]
        )
        pixel_scale_x = abs(header["CD1_1"] / np.cos(_arg))
        pixel_scale_y = abs(header["CD2_2"] / np.cos(_arg))
    elif all([
        key in header
        for key in [
            "CDELT1",
            "CDELT2"
        ]
    ]):
        pixel_scale_x = abs(header["CDELT1"])
        pixel_scale_y = abs(header["CDELT2"])
    elif all([
        key in header
        for key in [
            "PC1_1",
            "PC1_2",
            "PC2_1",
            "PC2_2"
        ]
    ]):
        arg = np.arctan(
            header["PC2_1"] / header["PC1_1"]
        )
        pixel_scale_x = abs(header["PC1_1"] / np.cos(arg))
        pixel_scale_y = abs(header["PC2_2"] / np.cos(arg))
    else:
        raise ValueError("Header does not contain a supported pixel scale definition.")

    pixel_scale = np.sqrt(pixel_scale_x * pixel_scale_y)
    return _convert_deg_value(pixel_scale, units)


def get_pixel_scale_from_fits(filename, ext=0, units="arcsec"):
    """Load a header from disk and return its inferred pixel scale."""
    header = fits.getheader(filename=filename, ext=ext)
    return get_pixel_scale_from_header(header=header, units=units)


def extract_key_from_header(header, key):
    """Return one header value, raising if the requested key is missing."""
    if key in header:
        return header[key]
    raise ValueError(f"{key} was not found in the header")


def extract_key_from_fits(filename, key):
    """Load a FITS header and return one key from it."""
    header = fits.getheader(filename=filename)
    return extract_key_from_header(header=header, key=key)

def extract_list_of_keys_from_header(header, list_of_keys, error=False):
    """Return a dict containing a selected subset of header keys."""
    if not isinstance(list_of_keys, list):
        raise TypeError("It is not a list")
    if not list_of_keys:
        raise ValueError("The list is empty")

    header_keys = {}
    for key in list_of_keys:
        if key in header:
            header_keys[key] = header[key]
            continue
        if error:
            raise ValueError(f"{key} was not found in the header")
        warnings.warn(f"{key} was not found in the header", stacklevel=2)

    return header_keys

def remove_keys_from_header(header, list_of_keys):
    """Create a new header containing every key except the excluded ones."""
    header_keys = {key: header[key] for key in header if key not in list_of_keys}

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys
    )

def header_from_header_and_list_of_keys(header, list_of_keys):
    """Build a new header containing only the requested keys."""

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys
    )

def filter_header(header, list_of_keys):
    """Alias for selecting a subset of keys into a fresh header."""

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=list_of_keys
    )

    return updated_header_with_header_keys(
        header=fits.Header(), header_keys=header_keys
    )

def updated_header_with_header_keys(header, header_keys, replace=False):
    """Merge key/value pairs into a header, optionally replacing existing keys."""
    header = copy.copy(header)

    if header_keys is None:
        return header

    for key in header_keys:
        if replace or key not in header:
            header[key] = header_keys[key]

    return header

def updated_header_with_header_keys_from_filename(filename, header_keys, replace=False):
    """Write header updates back into an existing FITS file on disk."""
    header = fits.getheader(filename=filename)
    header = updated_header_with_header_keys(
        header=header,
        header_keys=header_keys,
        replace=replace,
    )

    data = fits.getdata(filename=filename)

    fits.writeto(
        filename,
        data=data,
        header=header,
        overwrite=True
    )

def get_extent_from_header(header):
    """Return a matplotlib-style extent list derived from image size and scale."""
    pixel_scale = get_pixel_scale_from_header(header=header)

    extent = [
        0,
        header["NAXIS2"] * pixel_scale,
        0,
        header["NAXIS1"] * pixel_scale
    ]

    return extent

def extract_keys_from_header_for_2d(header):
    """Extract the module's standard 2D beam and WCS header subset."""
    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=DEFAULT_2D_HEADER_KEYS
    )

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )

def default_list_of_keys():
    """Return the default 2D FITS header keys used throughout this module."""
    return list(DEFAULT_2D_HEADER_KEYS)

def header_from_header_and_default_list_of_keys(header):
    """Build a new header using the module's default 2D key selection."""

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=default_list_of_keys()
    )

    return updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys
    )

def sanitize_fits(filename, output_filename, flipped=False):
    """Write a simplified FITS file with squeezed data and core 2D WCS keys."""
    data = fits.getdata(filename=filename)

    header_keys = extract_list_of_keys_from_header(
        header=fits.getheader(filename=filename),
        list_of_keys=SANITIZE_FITS_KEYS
    )

    header = updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )

    data = np.squeeze(a=data)
    if flipped:
        data = data[::-1]
    fits.writeto(
        filename=output_filename,
        data=np.squeeze(a=data),
        header=header,
        overwrite=True
    )


def sanitize_fits_with_scaling(filename, output_filename, scaling_factor=1.0, flipped=False):
    """Write a simplified FITS file after multiplying the data by a scale factor."""
    data = fits.getdata(filename=filename)
    data *= scaling_factor

    header = fits.getheader(filename=filename)

    header_keys = extract_list_of_keys_from_header(
        header=header, list_of_keys=SANITIZE_FITS_WITH_SCALING_KEYS
    )
    header = updated_header_with_header_keys(
        header=fits.Header(),
        header_keys=header_keys,
        replace=False
    )

    data = np.squeeze(a=data)
    if flipped:
        data = data[::-1]
    fits.writeto(
        filename=output_filename,
        data=np.squeeze(
            a=data
        ),
        header=header,
        overwrite=True
    )

# def save_cube_to_fits(
#     CRVAL1,
#     CDELT1,
#     CRPIX1,
#     CRVAL2,
#     CDELT2,
#     CRPIX2,
#     data,
#     directory=None,
#     filename="cube"
# ):
#
#     if len(data.shape) == 3:
#         pass
#     else:
#         raise ValueError
#
#     header = fits.Header()
#     header["CTYPE1"] = "RA---SIN"
#     header["CRVAL1"] = CRVAL1
#     header["CDELT1"] = CDELT1
#     header["CRPIX1"] = CRPIX1
#     header["CUNIT1"] = "deg"
#     header["CTYPE2"] = "DEC--SIN"
#     header["CRVAL2"] = CRVAL2
#     header["CDELT2"] = CDELT2
#     header["CRPIX2"] = CRPIX2
#     header["CUNIT2"] = "deg"
#
#     # # ...
#     # if directory is None:
#     #     filename = "cube.fits"
#     # else:
#     #     if directory[-1] == "/":
#     #         directory = directory[:-1]
#     #     filename = directory + "/cube.fits"
#
#     if directory:
#         # TODO: check if directory exists.
#
#         if directory[-1] == "/":
#             directory = directory[:-1]
#     else:
#         directory = "."
#
#     filename = directory + "/" + filename + ".fits"
#
#     fits.writeto(
#         filename,
#         data=data,
#         header=header,
#         overwrite=True
#     )


def get_wavelengths_from_header(header):
    """Construct the third-axis coordinate array from spectral header keywords."""
    spectral_keys = _extract_required_keys(
        header,
        ["NAXIS3", "CRVAL3", "CDELT3", "CRPIX3"],
    )
    return spectral_keys["CRVAL3"] + np.arange(spectral_keys["NAXIS3"]) * spectral_keys["CDELT3"]


def get_frequencies_from_fits(filename, units=au.Hz):
    """Load a FITS header and return its spectral axis as frequencies."""
    header = fits.getheader(filename=filename)
    return get_frequencies_from_header(header=header, units=units)

def get_frequencies_from_filename(filename, units=au.Hz):
    """Compatibility wrapper around `get_frequencies_from_fits`."""
    return get_frequencies_from_fits(filename=filename, units=units)

def get_frequencies_from_header(header, units=au.Hz):
    """Construct a frequency axis from third-axis FITS WCS metadata."""
    spectral_keys = _extract_required_keys(
        header,
        ["NAXIS3", "CRVAL3", "CDELT3", "CRPIX3", "CUNIT3"],
    )

    frequencies = (
        spectral_keys["CRVAL3"]
        + np.arange(spectral_keys["NAXIS3"]) * spectral_keys["CDELT3"]
    )
    if spectral_keys["CUNIT3"] != "Hz":
        raise NotImplementedError(
            f"Unsupported spectral axis unit: {spectral_keys['CUNIT3']}"
        )

    return (frequencies * au.Hz).to(units)


def convert_coords(coords, frame):
    """Convert an FK5 coordinate pair into another Astropy coordinate frame."""
    skycoords = SkyCoord(coords[0], coords[1], frame="fk5")
    return skycoords.transform_to(frame)

def recenter(x, y, radius, header, filename=None):
    """Convert a sky position and angular radius into pixel cutout bounds."""
    wcs = WCS(header)

    xpix, ypix = wcs.wcs_world2pix(x, y, 0)
    pixel_scale = get_pixel_scale_from_header(header=header)

    radius = radius.to(au.deg).value

    if radius:
        dx_pix = radius / pixel_scale
        dy_pix = radius / pixel_scale

    xmin = xpix - dx_pix
    xmax = xpix + dx_pix
    ymin = ypix - dy_pix
    ymax = ypix + dy_pix

    return xmin, xmax, ymin, ymax

def recenter_from_image(filename_i, filename_j):
    """Plot and return a cutout from one image aligned to another image's center."""

    hdu_i = fits.open(filename_i)
    hdu_j = fits.open(filename_j)

    pixel_scale_i = get_pixel_scale_from_fits(
        filename=filename_i
    )
    pixel_scale_j = get_pixel_scale_from_fits(
        filename=filename_j
    )


    keys = extract_list_of_keys_from_header(
        header=hdu_i[0].header,
        list_of_keys=[
            "NAXIS1",
            "CRVAL1",
            "CRPIX1",
            "NAXIS2",
            "CRVAL2",
            "CRPIX2",
        ],
        error=False
    )

    center = SkyCoord(
        keys["CRVAL1"] * au.deg,
        keys["CRVAL2"] * au.deg,
        frame='icrs'
    )

    radius = keys["NAXIS1"] * pixel_scale_i / 2.0 * au.arcsec

    extent_i = [
        0.0,
        keys["NAXIS1"] * pixel_scale_i,
        0.0,
        keys["NAXIS1"] * pixel_scale_i
    ]

    xmin, xmax, ymin, ymax = recenter(
        x=center.ra,
        y=center.dec,
        radius=radius,
        header=hdu_j[0].header
    )
    xmin = int(np.round(xmin))
    xmax = int(np.round(xmax))
    ymin = int(np.round(ymin))
    ymax = int(np.round(ymax))

    image_i = fits.getdata(filename=filename_i)
    image_j = fits.getdata(filename=filename_j)
    image_i = np.squeeze(image_i)
    image_j = np.squeeze(image_j)

    image_j_recentered = image_j[ymin:ymax, xmin:xmax]

    figure, axes = plt.subplots(nrows=1, ncols=2)


    extent_j = [
        0.0,
        image_j_recentered.shape[0] * pixel_scale_j,
        0.0,
        image_j_recentered.shape[1] * pixel_scale_j,
    ]

    axes[0].imshow(image_j_recentered, cmap="jet", vmin=-0.005, vmax=0.5, origin="lower", extent=extent_j)
    axes[1].imshow(image_i, cmap="jet", origin="lower", extent=extent_i)
    axes[0].contour(image_i, colors="black", extent=extent_i)
    axes[1].contour(image_i, colors="black", extent=extent_i)

    plt.show()
    return image_j_recentered, extent_j


def save_image_with_extent(image, extent):
    """Placeholder for writing an image together with a plotting extent."""
    raise NotImplementedError("save_image_with_extent is not implemented.")


def _get_default_test_filename(filename=None):
    """Return the requested test FITS filename or the module's default sample."""
    if filename is not None:
        return filename
    return DEFAULT_TEST_FITS_FILENAME


def _get_sample_header_and_data(filename=None):
    """Load the default sample FITS file and return its header and squeezed data."""
    filename = _get_default_test_filename(filename)
    header = fits.getheader(filename=filename)
    data = np.squeeze(fits.getdata(filename=filename))
    return filename, header, data


def _assert(condition, message):
    """Raise an AssertionError with a friendlier message for manual tests."""
    if not condition:
        raise AssertionError(message)

# ----------------------- #
#
# ----------------------- #

def test__sample_file_exists(filename=None):
    """Verify that the default sample FITS file is present on disk."""
    filename = _get_default_test_filename(filename)
    _assert(os.path.exists(filename), f"Test FITS file was not found: {filename}")
    return filename


def test__get_pixel_scale_from_fits(filename=None):
    """Check that pixel-scale extraction succeeds for the sample FITS file."""
    filename = test__sample_file_exists(filename)
    pixel_scale = get_pixel_scale_from_fits(filename=filename, ext=0, units="arcsec")
    _assert(np.isfinite(pixel_scale), "Pixel scale should be finite.")
    _assert(pixel_scale > 0.0, "Pixel scale should be positive.")
    return pixel_scale


def test__beam_helpers(filename=None):
    """Check that beam extraction works from both a header and a FITS file."""
    filename, header, _ = _get_sample_header_and_data(filename)
    beam_from_header = get_beam_from_header(header=header, units="arcsec")
    beam_from_fits = get_beam_from_fits(filename=filename, units="arcsec")
    _assert(np.isfinite(beam_from_header), "Beam area from header should be finite.")
    _assert(beam_from_header > 0.0, "Beam area should be positive.")
    _assert(np.isclose(beam_from_header, beam_from_fits), "Beam helpers should agree.")
    return beam_from_header


def test__extract_key_helpers(filename=None):
    """Check single-key extraction from both a header and a FITS file."""
    filename, header, _ = _get_sample_header_and_data(filename)
    object_from_header = extract_key_from_header(header=header, key="OBJECT")
    object_from_fits = extract_key_from_fits(filename=filename, key="OBJECT")
    _assert(object_from_header == "SPT2147-50", "Unexpected OBJECT value in header.")
    _assert(object_from_header == object_from_fits, "Key extractors should agree.")
    return object_from_header


def test__extract_list_of_keys_from_header(filename=None):
    """Check multi-key extraction for the sample FITS header."""
    _, header, _ = _get_sample_header_and_data(filename)
    header_keys = extract_list_of_keys_from_header(
        header=header,
        list_of_keys=["CTYPE3", "CRVAL3", "CDELT3", "CRPIX3", "CUNIT3"],
        error=True,
    )
    _assert(header_keys["CTYPE3"].strip() == "FREQ", "Expected a FREQ third axis.")
    _assert(header_keys["CUNIT3"].strip() == "Hz", "Expected the spectral axis in Hz.")
    return header_keys


def test__header_subset_helpers(filename=None):
    """Check the helpers that create filtered header copies."""
    _, header, _ = _get_sample_header_and_data(filename)
    subset = header_from_header_and_list_of_keys(header, ["OBJECT", "BUNIT"])
    filtered = filter_header(header, ["OBJECT", "BUNIT"])
    default_header = header_from_header_and_default_list_of_keys(header)
    reduced = remove_keys_from_header(header, ["OBJECT"])

    _assert(subset["OBJECT"] == "SPT2147-50", "Subset header should keep OBJECT.")
    _assert(filtered["BUNIT"].strip() == "Jy/beam", "Filtered header should keep BUNIT.")
    _assert("BMAJ" in default_header, "Default header selection should keep beam info.")
    _assert("OBJECT" not in reduced, "Removed header should not include OBJECT.")
    return {
        "subset": subset,
        "filtered": filtered,
        "default_header": default_header,
        "reduced": reduced,
    }


def test__header_update_helpers(filename=None):
    """Check header-update helpers in memory and on a temporary FITS copy."""
    filename, header, _ = _get_sample_header_and_data(filename)
    updated = updated_header_with_header_keys(
        header=header,
        header_keys={"TESTKEY": 42},
        replace=False,
    )
    _assert(updated["TESTKEY"] == 42, "Header update should add TESTKEY in memory.")

    with tempfile.NamedTemporaryFile(suffix=".fits", delete=False) as temp_file:
        temp_filename = temp_file.name

    try:
        fits.writeto(
            temp_filename,
            data=fits.getdata(filename=filename),
            header=header,
            overwrite=True,
        )
        updated_header_with_header_keys_from_filename(
            filename=temp_filename,
            header_keys={"TESTKEY": 99},
            replace=True,
        )
        temp_header = fits.getheader(temp_filename)
        _assert(temp_header["TESTKEY"] == 99, "On-disk header update should persist TESTKEY.")
        return temp_header
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)


def test__extent_and_angle_helpers(filename=None):
    """Check extent and rotation-angle extraction for the sample FITS header."""
    _, header, _ = _get_sample_header_and_data(filename)
    extent = get_extent_from_header(header)
    angle = angle_from_header(header)
    _assert(len(extent) == 4, "Extent should contain four values.")
    _assert(extent[1] > 0.0 and extent[3] > 0.0, "Extent should be positive.")
    _assert(np.isclose(angle, 0.0), "Sample image should have zero rotation.")
    return extent, angle


def test__2d_header_helpers(filename=None):
    """Check the 2D header extraction helpers used by imaging workflows."""
    _, header, _ = _get_sample_header_and_data(filename)
    header_2d = extract_keys_from_header_for_2d(header)
    aplpy_keys = get_list_of_keys_for_aplpy(header)
    _assert("BMAJ" in header_2d, "2D header extraction should preserve BMAJ.")
    _assert(aplpy_keys["CTYPE1"].strip() == "RA---SIN", "APLpy keys should preserve axis types.")
    return header_2d, aplpy_keys


def test__cutout_helper(filename=None):
    """Check that the 2D cutout helper slices data and updates CRPIX correctly."""
    _, header, data = _get_sample_header_and_data(filename)
    hdu = fits.PrimaryHDU(data=data, header=header)
    data_cutout, header_cutout = cutout(
        hdu=hdu,
        xmin=100,
        xmax=140,
        ymin=200,
        ymax=260,
    )
    _assert(data_cutout.shape == (60, 40), "Cutout shape should match the requested bounds.")
    _assert(np.isclose(header_cutout["CRPIX1"], header["CRPIX1"] - 100), "CRPIX1 should shift with xmin.")
    _assert(np.isclose(header_cutout["CRPIX2"], header["CRPIX2"] - 200), "CRPIX2 should shift with ymin.")
    return data_cutout, header_cutout


def test__coordinate_helpers(filename=None):
    """Check coordinate conversion and recentering against the sample FITS WCS."""
    _, header, _ = _get_sample_header_and_data(filename)
    icrs_coords = convert_coords((header["CRVAL1"] * au.deg, header["CRVAL2"] * au.deg), "icrs")
    xmin, xmax, ymin, ymax = recenter(
        x=header["CRVAL1"] * au.deg,
        y=header["CRVAL2"] * au.deg,
        radius=1.0 * au.arcsec,
        header=header,
    )
    _assert(icrs_coords.frame.name == "icrs", "Coordinate conversion should return the requested frame.")
    _assert(xmin < xmax and ymin < ymax, "Recentering should return ordered pixel bounds.")
    return icrs_coords, (xmin, xmax, ymin, ymax)


def test__sanitize_helpers(filename=None):
    """Check that the sanitize helpers produce writable FITS outputs."""
    filename = _get_default_test_filename(filename)

    with tempfile.NamedTemporaryFile(suffix=".fits", delete=False) as temp_one:
        output_one = temp_one.name
    with tempfile.NamedTemporaryFile(suffix=".fits", delete=False) as temp_two:
        output_two = temp_two.name

    try:
        sanitize_fits(filename=filename, output_filename=output_one, flipped=False)
        sanitize_fits_with_scaling(
            filename=filename,
            output_filename=output_two,
            scaling_factor=2.0,
            flipped=False,
        )

        data_one = np.squeeze(fits.getdata(output_one))
        data_two = np.squeeze(fits.getdata(output_two))
        _assert(data_one.shape == (1536, 1536), "Sanitized FITS should be squeezed to a 2D image.")
        _assert(data_two.shape == (1536, 1536), "Scaled sanitized FITS should be squeezed to a 2D image.")
        _assert(np.nanmax(np.abs(data_two)) >= np.nanmax(np.abs(data_one)), "Scaled output should not be smaller than the unscaled output.")
        return output_one, output_two
    finally:
        for temp_filename in [output_one, output_two]:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)


def get_list_of_keys_for_aplpy(header):
    """Return the header subset typically needed to build an APLpy figure."""

    list_of_keys = [
        "NAXIS1",
        "NAXIS2",
        "CRVAL1",
        "CDELT1",
        "CRPIX1",
        "CTYPE1",
        "CUNIT1",
        "CRVAL2",
        "CDELT2",
        "CRPIX2",
        "CTYPE2",
        "CUNIT2",
        # "PC1_1",
        # "PC2_1",
        # "PC1_2",
        # "PC2_2",
    ]


    return extract_list_of_keys_from_header(
        header=header,
        list_of_keys=list_of_keys
    )

# ----------------------- #
#
# ----------------------- #

def run_tests():
    """Run the manual smoke tests against the default sample FITS file."""
    test_functions = [
        test__sample_file_exists,
        test__get_pixel_scale_from_fits,
        test__beam_helpers,
        test__extract_key_helpers,
        test__extract_list_of_keys_from_header,
        test__header_subset_helpers,
        test__header_update_helpers,
        test__extent_and_angle_helpers,
        test__2d_header_helpers,
        test__cutout_helper,
        test__coordinate_helpers,
        test__sanitize_helpers,
    ]

    results = []
    filename = _get_default_test_filename()
    print(f"Running fits_utils tests with {filename}")

    for test_function in test_functions:
        test_name = test_function.__name__
        try:
            test_function(filename=filename)
        except Exception as error:
            print(f"FAIL: {test_name}: {error}")
            results.append((test_name, False, str(error)))
        else:
            print(f"PASS: {test_name}")
            results.append((test_name, True, ""))

    passed = sum(result[1] for result in results)
    failed = len(results) - passed
    print(f"Summary: {passed} passed, {failed} failed")

    if failed:
        raise RuntimeError("One or more fits_utils tests failed.")

    return results


def func():
    """Placeholder function kept for compatibility with older callers."""
    pass


if __name__ == "__main__":
    run_tests()
