from typing import Dict, Any

class DustClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def analyze(self, prompt: str) -> Dict[str, Any]:
        # Assume this method sends request to Dust API
        # and returns parsed response
        pass

    def _build_prompt(self, code: str) -> str:
        return f"""
        Please review this code focusing on:
        1. Naming conventions
        2. Code style/quality
        3. Indentation
        4. Documentation
        5. Test coverage

        Code:
        {code}
        """