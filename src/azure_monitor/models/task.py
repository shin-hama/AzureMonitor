import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from azure_monitor.db.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(512), unique=True)
    owner_id = sa.Column(sa.Integer, ForeignKey("issues.id"))

    owner = relationship("Issue", back_populates="tasks")
