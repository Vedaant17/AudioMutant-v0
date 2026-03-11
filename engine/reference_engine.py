import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from vector_builder import build_feature_vector

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

    # -----------------------------
    # Step 1: Build feature vectors
    # -----------------------------
    for genre, tracks in reference_library.items():

        genre_vectors[genre] = []

        for track_features in tracks:

            vector = build_feature_vector(track_features)

            genre_vectors[genre].append(vector)

            all_vectors.append(vector)

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
                                    "tracks": normalized_matrix}

    for genre, data in processed_library.items():
        print(genre, data["centroid"][:10])

    return processed_library, global_mean, global_std


def compute_genre_similarity(user_vector, processed_library):

    similarity_scores = {}

    for genre, data in processed_library.items():

        centroid = data["centroid"]
        tracks = data["tracks"]

        centroid_similarity = np.dot(user_vector, centroid)

        track_similarities = np.dot(tracks, user_vector)
        best_track_similarity = np.max(track_similarities)

        similarity = (
        0.7 * centroid_similarity +
        0.3 * best_track_similarity
        )

        similarity_scores[genre] = np.clip(similarity, -1, 1)

    print("\nRaw Similarity Scores:")
    for genre, score in similarity_scores.items():
        print(f"{genre}: {score}")

    values = np.array(list(similarity_scores.values()))

    # increase separation
    temperature = 3.0
    scaled_values = values * temperature

    exp_scores = np.exp(scaled_values - np.max(scaled_values))
    probabilities = exp_scores / np.sum(exp_scores)

    probability_dict = {}

    for genre, prob in zip(similarity_scores.keys(), probabilities):
        probability_dict[genre] = float(prob)

    predicted_genre = max(probability_dict, key=probability_dict.get)

    return predicted_genre, probability_dict

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