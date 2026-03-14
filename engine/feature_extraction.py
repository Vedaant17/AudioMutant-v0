import librosa
import json
import os
import numpy as np
import pyloudnorm as pyln


def extract_features(file_path: str):

    # --------------------------------------------------
    # LOAD AUDIO
    # --------------------------------------------------

    y, sr = librosa.load(file_path, sr=22050, mono=False, duration=600)
    y = y.astype(np.float32)

    if y.ndim > 1:
        y_mono = librosa.to_mono(y)
    else:
        y_mono = y

    # --------------------------------------------------
    # HPSS (HARMONIC / PERCUSSIVE)
    # --------------------------------------------------

    y_harmonic, y_percussive = librosa.effects.hpss(y_mono)

    harmonic_energy = float(np.mean(np.abs(y_harmonic)))
    percussive_energy = float(np.mean(np.abs(y_percussive)))

    harmonic_percussive_ratio = harmonic_energy / (percussive_energy + 1e-8)

    # --------------------------------------------------
    # TEMPO + RHYTHM
    # --------------------------------------------------

    tempo = librosa.feature.tempo(y=y_mono, sr=sr)
    tempo = float(np.mean(tempo))

    tp, beat_frames = librosa.beat.beat_track(y=y_mono, sr=sr)

    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    if len(beat_times) > 1:
        beat_intervals = np.diff(beat_times)
        tempo_stability = float(np.std(beat_intervals))
    else:
        tempo_stability = 0.0

    # --------------------------------------------------
    # KEY DETECTION
    # --------------------------------------------------

    chroma = librosa.feature.chroma_cqt(y=y_mono, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    chroma_std = np.std(chroma, axis=1)

    major_profile = np.array([
        6.35,2.23,3.48,2.33,4.38,4.09,
        2.52,5.19,2.39,3.66,2.29,2.88
    ])

    minor_profile = np.array([
        6.33,2.68,3.52,5.38,2.60,3.53,
        2.54,4.75,3.98,2.69,3.34,3.17
    ])

    major_scores = []
    minor_scores = []

    for i in range(12):
        major_scores.append(np.corrcoef(np.roll(chroma_mean,-i), major_profile)[0,1])
        minor_scores.append(np.corrcoef(np.roll(chroma_mean,-i), minor_profile)[0,1])

    major_key = np.argmax(major_scores)
    minor_key = np.argmax(minor_scores)

    note_names = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

    if max(major_scores) > max(minor_scores):
        key_signature = f"{note_names[major_key]} major"
    else:
        key_signature = f"{note_names[minor_key]} minor"

    # --------------------------------------------------
    # LOUDNESS
    # --------------------------------------------------

    rms = librosa.feature.rms(y=y_mono)[0]
    mean_rms = float(np.mean(rms))

    peak = float(np.max(np.abs(y_mono)))

    meter = pyln.Meter(sr)

    if y.ndim == 1:
        lufs = meter.integrated_loudness(y)
    else:
        lufs = meter.integrated_loudness(y.T)

    crest_factor = peak / (mean_rms + 1e-8)

    dynamic_range = float(np.percentile(rms,95) - np.percentile(rms,5))

    compression_ratio = crest_factor / (dynamic_range + 1e-8)

    # --------------------------------------------------
    # SPECTRAL FEATURES
    # --------------------------------------------------

    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y_mono, sr=sr)))

    bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y_mono, sr=sr)))

    rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y_mono, sr=sr)))

    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y_mono)))

    flatness = librosa.feature.spectral_flatness(y=y_mono)

    spectral_flatness_mean = float(np.mean(flatness))
    spectral_flatness_std = float(np.std(flatness))

    contrast = librosa.feature.spectral_contrast(y=y_mono, sr=sr)

    mean_contrast = np.mean(contrast, axis=1)
    std_contrast = np.std(contrast, axis=1)


    # --------------------------------------------------
    # STFT BASED FEATURES
    # --------------------------------------------------

    stft = np.abs(librosa.stft(y_mono, n_fft=2048, hop_length=512))

    freqs = librosa.fft_frequencies(sr=sr)

    # Spectral Flux

    spectral_flux = np.sqrt(np.sum(np.diff(stft, axis=1)**2, axis=0))

    spectral_flux_mean = float(np.mean(spectral_flux))
    spectral_flux_std = float(np.std(spectral_flux))

    # --------------------------------------------------
    # FREQUENCY BANDS
    # --------------------------------------------------

    low_band = np.where((freqs >= 20) & (freqs < 250))
    mid_band = np.where((freqs >= 250) & (freqs < 4000))
    high_band = np.where(freqs >= 4000)

    low_energy = float(np.mean(stft[low_band]))
    mid_energy = float(np.mean(stft[mid_band]))
    high_energy = float(np.mean(stft[high_band]))

    frequency_balance = {
        "low": low_energy,
        "mid": mid_energy,
        "high": high_energy
    }

    low_mid_ratio = low_energy / (mid_energy + 1e-8)
    mid_high_ratio = mid_energy / (high_energy + 1e-8)

    # --------------------------------------------------
    # SUB BASS
    # --------------------------------------------------

    sub_bass_idx = np.where(freqs < 60)

    sub_bass_energy = float(np.mean(stft[sub_bass_idx]))

    # --------------------------------------------------
    # ONSETS / TRANSIENTS
    # --------------------------------------------------

    onset_env = librosa.onset.onset_strength(y=y_mono, sr=sr)

    onset_strength_mean = float(np.mean(onset_env))
    onset_strength_std = float(np.std(onset_env))

    beat_strength = float(np.mean(librosa.util.normalize(onset_env)))

    onsets = librosa.onset.onset_detect(onset_envelope=onset_env)

    duration_seconds = librosa.get_duration(y=y_mono, sr=sr)

    transient_density = float(len(onsets) / duration_seconds)

    # --------------------------------------------------
    # SILENCE
    # --------------------------------------------------

    silence_threshold = 0.01

    silent_samples = np.sum(np.abs(y_mono) < silence_threshold)

    silence_ratio = float(silent_samples / len(y_mono))

    # --------------------------------------------------
    # MFCC (TIMBRE FINGERPRINT)
    # --------------------------------------------------

    mfcc = librosa.feature.mfcc(y=y_mono, sr=sr, n_mfcc=13)

    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)

    # --------------------------------------------------
    # STEREO WIDTH
    # --------------------------------------------------

    if y.ndim > 1:
        left = y[0]
        right = y[1]
        correlation = np.corrcoef(left,right)[0,1]
        correlation = np.clip(correlation, -1, 1)
        stereo_width = float(1 - correlation)
    else:
        stereo_width = 0.0

    # --------------------------------------------------
    # RETURN FEATURES
    # --------------------------------------------------

    return {

        "tempo_bpm": tempo,
        "tempo_stability": tempo_stability,
        "key_signature": key_signature,

        "harmonic_energy": harmonic_energy,
        "percussive_energy": percussive_energy,
        "harmonic_percussive_ratio": harmonic_percussive_ratio,

        "loudness_rms": mean_rms,
        "LUFS": lufs,
        "peak_amplitude": peak,
        "crest_factor": crest_factor,
        "dynamic_range": dynamic_range,
        "compression_ratio": compression_ratio,

        "spectral_centroid": centroid,
        "spectral_bandwidth": bandwidth,
        "spectral_rolloff": rolloff,
        "spectral_flatness_mean": spectral_flatness_mean,
        "spectral_flatness_std": spectral_flatness_std,
        "zero_crossing_rate": zcr,

        "spectral_flux_mean": spectral_flux_mean,
        "spectral_flux_std": spectral_flux_std,

        "stereo_width": stereo_width,
        "sub_bass_energy": sub_bass_energy,

        "frequency_balance": frequency_balance,
        "low_mid_ratio": low_mid_ratio,
        "mid_high_ratio": mid_high_ratio,

        "transient_density": transient_density,
        "beat_strength": beat_strength,
        "onset_strength_mean": onset_strength_mean,
        "onset_strength_std": onset_strength_std,

        "silence_ratio": silence_ratio,

        "chroma_mean": chroma_mean.tolist(),
        "chroma_std": chroma_std.tolist(),

        "mfcc_mean": mfcc_mean.tolist(),
        "mfcc_std": mfcc_std.tolist(),

        "spectral_contrast_mean": mean_contrast.tolist(),
        "spectral_contrast_std": std_contrast.tolist(),
    }


