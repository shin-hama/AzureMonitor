from typing import Optional
from sqlalchemy.orm import Session

from azure_monitor.models.issue import Issue


def get_issues(db: Session, skip: int = 0, limit: int = 100) -> list[Issue]:
    return db.query(Issue).offset(skip).limit(limit).all()


def get_issue(db: Session, id: int) -> Optional[Issue]:
    return db.query(Issue).filter_by(id=id).first()


def create_issue(db: Session, issue: Issue) -> None:
    db.add(issue)
    db.commit()
    db.refresh(issue)

    return


def update_issue(db: Session, issue_update: Issue) -> None:
    db.merge(issue_update)

    db.commit()
