from datetime import datetime

from aireview.interfaces.client import Client
from aireview.models.llms.llm_model import LlmModel
import pytz



class Assistant:

    name: str
    llm_model: LlmModel
    client: Client

    def __init__(self, name, llm_model):
        self.name = name
        self.llm_model = llm_model
        self.client = Client(llm_model.url, llm_model.api_key)

    def create_conversation(self, message):
        payload= {
            "title": None,
            "visibility": "unlisted",
            "message": {
                "content": message,
                "mentions": [{"configurationId": self.llm_model.id}],
                "context": {
                    "username": "automated",
                    "timezone": str(datetime.now(pytz.timezone("Europe/Paris")).tzinfo),
                    "fullName": "Automated Service",
                    "email": "no-reply@wakam.com",
                    "profilePictureUrl": None,
                    "origin": "api",
                },
            },
            "blocking": True,
        }
        return self.client.post(payload)

    def get_message(self, conversation):
        if 'content' in conversation['conversation']:
            return conversation['conversation']['content'][-1][-1]['content']
        else:
            return "Error: No message found"

    def send_message(self):
        pass