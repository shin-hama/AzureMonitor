import os
from pathlib import Path

from azure.devops.connection import Connection
from azure.devops.v6_0.work_item_tracking import WorkItemTrackingClient, Wiql, WorkItemQueryResult
from azure.devops.v6_0.work_item_tracking.models import WorkItem, WorkItemReference, WorkItemRelation
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication

from azure_monitor.models.issue import Issue
from azure_monitor.models.task import Task
from azure_monitor.db.queries.issues import create_issue, get_issue, update_issue
from azure_monitor.db.utils import get_db


def perse_id_from_work_item_url(url: str):
    try:
        id = Path(url).name
        return int(id)
    except Exception:
        return


def get_child_id_from_relation(item: WorkItemRelation):
    if item.attributes.get("name") == "Child":
        return perse_id_from_work_item_url(item.url)
    else:
        return None


load_dotenv()

# Fill in with your personal access token and org URL
personal_access_token = os.environ.get("AZURE_PAT", "")
organization_url = f'https://dev.azure.com/{os.environ.get("AZURE_ORGANIZATION", "")}'

# Create a connection to the org
credentials = BasicAuthentication("", personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()
core_client = connection.clients_v6_0.get_core_client()
wi_client: WorkItemTrackingClient = connection.clients_v6_0.get_work_item_tracking_client()


def get_work_item(id: int, project=None, fields=None, as_of=None, expand=None) -> WorkItem:
    wi = wi_client.get_work_item(id, project, fields, as_of, expand)
    return wi


# Get all work items where a type is issue
query = "Select * From WorkItems Where [System.WorkItemType] = 'Issue'"
wiql = Wiql(query)
result: WorkItemQueryResult = wi_client.query_by_wiql(wiql)
item: WorkItemReference
for item in result.work_items:
    # register all issues
    detail = get_work_item(item.id, expand="Relations")
    issue = Issue(id=detail.id, title=detail.fields["System.Title"])
    if detail.relations:
        child_task_ids: list[int] = [get_child_id_from_relation(task) for task in detail.relations]
        children: list[Task] = []
        for child in child_task_ids:
            if child is None:
                continue
            child_item = get_work_item(child)
            task = Task(id=child_item.id, title=child_item.fields["System.Title"])
            children.append(task)

        issue.tasks = children

    with get_db() as session:
        try:
            if get_issue(session, issue.id) is None:
                create_issue(session, issue)
            else:
                update_issue(session, issue)
        except:
            session.rollback()
