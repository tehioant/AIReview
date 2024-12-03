from graphql import print_schema

from aireview.domain.services.code_analyzer import CodeAnalyzer
from aireview.infrastructure.github_client import GitHubClient


class ReviewController:
    def __init__(
            self,
            code_analyzer: CodeAnalyzer,
            github_client: GitHubClient
    ):
        self._analyzer = code_analyzer
        self._github = github_client

    async def review_pull_request(self, pr_id: int) -> None:
        pull_request = await self._github.get_pull_request(pr_id)
        review = self._analyzer.analyze_code(pull_request)
        await self._github.submit_review(pr_id, review)