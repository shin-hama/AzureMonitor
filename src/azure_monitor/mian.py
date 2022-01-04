from typing import Callable, Optional

from sqlalchemy.orm.session import Session
from azure_monitor.azure.work_items import generate_issues
from azure_monitor.db.queries.issues import create_issue, get_issue, update_issue
from azure_monitor.db.utils import get_db
from azure_monitor.models.issue import Issue


def process_db(callback: Callable[[Session], Optional[Issue]]):
    with get_db() as session:
        try:
            return callback(session)
        except Exception:
            session.rollback()
        finally:
            session.close()


def _get_issue(id: int):
    def func(session: Session):
        return get_issue(session, id)

    return process_db(func)


def _create_issue(issue: Issue):
    def func(session: Session):
        create_issue(session, issue)

    process_db(func)


def _update_issue(issue: Issue):
    def func(session: Session):
        update_issue(session, issue)

    process_db(func)


def main():
    for issue in generate_issues():
        issue = _get_issue(issue.id)
        if issue is None:
            _create_issue(issue)
        else:
            _update_issue(issue)
