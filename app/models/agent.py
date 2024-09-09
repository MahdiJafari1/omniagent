from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class AgentType(str, Enum):
    RESEARCH = "research"
    CODING = "coding"
    WRITING = "writing"


class Agent(BaseModel):
    id: str
    type: AgentType
    name: str
    skills: List[str]
    status: str = "idle"
    current_task: Optional[str] = None


class ResearchAgent(Agent):
    type: AgentType = AgentType.RESEARCH
    research_specialties: List[str]


class CodingAgent(Agent):
    type: AgentType = AgentType.CODING
    programming_languages: List[str]


class WritingAgent(Agent):
    type: AgentType = AgentType.WRITING
    writing_styles: List[str]
