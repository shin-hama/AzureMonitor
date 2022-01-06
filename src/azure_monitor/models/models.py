import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func

from azure_monitor.db.db import Base


class BaseModel:
    created = sa.Column(sa.DateTime, nullable=False)
    updated = sa.Column(sa.DateTime, nullable=False)


class Issue(Base, BaseModel):
    __tablename__ = "issues"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String(512), nullable=False)
    ticket = sa.Column(sa.Integer, unique=True)

    tasks = relationship("Task", back_populates="owner")


class Task(Base, BaseModel):
    __tablename__ = "tasks"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(512), unique=True)
    owner_id = sa.Column(sa.Integer, ForeignKey("issues.id"))

    owner = relationship("Issue", back_populates="tasks")
