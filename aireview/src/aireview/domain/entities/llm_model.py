


class LlmModel:

    id: str
    api_key: str
    url: str

    def __init__(self, id, api_key, url):
        self.id = id
        self.api_key = api_key
        self.url = url