from datetime import (
    datetime,
    timedelta,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from app.models.project_models import ProjectCreate, ProjectEdit, TaskCreate, ProjectForm, TaskForm
from app.models.auth_models import User as UserForm
from app.models.user_models import connect_db, Project, Task, TaskProject, TaskUser, ProjectUser, User
from sqlalchemy.orm import Session


class ProjectService:

    def __init__(self, session: Session = Depends(connect_db)):
        self.session = session

    def create_project(self, user_id: int, project_info: ProjectCreate):  # Созадание проекта
        project = Project(
            user_id=user_id,
            project_name=project_info.projectName,
            description=project_info.projDesc
        )
        self.session.add(project)
        self.session.commit()
        project_user = ProjectUser(
            project_id=project.id,
            user_id=user_id
        )
        self.session.add(project_user)
        self.session.commit()
        project_form = ProjectForm(
            projectName=project_info.projectName,
            projDesc=project_info.projDesc,
            id=project.id,
            director_id=user_id
        )
        return project_form

    def get_projects(self, user_id: int):  # Получение списка проектвов созданных ползователем
        return self.session.query(Project.id).filter(Project.user_id == user_id).all()

    def get_all_projects(self, user_id: int):  # Получение всех проектов где учавствует пользователь
        projects_id = self.session.query(ProjectUser).filter(ProjectUser.user_id == user_id).all()
        projects = []
        for i in projects_id:
            prj_id = i.project_id
            project__ = self.session.query(Project).filter(Project.id == prj_id).first()
            project_form = ProjectForm(
                projectName=project__.project_name,
                projDesc=project__.description,
                id=project__.id,
                director_id=project__.user_id
            )
            projects.append(project_form)
        return projects

    def add_user_project(self, username: str, project_id: int, director_id: int):
        user_dir = self.session.query(Project).filter(Project.id == project_id).first()
        user_dir = user_dir.user_id
        exception = HTTPException(
            status_code=403,
            detail='No roots')
        if user_dir != director_id:
            raise exception
        user_id = self.session.query(User).filter(User.username == username).first()
        user_id = user_id.id
        proj_user = ProjectUser(
            project_id=project_id,
            user_id=user_id
        )
        self.session.add(proj_user)
        self.session.commit()
        return self.session.query(User).filter(User.id == proj_user.user_id).first()

    def get_project(self, project_id: int):  # Получение проекта по id
        return self.session.query(Project).filter(Project.id == project_id).first()

    def get_tasks(self, project_id: int):  # Получение задач из проекта
        return self.session.query(Task).filter(Task.project_id == project_id).all()

    def edit_project(self, project_info: ProjectEdit):  # Дописать редактирование проекта
        pass


class TaskService(ProjectService):

    def create_task(self, user_id: int, task_info: TaskCreate):
        task = Task(
            task_name=task_info.task_name,
            project_id=task_info.project_id,
            user_id=user_id,
            description=task_info.description,
            dead_line=task_info.deadline,
        )
        self.session.add(task)
        self.session.commit()
        task_project = TaskProject(
            task_id=task.id,
            project_id=task_info.project_id
        )
        self.session.add(task_project)
        self.session.commit()
        task_user = TaskUser(
            task_id=task.id,
            user_id=user_id
        )
        self.session.add(task_user)
        self.session.commit()
        task_form = TaskForm(
            task_name=task.task_name,
            description=task.description,
            deadline=task.dead_line,
            project_id=task.project_id,
            task_status=task.task_status
        )
        return task_form

    def give_user_task(self, task_id: int, user_id: int, project_id):
        pass

    def get_task_users(self, task_id: int):
        users_id = self.session.query(TaskUser).filter(TaskUser.task_id == task_id).all()
        users = []
        for i in users_id:
            usr_id = i.user_id
            user__ = self.session.query(User).filter(User.id == usr_id).first()
            user_form = UserForm(
                email=user__.email,
                username=user__.username,
                id=user__.id
            )
            users.append(user_form)
        return users

    def get_tasks_from_project(self, project_id: int, director_id: int):
        project_director_id = (self.session.query(Project).filter(Project.id == project_id).first()).user_id
        exception = HTTPException(
            status_code=403,
            detail='No roots')
        if project_director_id != director_id:
            raise exception
        tasks_id = self.session.query(TaskProject).filter(TaskProject.project_id == project_id).all()
        tasks = []
        for i in tasks_id:
            tsk_id = i.task_id
            task__ = self.session.query(Task).filter(Task.id == tsk_id).first()
            task_form = TaskForm(
                task_name=task__.task_name,
                description=task__.description,
                deadline=task__.dead_line,
                project_id=task__.project_id,
                task_status=task__.task_status,
                id=task__.id
            )
            tasks.append(task_form)
        return tasks

    def get_tasks(self, user_id: int):
        tasks_id = self.session.query(TaskUser).filter(TaskUser.user_id == user_id).all()
        tasks = []
        for i in tasks_id:
            tsk_id = i.task_id
            task__ = self.session.query(Task).filter(Task.id == tsk_id).first()
            task_form = TaskForm(
                task_name=task__.task_name,
                description=task__.description,
                deadline=task__.dead_line,
                project_id=task__.project_id,
                task_status=task__.task_status,
                id=task__.id
            )
            tasks.append(task_form)

        def key_sort(key: Task):
            return key.deadline

        return sorted(tasks, key=key_sort)
