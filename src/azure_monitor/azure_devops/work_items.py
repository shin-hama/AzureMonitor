from pathlib import Path
from typing import Iterator

from azure.devops.connection import Connection
from azure.devops.v6_0.work_item_tracking import WorkItemTrackingClient, Wiql, WorkItemQueryResult
from azure.devops.v6_0.work_item_tracking.models import WorkItem, WorkItemReference, WorkItemRelation

from .utils import create_connection
from azure_monitor.models.models import Issue, Task


def parse_id_from_work_item_url(url: str):
    try:
        id = Path(url).name
        return int(id)
    except Exception:
        return None


def checkIsChild(item: WorkItemRelation) -> bool:
    """Check the argument is child or not"""
    return item.attributes.get("name") == "Child"


class WorkItemClient:
    def __init__(self, con: Connection) -> None:
        self.client: WorkItemTrackingClient = con.clients_v6_0.get_work_item_tracking_client()

    def get_work_item(self, id: int, project=None, fields=None, as_of=None, expand=None) -> WorkItem:
        wi = self.client.get_work_item(id, project, fields, as_of, expand)
        return wi

    def get_all_issues(self) -> WorkItemQueryResult:
        # Get all work items where a type is issue
        query = "Select * From WorkItems Where [System.WorkItemType] = 'Issue'"
        wiql = Wiql(query)
        return self.client.query_by_wiql(wiql)


class WorkItemParser:
    def __init__(self) -> None:
        # self.wi_client = WorkItemClient()
        pass

    @staticmethod
    def build_issue(item: WorkItem):
        issue = Issue(id=item.id, title=item.fields.get("System.Title"))
        return issue

    @staticmethod
    def build_task(item: WorkItem):
        task = Task(id=item.id, title=item.fields.get("System.Title"))
        return task

    @staticmethod
    def parse_child(relations: list[WorkItemRelation]):
        child_task_ids: list[int] = []
        for task in relations:
            if checkIsChild(task):
                child_task_ids.append(parse_id_from_work_item_url(task))

        return child_task_ids


def generate_issues() -> Iterator[Issue]:
    # Get a client (the "core" client provides access to projects, teams, etc)
    connection = create_connection()
    wi_client = WorkItemClient(connection)

    result: WorkItemQueryResult = wi_client.get_all_issues()
    if result is None:
        return None

    item: WorkItemReference
    for item in result.work_items:
        # register all issues
        detail = wi_client.get_work_item(item.id, expand="Relations")
        issue = WorkItemParser.build_issue(detail)

        if detail.relations is not None and len(detail.relations) > 0:
            # If issue has child task, get detail of tasks.
            child_task_ids = WorkItemParser.parse_child(detail.relations)

            children: list[Task] = []
            for child in child_task_ids:
                if child is None:
                    continue
                child_item = wi_client.get_work_item(child)
                task = WorkItemParser.build_task(child_item)
                children.append(task)
            issue.tasks = children

        yield issue
