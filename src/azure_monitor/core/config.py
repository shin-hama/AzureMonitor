import os
from dotenv import load_dotenv


load_dotenv()


# Fill in with your personal access token and org URL
AZURE_DEVOPS_PAT = os.environ.get("AZURE_PAT", "")
AZURE_ORGANIZATION = f'https://dev.azure.com/{os.environ.get("AZURE_ORGANIZATION", "")}'

REDMINE_URL = os.environ.get("REDMINE_URL")
REDMINE_API_KEY = os.environ.get("REDMINE_API_KEY")
REDMINE_PROJECT = os.environ.get("REDMINE_PROJECT", "")

PROXY = os.environ.get("PROXY", "")
