import numpy as np

def convert_numpy(obj):

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, np.float32) or isinstance(obj, np.float64):
        return float(obj)

    if isinstance(obj, np.int32) or isinstance(obj, np.int64):
        return int(obj)

    if isinstance(obj, list):
        return [convert_numpy(i) for i in obj]

    if isinstance(obj, tuple):
        return tuple(convert_numpy(i) for i in obj)

    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}

    return obj