import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from engine.vector_builder import build_feature_vector
from engine.feature_names import FEATURE_NAMES
from engine.genre_weights import GENRE_WEIGHTS

def load_reference_data(reference_folder="reference_data"):
    """
    Loads all reference JSON files and groups them by genre.

    Returns:
        reference_library (dict)
        {
            "pop": [track1_features, track2_features],
            "rock": [...],
        }
    """

    if not os.path.exists(reference_folder):
        raise FileNotFoundError(f"{reference_folder} not found")

    reference_library = {}

    for genre in os.listdir(reference_folder):

        genre_path = os.path.join(reference_folder, genre)

        if not os.path.isdir(genre_path):
            continue

        reference_library[genre] = []

        for file in os.listdir(genre_path):

            if not file.endswith(".json"):
                continue

            file_path = os.path.join(genre_path, file)

            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                features = data.get("features")

                if features is not None:
                    reference_library[genre].append(features)

            except json.JSONDecodeError:
                print(f"Skipping invalid JSON: {file_path}")

    return reference_library


def process_reference_library(reference_library):

    # Store vectors per genre
    genre_vectors = {}

    # Store all vectors together for global normalization
    all_vectors = []

    feature_means = {}
    feature_stds = {}

    # -----------------------------
    # Step 1: Build feature vectors
    # -----------------------------
    for genre, tracks in reference_library.items():

        genre_vectors[genre] = []

        for track_features in tracks:

            vector = build_feature_vector(track_features)

            genre_vectors[genre].append(vector)

            all_vectors.append(vector)
    
    # -----------------------------------------
    # Compute per-genre feature statistics
    # -----------------------------------------
    for genre, vectors in genre_vectors.items():

        matrix = np.array(vectors)

        feature_means[genre] = np.mean(matrix, axis=0)
        feature_stds[genre] = np.std(matrix, axis=0) + 1e-8

    # Convert to numpy matrix
    all_matrix = np.array(all_vectors)

    # ---------------------------------
    # Step 2: Compute global statistics
    # ---------------------------------
    global_mean = np.mean(all_matrix, axis=0)
    global_std = np.std(all_matrix, axis=0) + 1e-8

    # ----------------------------------------
    # Step 3: Normalize all genres the same way
    # ----------------------------------------
    processed_library = {}

    for genre, vectors in genre_vectors.items():

        matrix = np.array(vectors)

        normalized_matrix = (matrix - global_mean) / global_std

        # L2 normalize each vector
        norms = np.linalg.norm(normalized_matrix, axis=1, keepdims=True)
        normalized_matrix = normalized_matrix / (norms + 1e-10)

        # -------- CENTROID --------
        centroid = np.mean(normalized_matrix, axis=0)

        # normalize centroid
        centroid = centroid / (np.linalg.norm(centroid) + 1e-10)

        processed_library[genre] = {"centroid": centroid,
                                    "tracks": normalized_matrix,
                                    "feature_mean": feature_means[genre],
                                    "feature_std": feature_stds[genre]
                                    }

    #for genre, data in processed_library.items():
        #print(genre, data["centroid"][:10])

    return processed_library, global_mean, global_std

def normalize(v):
    return v / (np.linalg.norm(v) + 1e-10)

def compute_genre_similarity(user_vector, processed_library):

    similarity_scores = {}

    for genre, data in processed_library.items():

        centroid = data["centroid"]
        tracks = data["tracks"]

        weights = np.array(GENRE_WEIGHTS[genre])

        weighted_user = user_vector * weights
        weighted_centroid = centroid * weights
        weighted_tracks = tracks * weights

        centroid_similarity = np.dot(weighted_user, weighted_centroid)
 
        track_similarities = np.dot(weighted_tracks, weighted_user)

        top_k = min(3, len(track_similarities))
        top_k_scores = np.sort(track_similarities)[-top_k:]

        track_similarity = np.mean(top_k_scores)

        similarity = (
        0.6 * centroid_similarity +
        0.4 * track_similarity
        )

        similarity_scores[genre] = similarity

    #print("\nRaw Similarity Scores:")
    #for genre, score in similarity_scores.items():
        #print(f"{genre}: {score}")

    values = np.array(list(similarity_scores.values()))

    # increase separation
    temperature = 2.0
    scaled_values = values / temperature

    exp_scores = np.exp(scaled_values - np.max(scaled_values))
    probabilities = exp_scores / np.sum(exp_scores)

    probability_dict = {}

    for genre, prob in zip(similarity_scores.keys(), probabilities):
        probability_dict[genre] = float(prob)

    predicted_genre = max(probability_dict, key=probability_dict.get)

    return predicted_genre, probability_dict


