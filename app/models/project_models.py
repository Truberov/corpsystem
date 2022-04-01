from pydantic import BaseModel
from datetime import date


class ProjectCreate(BaseModel):
    projectName: str
    projDesc: str


class ProjectForm(ProjectCreate):
    id: int
    director_id: int

class ProjectEdit(ProjectCreate):
    pass


class TaskCreate(BaseModel):
    task_name: str
    description: str
    deadline: date


class TaskForm(TaskCreate):
    pass


class UserProjectInfo(BaseModel):
    user_name: str