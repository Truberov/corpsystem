from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status, Query,
)

from app.models import project_models, auth_models
from app.models.auth_models import User
from app.models.project_models import TaskCreate, TaskForm
from app.models.user_models import Task
from app.services.auth_services import get_current_user
from app.services.project_services import ProjectService, TaskService

router = APIRouter(
    prefix='/project',
    tags=['projects'],
)


@router.post(
    '/create/',
    response_model=project_models.ProjectForm,
    status_code=status.HTTP_201_CREATED,
)
def create(
        project_data: project_models.ProjectCreate,
        project_service: ProjectService = Depends(),
        user: auth_models.User = Depends(get_current_user),
):
    return project_service.create_project(user.id, project_data)


@router.get(
    '/get/',
    response_model=List[project_models.ProjectForm]
)
def get_projects(
        user: auth_models.User = Depends(get_current_user),
        project_service: ProjectService = Depends(),
):
    return project_service.get_all_projects(user.id)


@router.post(
    '/add_user/',
    response_model=auth_models.User,
    status_code=status.HTTP_201_CREATED,
)
def add_user(
        project_id: int = Query(..., description="Id проекта"),
        project_service: ProjectService = Depends(),
        user: auth_models.User = Depends(get_current_user),
        username: str = Query(..., description="Имя пользователя добавляемого в проект")
):
    return project_service.add_user_project(username, project_id, user.id)


@router.post(
    '/create_task',
    response_model=TaskForm,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
        task_info: TaskCreate,
        task_service: TaskService = Depends(),
        user: auth_models.User = Depends(get_current_user),
):
    return task_service.create_task(user.id, task_info)


@router.get(
    '/tasks/get',
    response_model=List[TaskForm]
)
def get_tasks(
        user: auth_models.User = Depends(get_current_user),
        task_service: TaskService = Depends(),
):
    return task_service.get_tasks(user.id)


@router.get(
    '/task-project/get',
    response_model=List[TaskForm]
)
def get_task_project(
        user: auth_models.User = Depends(get_current_user),
        task_service: TaskService = Depends(),
        project_id: int = Query(..., description="id проекта откуда запрашиваем задачи")
):
    return task_service.get_tasks_from_project(project_id, user.id)


@router.get(
    '/task-users/get',
    response_model=List[User]
)
def get_task_project(
        user: auth_models.User = Depends(get_current_user),
        task_service: TaskService = Depends(),
        task_id: int = Query(..., description="id проекта откуда запрашиваем задачи")
):
    return task_service.get_task_users(task_id)

