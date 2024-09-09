import uuid
from typing import List, Dict
from app.models.task import TaskStatus, Task
from app.services.agent.manager import agent_manager


class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def create_task(self, description: str, priority: int = 1) -> Task:
        task_id = str(uuid.uuid4())
        task = Task(id=task_id, description=description, priority=priority)
        self.tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    def update_task_status(self, task_id: str, status: TaskStatus):
        task = self.get_task(task_id)
        if task:
            task.status = status

    def assign_task(self, task_id: str, agent_id: str):
        task = self.get_task(task_id)
        if task:
            task.assigned_agent = agent_id
            task.status = TaskStatus.IN_PROGRESS
            agent_manager.assign_task(agent_id, task_id)

    def complete_task(self, task_id: str):
        task = self.get_task(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            if task.assigned_agent:
                agent_manager.complete_task(task.assigned_agent)

    def create_subtask(self, parent_task_id: str, description: str) -> Task:
        subtask = self.create_task(description)
        parent_task = self.get_task(parent_task_id)
        if parent_task:
            parent_task.subtasks.append(subtask.id)
            subtask.parent_task = parent_task_id
        return subtask


task_manager = TaskManager()
