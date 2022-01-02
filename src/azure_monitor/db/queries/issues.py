from sqlalchemy.orm import Session

from azure_monitor.models.issue import Issue


def get_issues(db: Session, skip: int = 0, limit: int = 100) -> list[Issue]:
    return db.query(Issue).offset(skip).limit(limit).all()


def create_issue(db: Session, issue: Issue) -> None:
    db.add(issue)
    db.commit()
    db.refresh(issue)

    return
