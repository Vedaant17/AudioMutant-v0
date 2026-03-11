import numpy as np

def build_feature_vector(features):

    vector = []

    # -------- TEMPO --------
    vector.append(features["tempo_bpm"])
    vector.append(features["tempo_stability"])

    # -------- ENERGY --------
    vector.append(features["harmonic_energy"])
    vector.append(features["percussive_energy"])
    vector.append(features["harmonic_percussive_ratio"])

    # -------- LOUDNESS --------
    vector.append(features["loudness_rms"])
    vector.append(features["LUFS"])
    vector.append(features["crest_factor"])
    vector.append(features["dynamic_range"])
    vector.append(features["compression_ratio"])

    # -------- SPECTRAL --------
    vector.append(features["spectral_centroid"])
    vector.append(features["spectral_bandwidth"])
    vector.append(features["spectral_rolloff"])
    vector.append(features["spectral_flatness_mean"])
    vector.append(features["spectral_flatness_std"])
    vector.append(features["zero_crossing_rate"])

    # -------- FLUX --------
    vector.append(features["spectral_flux_mean"])
    vector.append(features["spectral_flux_std"])

    # -------- MIX --------
    vector.append(features["stereo_width"])
    vector.append(features["sub_bass_energy"])

    # -------- FREQUENCY BALANCE --------
    vector.append(features["low_mid_ratio"])
    vector.append(features["mid_high_ratio"])

    # -------- RHYTHM --------
    vector.append(features["transient_density"])
    vector.append(features["beat_strength"])
    vector.append(features["onset_strength_mean"])
    vector.append(features["onset_strength_std"])

    # -------- SILENCE --------
    vector.append(features["silence_ratio"])

    # -------- MFCC --------
    vector.extend(features["mfcc_mean"])
    vector.extend(features["mfcc_std"])

    # -------- CHROMA --------
    vector.extend(features["chroma_mean"])
    vector.extend(features["chroma_std"])

    # -------- SPECTRAL CONTRAST --------
    vector.extend(features["spectral_contrast_mean"])
    vector.extend(features["spectral_contrast_std"])

    return np.array(vector, dtype=np.float32)