from azure_monitor.db.queries.issues import get_issues
from azure_monitor.db.utils import get_db
from azure_monitor.models.models import Issue


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


with get_db() as session:
    for i in get_issues(session):
        print(build_ticket(i))
