import os

from azure.devops.connection import Connection
from azure.devops.v6_0.work_item_tracking import WorkItemTrackingClient, Wiql, WorkItemQueryResult
from dotenv import load_dotenv
from msrest.authentication import BasicAuthentication


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

# Get all work items where a type is issue
query = "Select * From WorkItems Where [System.WorkItemType] = 'Issue'"
wiql = Wiql(query)
test: WorkItemQueryResult = wi_client.query_by_wiql(wiql)
for i in test.work_items:
    print(i)
