import numpy as np
from astropy import units as au

# NOTE: THIS ONLY WORKS WHEN THE NUMBER OF CHANNELS IS EVEN NUMBER.
def generate_frequencies(central_frequency, n_channels, bandwidth):

    df = (bandwidth / n_channels).to(au.Hz).value

    frequencies = np.arange(
        central_frequency.to(au.Hz).value - int(n_channels / 2.0) * df,
        central_frequency.to(au.Hz).value + int(n_channels / 2.0) * df,
        df
    )

    return frequencies
