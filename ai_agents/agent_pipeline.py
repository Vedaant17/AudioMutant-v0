import os
from openai import OpenAI
from dotenv import load_dotenv
from .gap_analysis import summarize_gaps, compute_reference_gaps
from .user_context import collect_user_context
from .prompt_builder import build_prompt
from .utils import convert_numpy

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_mix_agent(engine_result):
    engine_result = convert_numpy(engine_result)
    feature_names = engine_result["feature_names"]
    gaps = compute_reference_gaps(engine_result, feature_names)
    gap_summary = summarize_gaps(gaps)
    user_context = collect_user_context()
    prompt = build_prompt(
        engine_result,
        gap_summary,
        user_context
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input = prompt
    )

    return response.output_text