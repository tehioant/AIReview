from abc import ABC
from typing import Dict, Any

from aireview.infrastructure.llm_client import LLMClient


class DustClient(LLMClient, ABC):

    def __init__(self, api_key: str, agent_id: str):
        super().__init__(self._as_connection_url())
        self._api_key = api_key
        self._agent_id = agent_id

    async def analyze(self, prompt: str) -> Dict[str, Any]:
        # Assume this method sends request to Dust API
        # and returns parsed response
        pass

    def _as_connection_url(self) -> str:
        return f"https://dust.tt/api/v1/w/{woarkspaceid}"
