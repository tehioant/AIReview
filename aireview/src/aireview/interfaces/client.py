import requests

class Client:

    url: str
    bearer_token: str
    headers: dict

    def __init__(self, url, bearer_token):
        self.url = url
        self.bearer_token = bearer_token
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "accept": "application/json",
        }

    def get(self):
        pass

    def getResponse(self):
        pass


    def post(self, payload):
        response = requests.post(self.url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()