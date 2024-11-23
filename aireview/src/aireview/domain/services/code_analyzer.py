from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.review import Review


class CodeAnalyzer:
    def __init__(self, dust_client, call_limit: int = 10):
        self._dust_client = dust_client
        self._call_count = 0
        self._call_limit = call_limit

    async def analyze_code(self, pull_request: PullRequest) -> Review:
        if self._call_count >= self._call_limit:
            raise Exception("Dust API call limit reached")

        prompt = self._build_analysis_prompt(pull_request)
        analysis = await self._dust_client.analyze(prompt)
        self._call_count += 1

        return self._parse_analysis(analysis)

    def _build_analysis_prompt(self, pull_request):
        pass

    def _parse_analysis(self, analysis):
        return Review