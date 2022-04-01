from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.config import DATABASE_URL


Base = declarative_base()


engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})


def connect_db():
    engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
    session = Session(bind=engine.connect())
    return session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password_hash = Column(String)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    description = Column(String)
    created_at = Column(String, default=datetime.utcnow())

    user = relationship('User', backref='projects')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    project_id = Column(Integer, ForeignKey('projects.id'), index=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    description = Column(String)
    task_status = Column(String, default='to do')
    created_at = Column(String, default=datetime.utcnow())
    dead_line = Column(Date)

    project = relationship('Project', backref='tasks')
    user = relationship('User', backref='tasks')


class TaskProject(Base):
    __tablename__ = 'taskproject'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), index=True, unique=True)
    project_id = Column(Integer, ForeignKey('projects.id'))


class TaskUser(Base):
    __tablename__ = 'taskuser'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


class ProjectUser(Base):
    __tablename__ = 'projectuser'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

