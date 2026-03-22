import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from .gap_analysis import summarize_gaps, compute_reference_gaps
from .user_context import collect_user_context
from .prompt_builder import build_prompt
from .utils import convert_numpy
from .data_formatter import extract_relevant_data, get_top_moves


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def run_mix_agent(engine_result, mode="detailed"):

    # ✅ Convert numpy → JSON safe
    engine_result = convert_numpy(engine_result)

    # ✅ Filter only important data
    filtered_result = extract_relevant_data(engine_result)

    # ✅ Compute reference gaps
    feature_names = engine_result["feature_names"]
    gaps = compute_reference_gaps(engine_result, feature_names)
    gap_summary = summarize_gaps(gaps)

    # ✅ Get user context
    user_context = collect_user_context()

    # ✅ Get top simulation moves
    simulation = filtered_result.get("simulation", {})
    top_moves = get_top_moves(simulation)

    # ✅ Build prompt
    prompt = build_prompt(
        filtered_result,
        gap_summary,
        user_context,
        top_moves,
        mode
    )

    # ✅ Call model
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    # ✅ Parse JSON safely
    try:
        output_text = response.output_text.strip()
        parsed_output = json.loads(output_text)
        return parsed_output

    except Exception as e:
        return {
            "error": "Failed to parse AI response",
            "raw_output": response.output_text
        }