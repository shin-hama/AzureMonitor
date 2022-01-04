from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

from azure_monitor.core.config import AZURE_DEVOPS_PAT, AZURE_ORGANIZATION


def create_connection() -> Connection:
    # Create a connection to the org
    credentials = BasicAuthentication("", AZURE_DEVOPS_PAT)
    connection = Connection(base_url=AZURE_ORGANIZATION, creds=credentials)
    return connection
