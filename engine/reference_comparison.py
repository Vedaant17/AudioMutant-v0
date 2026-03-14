import numpy as np

REFERENCE_FEATURES = [
"LUFS",
"dynamic_range",
"crest_factor",
"compression_ratio",
"stereo_width",
"spectral_centroid",
"spectral_bandwidth",
"sub_bass_energy",
"transient_density",
"beat_strength"
]


def get_reference_features(reference_library, closest_tracks):

    refs = []

    for sim, genre, idx in closest_tracks:

        track = reference_library[genre][idx]

        refs.append(track)

    return refs


def compute_reference_average(reference_tracks):

    avg = {}

    for feature in REFERENCE_FEATURES:

        values = [t[feature] for t in reference_tracks]

        avg[feature] = float(np.mean(values))

    avg["low"] = np.mean([t["frequency_balance"]["low"] for t in reference_tracks])
    avg["mid"] = np.mean([t["frequency_balance"]["mid"] for t in reference_tracks])
    avg["high"] = np.mean([t["frequency_balance"]["high"] for t in reference_tracks])

    return avg


def compare_mix(user_features, reference_avg):

    user = {
        "LUFS": user_features["LUFS"],
        "dynamic_range": user_features["dynamic_range"],
        "crest_factor": user_features["crest_factor"],
        "compression_ratio": user_features["compression_ratio"],
        "stereo_width": user_features["stereo_width"],
        "spectral_centroid": user_features["spectral_centroid"],
        "spectral_bandwidth": user_features["spectral_bandwidth"],
        "sub_bass_energy": user_features["sub_bass_energy"],
        "transient_density": user_features["transient_density"],
        "beat_strength": user_features["beat_strength"],
        "low": user_features["frequency_balance"]["low"],
        "mid": user_features["frequency_balance"]["mid"],
        "high": user_features["frequency_balance"]["high"]
    }

    differences = {}

    for key in user:

        differences[key] = user[key] - reference_avg[key]

    return differences


def interpret_differences(differences):

    interpretation = {}

    for feature, diff in differences.items():

        if diff > 0.15:
            interpretation[feature] = "higher than reference"

        elif diff < -0.15:
            interpretation[feature] = "lower than reference"

        else:
            interpretation[feature] = "similar to reference"

    return interpretation