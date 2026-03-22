FEEDBACK_RULES = {

    "Sub Bass Energy": {
        "weak": "Your mix lacks sub-bass compared to typical tracks. Consider boosting around 40–60 Hz.",
        "balanced": "Your sub-bass levels are well balanced for modern mixes.",
        "strong": "Your mix has strong sub-bass presence. Ensure it doesn't overpower the kick."
    },

    "Low/Mid Ratio": {
        "weak": "Your mix may lack warmth. Consider adding subtle energy around 150–300 Hz.",
        "balanced": "Your low-mid balance is well controlled.",
        "strong": "Your mix may contain excess low-mid energy causing muddiness. Consider reducing 150–300 Hz."
    },

    "Mid/High Ratio": {
        "weak": "High frequencies may be weak. Consider boosting around 8–12 kHz.",
        "balanced": "Your high-frequency balance is good.",
        "strong": "Your mix has strong high-frequency presence which adds clarity."
    },

    "Spectral Bandwidth": {
        "weak": "Your mix lacks high-frequency content. Try boosting around 8–12 kHz.",
        "balanced": "Your mix has a healthy spectral bandwidth.",
        "strong": "Your mix has very strong high-frequency presence."
    },

    "Spectral Centroid": {
        "weak": "Your mix sounds darker than typical tracks. Add brightness around 6–10 kHz.",
        "balanced": "Your tonal brightness is well balanced.",
        "strong": "Your mix is brighter than typical tracks."
    },

    "Stereo Width": {
        "weak": "Your mix is narrow. Try widening pads, synths or reverbs.",
        "balanced": "Your stereo width is well balanced.",
        "strong": "Your mix has strong stereo width which creates an immersive soundstage."
    },

    "Percussive Energy": {
        "weak": "Drums feel less energetic than typical tracks. Try boosting transients or compression.",
        "balanced": "Your drum energy is well balanced.",
        "strong": "Your track has strong percussive impact."
    },

    "Transient Density": {
        "weak": "Your mix lacks punch. Try enhancing drum transients.",
        "balanced": "Your transient activity is well balanced.",
        "strong": "Your mix has strong transient punch."
    },

    "Dynamic Range": {
        "weak": "Your mix may be over-compressed. Reduce limiting to restore dynamics.",
        "balanced": "Your track retains a healthy dynamic range.",
        "strong": "Your mix has very large dynamic range compared to typical masters."
    },

    "Crest Factor": {
        "weak": "Your track may be heavily limited. Allow more peak dynamics.",
        "balanced": "Your peak dynamics are well balanced.",
        "strong": "Your track maintains strong peak dynamics."
    },

    "LUFS": {
        "weak": "Your mix may be quieter than typical commercial tracks.",
        "balanced": "Your loudness level is appropriate for modern streaming.",
        "strong": "Your mix is very loud. Excess limiting may reduce clarity."
    },

    "Zero Crossing Rate": {
        "weak": "Your mix may lack high-frequency detail.",
        "balanced": "Your high-frequency activity is balanced.",
        "strong": "Your mix contains strong high-frequency activity."
    },

    "Spectral Flatness Mean": {
        "weak": "Your mix may lack harmonic richness. Try adding saturation.",
        "balanced": "Your harmonic content is balanced.",
        "strong": "Your mix contains strong harmonic/noise texture."
    },

    "Spectral Flux Mean": {
        "weak": "Your track may lack movement between frames.",
        "balanced": "Your track shows good spectral movement.",
        "strong": "Your track has very dynamic spectral movement."
    }
}

def generate_production_feedback(strengths, weaknesses, balanced):

    feedback = []

    for s in strengths:
        feature = s.replace(" stronger than typical", "")

        if feature in FEEDBACK_RULES:
            feedback.append("▲ " + FEEDBACK_RULES[feature]["strong"])

    for w in weaknesses:
        feature = w.replace(" weaker than typical", "")

        if feature in FEEDBACK_RULES:
            feedback.append("• " + FEEDBACK_RULES[feature]["weak"])

    for b in balanced:
        feature = b.replace(" typical", "")

        if feature in FEEDBACK_RULES:
            feedback.append("✓ " + FEEDBACK_RULES[feature]["balanced"])

    return feedback