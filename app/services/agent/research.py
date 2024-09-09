from app.services.agent.base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    def execute_task(self, task: dict):
        prompt = self.prompt_builder.research_prompt(task["topic"])
        result = self.llm_executor.execute(prompt, {"topic": task["topic"]})
        return result
