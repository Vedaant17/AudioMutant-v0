import numpy as np

def compute_reference_gaps(result, feature_names):
    user_vector = np.array(result["feature_vector"])
    ref_mean = np.array(result["reference_mean"])

    gaps = []

    for i, name in enumerate(feature_names):
        diff = user_vector[i] - ref_mean[i]
        gaps.append({
            "feature": name,
            "difference": float(diff)
        })

    return gaps

def summarize_gaps(gaps):
    too_high = []
    too_low = []

    for g in gaps:
        if g["difference"] > 0.8:
            too_high.append(g)
        elif g["difference"] < -0.8:
            too_low.append(g)
    too_high.sort(key=lambda x: x["difference"], reverse=True)
    too_low.sort(key=lambda x: x["difference"])

    return {
        "too_high": too_high[:5],
        "too_low": too_low[:5]
    }