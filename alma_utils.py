
def pixel_scale_from_antenna_configuration_and_frequency(antenna_configuration, frequency):

    if antenna_configuration is None:
        raise ValueError
    elif antenna_configuration == "5.1":
        raise ValueError
    elif antenna_configuration == "5.2":
        raise ValueError
    elif antenna_configuration == "5.3":
        raise ValueError
    elif antenna_configuration == "5.4":
        #if frequency > value and frequency < value:
        pixel_scale = 0.05
    elif antenna_configuration == "5.5":
        raise ValueError
    elif antenna_configuration == "5.6":
        pixel_scale = 0.04
    elif antenna_configuration == "5.7":
        raise ValueError
    elif antenna_configuration == "5.8":
        pixel_scale = 0.01
    elif antenna_configuration == "5.9":
        raise ValueError
    elif antenna_configuration == "5.10":
        raise ValueError
    else:
        raise ValueError

    return pixel_scale


def compute_frequencies(central_frequency, n_channels, frequency_resolution):

    frequency_0 = compute_0_index_frequency(
        central_frequency=central_frequency,
        n_channels=n_channels,
        frequency_resolution=frequency_resolution
    )

    # TODO: 

def compute_0_index_frequency(central_frequency, n_channels, frequency_resolution):

    if (n_channels % 2) == 0:
        frequency_0 = central_frequency - n_channels / 2.0 * frequency_resolution
    else:
        frequency_0 = central_frequency - (n_channels - 1) / 2.0 * frequency_resolution

    return frequency_0
