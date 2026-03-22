import asyncio
from backend.ai_agents.agent_pipeline import run_mix_agent

async def generate_ai_feedback(engine_result):

    try:
        loop = asyncio.get_event_loop()
        advice = await loop.run_in_executor(None, run_mix_agent, engine_result)

        return {
            "status": "success",
            "ai_advice": advice
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }