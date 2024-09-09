from abc import ABC, abstractmethod
from app.services.llm.executor import Executor
from app.services.llm.prompt_builders import PromptBuilder


class BaseAgent(ABC):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm_executor = Executor(model)
        self.prompt_builder = PromptBuilder()

    @abstractmethod
    def execute_task(self, task: dict):
        pass
