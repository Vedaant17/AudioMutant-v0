import numpy as np

def compute_spectral_tilt(stft, freqs):

    spectrum = np.mean(stft, axis=1)

    mask = freqs > 50

    freqs = freqs[mask]
    spectrum = spectrum[mask]

    log_freq = np.log(freqs)
    log_mag = np.log(spectrum + 1e-10)

    slope = np.polyfit(log_freq, log_mag, 1)[0]

    return float(slope)

def classify_tilt(slope):

    if slope > 0.05:
        return "Bright Mix"

    elif slope < -0.05:
        return "Dark Mix"

    else:
        return "Balanced Mix"