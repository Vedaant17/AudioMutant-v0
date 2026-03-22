import json

def build_prompt(filtered_result, gap_summary, user_context, top_moves, mode="detailed"):

    if mode == "quick":
        format_instructions = """
Return ONLY valid JSON in this format:

{
  "top_fixes": ["...", "...", "..."],
  "why": "1-2 sentence explanation of the main problem"
}
"""
    else:
        format_instructions = """
Return ONLY valid JSON in this format:

{
  "summary": "...",
  "strengths": ["...", "..."],
  "issues": ["...", "..."],
  "top_fixes": ["...", "...", "..."],
  "eq": ["...", "..."],
  "compression": ["...", "..."],
  "stereo": ["...", "..."],
  "effects": ["...", "..."],
  "steps": ["...", "...", "..."],
  "daw_tips": ["...", "..."]
}
"""

    prompt = f"""
You are a professional mixing engineer AI.

Analyze the mix and provide practical, real-world advice.

---

MIX DATA:
{json.dumps(filtered_result, indent=2)}

REFERENCE GAPS:
{json.dumps(gap_summary, indent=2)}

TOP PRIORITY IMPROVEMENTS:
{json.dumps(top_moves, indent=2)}

USER CONTEXT:
{json.dumps(user_context, indent=2)}

---

INSTRUCTIONS:

- Focus on closing the biggest gaps with reference mixes
- Use TOP PRIORITY IMPROVEMENTS as the main guidance
- Give specific, DAW-usable advice
- Avoid generic suggestions

---

{format_instructions}

IMPORTANT:
- Output MUST be valid JSON
- No explanations outside JSON
"""

    return prompt