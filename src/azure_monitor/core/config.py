import os
from dotenv import load_dotenv


load_dotenv()

# Fill in with your personal access token and org URL
AZURE_DEVOPS_PAT = os.environ.get("AZURE_PAT", "")
AZURE_ORGANIZATION = f'https://dev.azure.com/{os.environ.get("AZURE_ORGANIZATION", "")}'
