from sqlalchemy.orm import Session

from azure_monitor.models.task import Task


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    return db.query(Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: Task) -> None:
    db.add(task)
    db.commit()
    db.refresh(task)

    return
