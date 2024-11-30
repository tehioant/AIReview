from abc import ABC

import requests
from aiohttp import payload_type
from sqlalchemy.util import await_only

from aireview.infrastructure.llm_client import LLMClient


class DustClient(LLMClient, ABC):

    _conversation_id: str = None

    def __init__(self, api_key: str, agent_id: str, workspace_id: str):
        self._api_key = api_key
        self._agent_id = agent_id
        self._workspace_id = workspace_id
        super().__init__(self._as_connection_url())

    def analyse(self, prompt: str):
        return self.create_conversation(prompt)

    def initialize(self, init_prompt: str):
        self._conversation_id = self.get_conversation_id(self.create_conversation(init_prompt))

    def _as_connection_url(self) -> str:
        return f"https://dust.tt/api/v1/w/{self._workspace_id}"

    def create_conversation(self, prompt: str):
        payload = {
            "title": "",
            "visibility": "unlisted",
            "message": {
                "content": prompt,
                "mentions": [{"configurationId": self._agent_id}],
                "context": {
                    "username": "automated",
                    "timezone": "Europe/Paris",
                    "fullName": "Automated Service",
                    "email": "no-reply@wakam.com",
                    "profilePictureUrl": "None",
                    "origin": "api"
                }
            },
            "blocking": True
        }
        response = requests.post(self.url + "/assistant/conversations", headers=self.get_headers(), json=payload)
        print(response.json())
        response.raise_for_status()
        return self.get_content(response.json())


    def send_message(self, prompt):
        payload = { "context": {
                        "origin": "api"
                        },
                    "content": prompt,
                    "mentions": ""
                }
        response = requests.post(self.url + f"/assistant/conversations/{self._conversation_id}/messages", headers=self.get_headers(), json=payload)
        print(response.json())
        response.raise_for_status()
        return self.get_content(response.json())

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

    def get_content(self, conversation):
        if 'content' in conversation['conversation']:
            return conversation['conversation']['content'][-1][-1]['content']
        else:
            return "Error: No message found"

    def get_conversation_id(self, conversation):
        if 'content' in conversation['id']:
            return conversation['conversation']['id']
        else:
            return "Error: No ID found"