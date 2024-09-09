from typing import List, Dict
from app.models.agent import Agent, AgentType, ResearchAgent, CodingAgent, WritingAgent
import uuid


class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    def create_agent(
        self, agent_type: AgentType, name: str, skills: List[str], **kwargs
    ) -> Agent:
        agent_id = str(uuid.uuid4())
        if agent_type == AgentType.RESEARCH:
            agent = ResearchAgent(id=agent_id, name=name, skills=skills, **kwargs)
        elif agent_type == AgentType.CODING:
            agent = CodingAgent(id=agent_id, name=name, skills=skills, **kwargs)
        elif agent_type == AgentType.WRITING:
            agent = WritingAgent(id=agent_id, name=name, skills=skills, **kwargs)
        else:
            raise ValueError(f"Invalid agent type: {agent_type}")

        self.agents[agent_id] = agent
        return agent

    def get_agent(self, agent_id: str) -> Agent:
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Agent]:
        return list(self.agents.values())

    def update_agent_status(self, agent_id: str, status: str, current_task: str = None):
        agent = self.get_agent(agent_id)
        if agent:
            agent.status = status
            agent.current_task = current_task

    def assign_task(self, agent_id: str, task_id: str):
        self.update_agent_status(agent_id, "busy", task_id)

    def complete_task(self, agent_id: str):
        self.update_agent_status(agent_id, "idle", None)


agent_manager = AgentManager()
