def detect_mix_style(z_scores, feature_names):

    feature_map = dict(zip(feature_names, z_scores))

    lufs = feature_map.get("LUFS", 0)
    rms = feature_map.get("RMS Loudness", 0)
    centroid = feature_map.get("Spectral Centroid", 0)
    bandwidth = feature_map.get("Spectral Bandwidth", 0)
    stereo = feature_map.get("Stereo Width", 0)
    transient = feature_map.get("Transient Density", 0)

    style = {}

    # Loudness style
    if lufs > 0.6 or rms > 0.6:
        style["Overall Style"] = "Loud Modern Mix"
    elif lufs < -0.6:
        style["Overall Style"] = "Dynamic / Quiet Mix"
    else:
        style["Overall Style"] = "Balanced Mix"

    # Energy
    if transient > 0.6:
        style["Energy Profile"] = "High Energy"
    elif transient < -0.6:
        style["Energy Profile"] = "Low Energy"
    else:
        style["Energy Profile"] = "Moderate Energy"

    # Brightness
    if centroid > 0.6 or bandwidth > 0.6:
        style["Brightness Profile"] = "Bright"
    elif centroid < -0.6:
        style["Brightness Profile"] = "Dark"
    else:
        style["Brightness Profile"] = "Balanced"

    # Stereo field
    if stereo > 0.6:
        style["Stereo Profile"] = "Wide"
    elif stereo < -0.6:
        style["Stereo Profile"] = "Narrow"
    else:
        style["Stereo Profile"] = "Balanced"

    # Punch
    if transient > 0.6:
        style["Punch Profile"] = "Punchy"
    elif transient < -0.6:
        style["Punch Profile"] = "Soft"
    else:
        style["Punch Profile"] = "Balanced"

    return style