from typing import Iterator
from contextlib import contextmanager

from sqlalchemy.orm.session import Session

from .db import SessionLocal


@contextmanager
def get_db() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
