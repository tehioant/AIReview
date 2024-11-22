import requests


class GithubClient:

    base_url = "https://api.github.com"
    def __init__(self):
        pass

    def get_repositories(self):
        url = f"{self.base_url}/users/tehioant/repos"
        response = requests.get(url)

        if response.status_code == 200:
            repositories_data = response.json()
            return repositories_data
        else:
            return None