import numpy as np

def find_closest_tracks(user_vector, processed_library, top_n=3):

    matches = []

    for genre, data in processed_library.items():

        tracks = data["tracks"]   # matrix of normalized track vectors

        for i, track_vector in enumerate(tracks):

            similarity = np.dot(user_vector, track_vector)

            matches.append((similarity, genre, i))

    matches.sort(reverse=True)

    return matches[:top_n]