import json

def build_prompt(engine_result, gap_summary, user_context):

    prompt = f"""
You are a professional mixing engineer AI.

Analyze the mix using the engine results.

ENGINE ANALYSIS:
{json.dumps(engine_result, indent=2)}

REFERENCE MIX GAPS:
{json.dumps(gap_summary, indent=2)}

USER CONTEXT:
{json.dumps(user_context, indent=2)}

Tasks:

1. Explain how the mix currently sounds.
2. Identify strengths.
3. Identify weaknesses.
4. Compare the mix to professional reference mixes.
5. Explain the biggest mix gaps.
6. Suggest improvements.
7. Provide step-by-step instructions for fixing the mix.
8. Recommend effects (EQ, compression, reverb, delay, chorus).
9. Suggest plugins if possible.
10. Adapt advice to the user's DAW and instruments.

Provide practical advice like a professional mix engineer.
"""

    return prompt