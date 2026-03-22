import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from engine.feature_extraction import extract_features
from engine.vector_builder import build_feature_vector
from engine.reference_engine import (
    load_reference_data,
    process_reference_library,
    compute_genre_similarity,
    infer_instruments,
    evaluate_mix_quality,
    analyze_features,
    generate_suggestions
)
from engine.production_feedback import generate_production_feedback
from engine.reference_matcher import find_closest_tracks
from engine.feature_names import FEATURE_NAMES, BASE_FEATURE_NAMES
from engine.mix_style import detect_mix_style
from backend.ai_agents.agent_pipeline import run_mix_agent
from engine.reference_comparison import get_reference_features, compute_reference_average, compare_mix, interpret_differences
from engine.change_simulator import run_mix_simulations
import numpy as np


def build_user_vector(features):
    """
    Convert extracted features into a vector compatible
    with the reference engine.
    """

    vector = []

    # Tempo
    vector.append(features.get("tempo_bpm", 0))

    # Spectral centroid
    vector.append(features.get("spectral_centroid", 0))

    # Spectral bandwidth
    vector.append(features.get("spectral_bandwidth", 0))

    # Zero crossing rate
    vector.append(features.get("zero_crossing_rate", 0))

    # RMS loudness
    vector.append(features.get("loudness_rms", 0))

    # Dynamic range
    vector.append(features.get("dynamic_range", 0))

    # Spectral rolloff
    vector.append(features.get("spectral_rolloff", 0))

    # Spectral contrast
    vector.append(features.get("spectral_contrast", 0))

    # Stereo width
    vector.append(features.get("stereo_width", 0))

    # Sub bass energy
    vector.append(features.get("sub_bass_energy", 0))

    # Transient density
    vector.append(features.get("transient_density", 0))

    # Silence ratio
    vector.append(features.get("silence_ratio", 0))

    # Frequency balance
    freq_balance = features.get("frequency_balance", {})
    vector.append(freq_balance.get("low", 0))
    vector.append(freq_balance.get("mid", 0))
    vector.append(freq_balance.get("high", 0))

    return np.array(vector)


"""def run_pipeline(audio_file):

    print("\n--- Extracting Features ---")
    features = extract_features(audio_file)

    print("\n--- Building Feature Vector ---")
    raw_user_vector = build_feature_vector(features)

    print("\n--- Loading Reference Library ---")
    reference_library = load_reference_data()


    #for genre, tracks in reference_library.items():
       # print(f"{genre}: {len(tracks)} reference tracks")

    print("\n--- Processing Reference Library ---")
    processed_library, global_mean, global_std = process_reference_library(reference_library)

    # Normalize user vector AFTER reference stats are known
    user_vector = (raw_user_vector - global_mean) / global_std
    #user_vector = user_vector / (np.linalg.norm(user_vector) + 1e-10)

    #print("\nUser vector normalized using global reference statistics.")
    #np.linalg.norm(user_vector)  # just to confirm it's not all zeros
    #print("First 10 values:", user_vector[:10])

    print("\n--- Computing Similarity ---")
    predicted_genre, similarity_scores = compute_genre_similarity(
        user_vector,
        processed_library
    )


    print("\n===== RESULT =====")
    
    confidence = similarity_scores[predicted_genre] * 100

    print(f"Predicted Genre: {predicted_genre}")
    print(f"Confidence: {confidence:.2f}%")

    print("\nGenre Probabilities:")

    for genre, score in sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True):
        print(f"{genre}: {score*100:.2f}%")

    if confidence < 40:
        print("\n⚠ Low confidence prediction — track may be multi-genre.")

    print("\n--- Instrument Detection ---")
    instruments = infer_instruments(features)

    for inst in instruments:
        print("✓", inst)

    print("\n--- Mix Quality ---")

    mix_score, mix_label, issues = evaluate_mix_quality(features)

    print(f"Score: {mix_score}/100")
    print("Classification:", mix_label)

    closest_tracks = find_closest_tracks(user_vector, processed_library)
    print("\n--- Reference Mix Comparison ---")

    reference_tracks = get_reference_features(
    reference_library,
    closest_tracks
    )

    reference_avg = compute_reference_average(reference_tracks)

    differences = compare_mix(features, reference_avg)

    reference_diagnostics = interpret_differences(differences)

    for k, v in reference_diagnostics.items():
        print(f"{k}: {v}")

    print("\n---Closest Reference Tracks ---")
    for sim, genre, idx in closest_tracks:
        percent = sim*10
        print(f"{genre} reference track{idx+1} - Similarity: {percent:.1f}%")


    strengths, weaknesses, balanced, z_scores = analyze_features(
        user_vector,
        processed_library,
        predicted_genre,
    )

    mix_style = detect_mix_style(z_scores, FEATURE_NAMES)
    print("\n--- Mix Style ---")
    for k, v in mix_style.items():
        print(f"{k}: {v}")

    reference_mean = processed_library[predicted_genre]["feature_mean"]
    #reference_mean_raw = reference_mean * global_mean * global_std
    simulation_results = run_mix_simulations(
        raw_user_vector,
        FEATURE_NAMES,
        reference_mean
    )

    print("\n --- Predicted Results")
    for k, v in simulation_results.items():
        print(f"{k}: {v}")
    

    #print("\n--- Feedback ---")
    feedback = generate_production_feedback(strengths, weaknesses, balanced)
    #for f in feedback:
        #print(f)

    result = {
    "feature_vector": user_vector.tolist(),
    "predicted_genre": predicted_genre,
    "confidence": confidence,

    "genre_probabilities": similarity_scores,

    "instrument_detection": instruments,

    "mix_score": mix_score,
    "mix_label": mix_label,
    "mix_issues": issues,

    "closest_reference_tracks": closest_tracks,
    "reference_mix_analysis": reference_diagnostics,

    "mix_style": mix_style,

    "strengths": strengths,
    "weaknesses": weaknesses,
    "balanced_features": balanced,

    "production_feedback": feedback,
    "mix_change_simulation": simulation_results,


    "reference_mean": processed_library[predicted_genre]["feature_mean"].tolist(),
    "reference_std": processed_library[predicted_genre]["feature_std"].tolist(),
    "feature_names": FEATURE_NAMES
}

    return result

def display_results(result):

    print("\n===== RESULT =====")

    print("Predicted Genre:", result["predicted_genre"])
    print("Confidence:", result["confidence"])
"""

