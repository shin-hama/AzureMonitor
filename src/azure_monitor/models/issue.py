import sqlalchemy as sa
from sqlalchemy.orm import relationship

from azure_monitor.db.db import Base


class Issue(Base):
    __tablename__ = "issues"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    title = sa.Column(sa.String(512), nullable=False)
    ticket = sa.Column(sa.Integer, unique=True)

    tasks = relationship("Task", back_populates="owner")
