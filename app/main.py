from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings

app = FastAPI(
    title=settings.TTILE,
    openapi_tags=settings.TAGS_METADATA,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    terms_of_service=settings.TOS,
    contact=settings.CONTACT,
    license_info=settings.LICENSE,
)


class Task(BaseModel):
    description: str
    priority: int = 1


@app.post("/tasks/")
async def create_task(task: Task):
    # Here we'll add logic to create a new task
    return {"task": task, "status": "created"}


@app.get("/")
async def root():
    return {"message": "Welcome to the Multi-Agent System API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
