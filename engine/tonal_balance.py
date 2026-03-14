import numpy as np

TONAL_BANDS = {
    "sub": (20, 60),
    "low": (60, 250),
    "low_mid": (250, 500),
    "mid": (500, 2000),
    "high_mid": (2000, 6000),
    "high": (6000, 20000)
}

def compute_tonal_balance(stft, freqs):

    band_energy = {}

    for band, (low, high) in TONAL_BANDS.items():

        mask = (freqs >= low) & (freqs < high)

        energy = np.mean(stft[mask])

        band_energy[band] = float(energy)

    return band_energy

def normalize_bands(band_energy):

    total = sum(band_energy.values())

    return {
        band: energy / (total + 1e-10)
        for band, energy in band_energy.items()
    }

def analyze_tonal_balance(user_bands, reference_bands):

    issues = []

    for band in user_bands:

        diff = user_bands[band] - reference_bands[band]

        if diff > 0.05:
            issues.append(f"Too much {band} energy")

        elif diff < -0.05:
            issues.append(f"Too little {band} energy")

    return issues