from app.services.agent.base_agent import BaseAgent


class WritingAgent(BaseAgent):
    def execute_task(self, task: dict):
        prompt = self.prompt_builder.writing_prompt(task["topic"], task["style"])
        result = self.llm_executor.execute(
            prompt, {"topic": task["topic"], "style": task["style"]}
        )
        return result
