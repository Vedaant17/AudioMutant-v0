from pydantic import BaseModel
from typing import List, Optional

class InputTrack(BaseModel):
    track_name: str
    description: str
    tempo: int
    key: str
    loudness: float
    genre: str

class AgentOutput(BaseModel):
    mix_feedback: str | None = None
    harmony_suggestions: str | None = None
    sound_design_ideas: str | None = None
    creative_direction: str | None = None

class MixSuggestion(BaseModel):
    issue: str
    suggestion: str
    plugin_recommendation: Optional[str] = None