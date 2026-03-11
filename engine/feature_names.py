BASE_FEATURE_NAMES = [
    "Tempo",
    "Tempo Stability",
    "Harmonic Energy",
    "Percussive Energy",
    "Harmonic/Percussive Ratio",
    "RMS Loudness",
    "LUFS",
    "Crest Factor",
    "Dynamic Range",
    "Compression Ratio",
    "Spectral Centroid",
    "Spectral Bandwidth",
    "Spectral Rolloff",
    "Spectral Flatness Mean",
    "Spectral Flatness Std",
    "Zero Crossing Rate",
    "Spectral Flux Mean",
    "Spectral Flux Std",
    "Stereo Width",
    "Sub Bass Energy",
    "Low/Mid Ratio",
    "Mid/High Ratio",
    "Transient Density",
    "Beat Strength",
    "Onset Strength Mean",
    "Onset Strength Std",
    "Silence Ratio",
]

MFCC_MEAN_NAMES = [f"MFCC Mean {i+1}" for i in range(13)]
MFCC_STD_NAMES = [f"MFCC Std {i+1}" for i in range(13)]

CHROMA_MEAN_NAMES = [f"Chroma Mean {i+1}" for i in range(12)]
CHROMA_STD_NAMES = [f"Chroma Std {i+1}" for i in range(12)]

SPECTRAL_CONTRAST_MEAN_NAMES = [
    f"Spectral Contrast Mean {i+1}" for i in range(7)
]

SPECTRAL_CONTRAST_STD_NAMES = [
    f"Spectral Contrast Std {i+1}" for i in range(7)
]

FEATURE_NAMES = (
    BASE_FEATURE_NAMES
    + MFCC_MEAN_NAMES
    + MFCC_STD_NAMES
    + CHROMA_MEAN_NAMES
    + CHROMA_STD_NAMES
    + SPECTRAL_CONTRAST_MEAN_NAMES
    + SPECTRAL_CONTRAST_STD_NAMES
)