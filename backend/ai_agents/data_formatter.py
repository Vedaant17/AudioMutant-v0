def extract_relevant_data(engine_result):
    return {
        "genre": engine_result.get("predicted_genre"),
        "mix_score": engine_result.get("mix_score"),
        "mix_style": engine_result.get("mix_style"),

        "strengths": engine_result.get("strengths"),
        "weaknesses": engine_result.get("weaknesses"),

        "reference_comparison": engine_result.get("reference_comparison"),

        "simulation": engine_result.get("mix_change_simulation"),
    }


def get_top_moves(simulation, top_n=3):
    if not simulation:
        return []

    valid_moves = [(k, v) for k, v in simulation.items() if v is not None]

    # sort descending (most impact first)
    sorted_moves = sorted(valid_moves, key=lambda x: x[1], reverse=True)

    return sorted_moves[:top_n]