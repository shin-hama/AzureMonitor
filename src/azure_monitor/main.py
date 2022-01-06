from typing import Callable, Optional

from sqlalchemy.orm.session import Session
from azure_monitor.azure_devops.work_items import generate_issues
from azure_monitor.db.queries.issues import create_issue, get_issue, update_issue
from azure_monitor.db.utils import get_db
from azure_monitor.models.models import Issue


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
    import pytz

    utc = pytz.UTC

    for issue in generate_issues():
        issue_db = _get_issue(issue.id)
        if issue_db is None:
            _create_issue(issue)
        else:
            if issue.updated > utc.localize(issue_db.updated):
                print("update")
                _update_issue(issue)


if __name__ == "__main__":
    main()
