import json
import os
from pathlib import Path

from azure.devops.connection import Connection
from azure.devops.v6_0.work_item_tracking import WorkItemTrackingClient, Wiql, WorkItemQueryResult
from azure.devops.v6_0.work_item_tracking.models import WorkItem
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication


def perse_id_from_work_item_url(url: str):
    try:
        id = Path(url).name
        return int(id)
    except Exception:
        return


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
for i in result.work_items:
    detail = get_work_item(237, expand="Relations")
    print(json.dumps(detail.as_dict(), indent=2))
    child_task_ids: list[int] = [perse_id_from_work_item_url(task.url) for task in detail.relations]
    for child in child_task_ids:
        child_item = get_work_item(child)
        print(child_item.fields["System.Title"])

    break
