from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status, Query,
)

from app.models import project_models, auth_models
from app.models.project_models import TaskCreate
from app.models.user_models import Task
from app.services.auth_services import get_current_user
from app.services.project_services import ProjectService

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
def get(
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
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
        task_info: TaskCreate,
        project_service: ProjectService = Depends(),
        user: auth_models.User = Depends(get_current_user),

)
