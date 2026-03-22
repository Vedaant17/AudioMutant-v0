from engine.feature_names import FEATURE_NAMES

NUM_FEATURES = len(FEATURE_NAMES)

def build_weight_vector(feature_boosts):

    weights = [1.0] * NUM_FEATURES

    for feature, value in feature_boosts.items():

        idx = FEATURE_NAMES.index(feature)
        weights[idx] = value

    return weights


GENRE_WEIGHTS = {

    "edm": build_weight_vector({
        "Tempo": 2.0,
        "Beat Strength": 2.0,
        "Percussive Energy": 2.0,
        "Transient Density": 1.8
    }),

    "hiphop": build_weight_vector({
        "Sub Bass Energy": 2.5,
        "Low/Mid Ratio": 2.0,
        "Beat Strength": 1.8,
        "Percussive Energy": 1.6
    }),

    "pop": build_weight_vector({
        "Stereo Width": 2.0,
        "Spectral Centroid": 1.8,
        "Beat Strength": 1.5
    }),

    "rock": build_weight_vector({
        "Harmonic Energy": 2.2,
        "Dynamic Range": 1.8,
        "Spectral Bandwidth": 1.5
    })

}