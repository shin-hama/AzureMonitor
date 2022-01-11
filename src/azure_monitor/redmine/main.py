from logging import getLogger, DEBUG, StreamHandler
from typing import Any, Union

from redminelib import Redmine, resources

from azure_monitor.db.queries.issues import get_issues
from azure_monitor.db.utils import get_db
from azure_monitor.core.config import REDMINE_API_KEY, REDMINE_PROJECT, REDMINE_URL
from azure_monitor.models.models import Issue
from azure_monitor.utils import proxy


logger = getLogger(__name__)
logger.setLevel(DEBUG)
sh = StreamHandler()
logger.addHandler(sh)


class RedmineClinet:
    def __init__(self) -> None:
        self.client = Redmine(
            url=REDMINE_URL,
            key=REDMINE_API_KEY,
        )

    def update_ticket(self, ticket_id: Union[int, str], **kwargs: Any) -> resources.Issue:
        """Update ticket.

        Parameters
        ----------
        The parameter name of kwargs as below.
        - subject (string): Issue subject
        - description (string): Issue description
        - notes (string): journal note that is called as history
        - parent_issue_id (int): Parent issue id.
        - done_ratio (int): Issue done ratio.

        Return
        ------
        issue: redminelib.resources.Issue
            The updated issue
        """
        logger.debug(f"Update: #{ticket_id}, kwargs: {kwargs}")
        # self.client.issue.update(ticket_id, **kwargs)

        issue = self.client.issue.get(ticket_id)

        return issue

    def create_ticket(self, subject: str, description: str, **kwargs: Any) -> resources.Issue:
        me = self.client.user.get("current")
        logger.debug(f"proj: {REDMINE_PROJECT}, ticket: {subject}, desc: {description}, kwargs: {kwargs}, me: {me.id}")
        issue = self.client.issue.create(
            project_id=REDMINE_PROJECT,
            subject=subject,
            description=description,
            tracker_id=2,
            assigned_to_id=me.id,
            is_private=True,
        )

        return issue


def register_ticket():
    with get_db() as session:
        issues = get_issues(session)
        for issue in issues:
            if issue.ticket is None:
                print("No ticket, register new ticket")
            else:
                print("Exists Ticket, update ticket contents if you need")


def build_ticket(issue: Issue):
    title: str = issue.title
    child_titles = [task.title for task in issue.tasks]
    description = "¥n".join(child_titles)

    ticket = {"title": title, "description": description}
    return ticket


if __name__ == "__main__":
    # with get_db() as session:
    #     for i in get_issues(session):
    #         print(build_ticket(i))
    proxy.remove()
    redmine = RedmineClinet()
    # redmine.create_ticket("test", "sample desxription")
    proxy.setup()
