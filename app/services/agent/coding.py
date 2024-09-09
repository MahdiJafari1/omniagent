from app.services.agent.base_agent import BaseAgent


class CodingAgent(BaseAgent):
    def execute_task(self, task: dict):
        prompt = self.prompt_builder.coding_prompt(task["requirements"])
        result = self.llm_executor.execute(
            prompt, {"requirements": task["requirements"]}
        )
        return result