def infer_instruments(features):

    instruments = []

    if features["onset_strength_mean"] > 0.5:
        instruments.append("Strong drum/percussion presence")

    if features["spectral_centroid"] < 1800:
        instruments.append("Bass-heavy elements")

    if features["spectral_contrast_mean"][0] > 20:
        instruments.append("Likely harmonic instruments (guitars/synths)")

    mfcc_var = np.mean(features["mfcc_std"])

    if mfcc_var > 50:
        instruments.append("Possible vocals")

    if features["stereo_width"] > 0.3:
        instruments.append("Wide stereo instrumentation")

    return instruments

def explain_genre_prediction(user_vector, processed_library, predicted_genre):

    centroid = processed_library[predicted_genre]["centroid"]

    # contribution = feature influence on similarity
    contributions = user_vector * centroid

    # get top features
    top_indices = np.argsort(np.abs(contributions))[-8:][::-1]

    explanation = []

    for idx in top_indices:

        feature_name = FEATURE_NAMES[idx]
        value = contributions[idx]

        if value > 0:
            explanation.append(f"Strong {feature_name}")
        else:
            explanation.append(f"Distinctive {feature_name}")

    return explanation


def evaluate_mix_quality(features):

    score = 100
    issues = []

    centroid = features["spectral_centroid"]
    flatness = features["spectral_flatness_mean"]
    stereo = features["stereo_width"]
    dynamic = features["dynamic_range"]
    crest = features["crest_factor"]
    lufs = features["LUFS"]

    freq = features["frequency_balance"]
    low = freq["low"]
    mid = freq["mid"]
    high = freq["high"]

    # LUFS check
    if lufs > -8:
        issues.append("Mix extremely loud (possible over-limiting)")
        score -= 10

    if lufs < -18:
        issues.append("Mix unusually quiet")
        score -= 10

    # Crest factor
    if crest < 3:
        issues.append("Low crest factor (over-compressed)")
        score -= 10

    if crest > 12:
        issues.append("Very high crest factor (weak limiting)")
        score -= 8

    # Frequency balance
    if low > mid * 1.8:
        issues.append("Too much low-end energy")
        score -= 8

    if high < mid * 0.3:
        issues.append("High frequencies weak")
        score -= 8

    # Spectral flatness
    if flatness > 0.35:
        issues.append("Possible distortion or noise")
        score -= 10

    # Stereo width
    if stereo < 0.05:
        issues.append("Very narrow stereo field")
        score -= 8

    # Dynamic range
    if dynamic < 0.02:
        issues.append("Very limited dynamics")
        score -= 10

    score = max(0, min(score, 100))

    if score > 85:
        label = "Professional quality mix"
    elif score > 70:
        label = "Good mix"
    elif score > 50:
        label = "Decent mix"
    else:
        label = "Rough / amateur mix"

    return score, label, issues


def analyze_features(user_vector, processed_library, predicted_genre):

    IMPORTANT_FEATURES = FEATURE_NAMES[:27]

    genre_data = processed_library[predicted_genre]

    mean = genre_data["feature_mean"]
    std = genre_data["feature_std"]

    z_scores = (user_vector - mean) / (std + 1e-6)
    z_scores = np.clip(z_scores, -3, 3)

    strength_scores = []
    weakness_scores = []
    balanced = []

    for i, z in enumerate(z_scores):

        feature_name = FEATURE_NAMES[i]

        # Only evaluate important features
        if feature_name not in IMPORTANT_FEATURES:
            continue

        if z > 0.7:
            strength_scores.append((z, feature_name))

        elif z < -0.7:
            weakness_scores.append((abs(z), feature_name))

        else:
            balanced.append(f"{feature_name} typical")

    strength_scores.sort(reverse=True)
    weakness_scores.sort(reverse=True)

    strengths = [f"{name} stronger than typical" for _, name in strength_scores[:5]]
    weaknesses = [f"{name} weaker than typical" for _, name in weakness_scores[:5]]

    return strengths, weaknesses, balanced, z_scores

def generate_suggestions(features):

    suggestions = []

    if features["spectral_centroid"] < 1500:
        suggestions.append("Increase high frequency presence (3–6 kHz EQ)")

    if features["spectral_flatness_mean"] > 0.3:
        suggestions.append("Reduce distortion or noise in mix")

    if features["stereo_width"] < 0.05:
        suggestions.append("Add stereo widening or panning")

    if features["transient_density"] < 1:
        suggestions.append("Enhance drum transients")

    return suggestions


"""if __name__ == "__main__":

    reference_library = load_reference_data()
    processed_library = process_reference_library(reference_library)

    print("Processed Reference Library:")
    for genre, matrix in processed_library.items():
        print(f"{genre}: {matrix.shape}")

    # Create a dummy user vector for testing
    sample_genre = next(iter(processed_library))
    feature_size = processed_library[sample_genre].shape[1]

    user_vector = np.random.rand(feature_size)

    predicted_genre, scores = compute_genre_similarity(user_vector, processed_library)

    print("\nPredicted Genre:", predicted_genre)
    print("Similarity Scores:", scores)"""