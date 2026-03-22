import numpy as np


# Features that actually relate to mixing decisions
MIX_FEATURES = [
    "RMS Loudness",
    "LUFS",
    "Crest Factor",
    "Dynamic Range",
    "Compression Ratio",
    "Spectral Centroid",
    "Spectral Bandwidth",
    "Spectral Rolloff",
    "Stereo Width",
    "Sub Bass Energy",
    "Low/Mid Ratio",
    "Mid/High Ratio",
    "Transient Density",
    "Onset Strength Mean"
]


# Simulated mix moves
MIX_MOVES = {

    "brighten_mix": {
        "Spectral Centroid": 1.12,
        "Spectral Bandwidth": 1.08,
        "Spectral Rolloff": 1.10,
        "Mid/High Ratio": 1.10
    },

    "add_low_end": {
        "Sub Bass Energy": 1.20,
        "Low/Mid Ratio": 1.15
    },

    "widen_stereo": {
        "Stereo Width": 1.25
    },

    "increase_compression": {
        "Dynamic Range": 0.85,
        "Crest Factor": 0.90
    },

    "add_punch": {
        "Transient Density": 1.20,
        "Onset Strength Mean": 1.10
    },

    "reduce_mud": {
        "Low/Mid Ratio": 0.90,
        "Spectral Centroid": 1.05
    }

}


# Apply simulated move
def simulate_move(user_vector, feature_names, move):

    vector = user_vector.copy()

    index_map = {name: i for i, name in enumerate(feature_names)}

    for feature, multiplier in MIX_MOVES[move].items():

        if feature in index_map:

            idx = index_map[feature]

            vector[idx] *= multiplier

    return vector


# Evaluate improvement relative to reference mix
def evaluate_move(user_vector, simulated_vector, reference_mean, feature_names):

    index_map = {f: i for i, f in enumerate(feature_names)}

    indices = [index_map[f] for f in MIX_FEATURES if f in index_map]

    user = user_vector[indices]
    sim = simulated_vector[indices]
    ref = reference_mean[indices]

    original_dist = np.linalg.norm(user - ref)
    new_dist = np.linalg.norm(sim - ref)

    improvement = (original_dist - new_dist) / (original_dist + 1e-8) * 100

    return improvement


# Prevent unrealistic moves
def move_is_valid(move, user_vector, reference_mean, index_map):

    if move == "brighten_mix":

        idx = index_map["Spectral Centroid"]
        return user_vector[idx] < reference_mean[idx]

    if move == "add_low_end":

        idx = index_map["Sub Bass Energy"]
        return user_vector[idx] < reference_mean[idx]

    if move == "widen_stereo":

        idx = index_map["Stereo Width"]
        return user_vector[idx] < reference_mean[idx]

    if move == "increase_compression":

        idx = index_map["Dynamic Range"]
        return user_vector[idx] > reference_mean[idx]

    if move == "add_punch":

        idx = index_map["Transient Density"]
        return user_vector[idx] < reference_mean[idx]

    if move == "reduce_mud":

        idx = index_map["Low/Mid Ratio"]
        return user_vector[idx] > reference_mean[idx]

    return True


# Run full simulation
def run_mix_simulations(user_vector, feature_names, reference_mean):

    results = {}

    index_map = {f: i for i, f in enumerate(feature_names)}

    for move in MIX_MOVES:

        if not move_is_valid(move, user_vector, reference_mean, index_map):

            results[move] = None
            continue

        simulated = simulate_move(user_vector, feature_names, move)

        impact = evaluate_move(
            user_vector,
            simulated,
            reference_mean,
            feature_names
        )

        results[move] = round(float(impact), 2)

    return results