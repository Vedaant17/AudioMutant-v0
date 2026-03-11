import numpy as np

def build_feature_vector(features):

    vector = []

    vector.append(features.get("tempo_bpm", 0) * 2)
    vector.append(features.get("tempo_stability", 0))
    vector.append(features.get("onset_strength_mean", 0))
    vector.append(features.get("onset_strength_std", 0))

    # Spectral features
    vector.append(features.get("spectral_centroid", 0))
    vector.append(features.get("spectral_bandwidth", 0))
    vector.append(features.get("spectral_rolloff", 0))
    

    # Loudness
    vector.append(features.get("loudness_rms", 0))
    vector.append(features.get("dynamic_range", 0))
    vector.append(features.get("crest_factor", 0) * 0.5)
    vector.append(features.get("LUFS", 0) * 0.7)

    # Mix features
    vector.append(features.get("stereo_width", 0) * 0.5)
    vector.append(features.get("sub_bass_energy", 0) * 0.7)
    vector.append(features.get("transient_density", 0))
    vector.append(features.get("silence_ratio", 0) * 0.3)

    # Frequency balance
    freq = features.get("frequency_balance", {})
    vector.append(freq.get("low", 0))
    vector.append(freq.get("mid", 0))
    vector.append(freq.get("high", 0))

    # MFCC
    mfcc_mean = features.get("mfcc_mean", [0]*13)
    mfcc_std = features.get("mfcc_std", [0]*13)

    vector.extend([m * 3 for m in mfcc_mean])
    vector.extend([s * 3 for s in mfcc_std])

    # Spectral contrast
    vector.extend(features["spectral_contrast_mean"])
    vector.extend(features["spectral_contrast_std"])
    vector.append(features.get("spectral_flatness_mean", 0))
    vector.append(features.get("spectral_flatness_std", 0))

    return np.array(vector, dtype=float)