# --------------------------------------------------
# CLEAN NUMPY TYPES
# --------------------------------------------------

def clean_features(obj):

    if isinstance(obj, np.generic):
        return obj.item()

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, dict):
        return {k: clean_features(v) for k,v in obj.items()}

    if isinstance(obj,(list,tuple)):
        return [clean_features(v) for v in obj]

    return obj


# --------------------------------------------------
# PRINT JSON
# --------------------------------------------------

def print_features_json(features):

    cleaned = clean_features(features)

    print("\nExtracted Features (JSON):\n")
    print(json.dumps(cleaned, indent=4))

    return cleaned


# --------------------------------------------------
# SAVE REFERENCE TRACK
# --------------------------------------------------

def save_reference(track_name, artist, genre, features):

    cleaned = clean_features(features)

    data = {
        "track": track_name,
        "artist": artist,
        "genre": genre,
        "features": cleaned
    }

    folder = f"reference_data/{genre}"
    os.makedirs(folder, exist_ok=True)

    filename = f"{track_name.lower().replace(' ','_')}.json"
    path = os.path.join(folder, filename)

    with open(path,"w") as f:
        json.dump(data,f,indent=4)

    print(f"Saved reference file: {path}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    features = extract_features("Tiësto - Adagio For Strings.mp3")

    print_features_json(features)

    save_reference(
        track_name="Adagio For Strings",
        artist="Tiesto",
        genre="edm",
        features=features
    )