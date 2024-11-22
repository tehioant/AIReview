import os

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint

class AzureDevopsClient:

    url: str = "https://dev.azure.com/la-parisienne-git/"
    client: any

    def __init__(self):
        self.client = self._connect()

    def _connect(self):
        print(os.environ["az_devops_access_token"])
        credentials = BasicAuthentication('antoine.tehio@wakam.com', "")
        connection = Connection(base_url=self.url, creds=credentials)
        return connection.clients.get_core_client()

    def get_projects(self):
        get_projects_response = self.client.get_projects()
        index = 0
        while get_projects_response is not None:
            for project in get_projects_response.value:
                pprint.pprint("[" + str(index) + "] " + project.name)
                index += 1
            if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
                # Get the next page of projects
                get_projects_response = self.client.get_projects(continuation_token=get_projects_response.continuation_token)
            else:
                # All projects have been retrieved
                get_projects_response = None
