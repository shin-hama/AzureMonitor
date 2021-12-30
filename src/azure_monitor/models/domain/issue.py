import sqlalchemy as sa

from azure_monitor.db.db import Base


class Issue(Base):
    __tablename__ = "issues"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    ticket = sa.Column(sa.Integer, unique=True)