def run_pipeline(audio_file, progress_callback=None):
    try:
        if progress_callback:
            progress_callback(5, "Extracting features")

        features = extract_features(audio_file)

        if progress_callback:
            progress_callback(15, "Building feature vector")

        raw_user_vector = build_feature_vector(features)

        if progress_callback:
            progress_callback(30, "Loading reference library")

        reference_library = load_reference_data()

        if progress_callback:
            progress_callback(45, "Processing reference data")

        processed_library, global_mean, global_std = process_reference_library(reference_library)

        if progress_callback:
            progress_callback(60, "Computing similarity")

        user_vector = (raw_user_vector - global_mean) / global_std

        predicted_genre, similarity_scores = compute_genre_similarity(
        user_vector,
        processed_library
        )

        if progress_callback:
            progress_callback(75, "Analyzing mix")

        instruments = infer_instruments(features)
        mix_score, mix_label, issues = evaluate_mix_quality(features)

        if progress_callback:
            progress_callback(85, "Running simulations")

        simulation_results = run_mix_simulations(
        raw_user_vector,
        FEATURE_NAMES,
        processed_library[predicted_genre]["feature_mean"]
        )

        if progress_callback:
            progress_callback(95, "Finalizing results")

        result = {
        "predicted_genre": predicted_genre,
        "confidence": similarity_scores[predicted_genre] * 100,
        "mix_score": mix_score,
        "mix_label": mix_label,
        "simulation_results": simulation_results,
        "original_features": raw_user_vector.tolist(),
        "target_features": processed_library[predicted_genre]["feature_mean"].tolist(),
        }

        if progress_callback:
            progress_callback(100, "Completed")

        return result
    
    except Exception as e:
        if progress_callback:
            progress_callback(100, f"Error: {str(e)}")
        raise e

def display_results(result):

    print("\n===== RESULT =====")

    print("Predicted Genre:", result["predicted_genre"])
    print("Confidence:", result["confidence"])

    
if __name__ == "__main__":

    audio_file = "dunno3.wav" # replace with your test file

    engine_result = run_pipeline(audio_file)
    mode = "detailed"
    ai_advice = run_mix_agent(engine_result)

    print("\n ---AI Mix Engineer--\n")    
    print(json.dumps(ai_advice, indent=2))