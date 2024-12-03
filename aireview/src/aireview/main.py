import asyncio
import logging

from aireview.application.controllers.review_controller import ReviewController
from aireview.config import AIReviewSettings
from aireview.domain.services.code_analyzer import CodeAnalyzer
from aireview.infrastructure.dust_client import DustClient
from aireview.infrastructure.github_client import GitHubClient

logger = logging.getLogger(__name__)

def main(pull_request: int, config: AIReviewSettings = AIReviewSettings()):
    dust_client = DustClient(config.dust_api_key, config.claude_id, config.workspace_id)
    github_client = GitHubClient(config.github_token, "tehioant", "AIReview")
    analyzer = CodeAnalyzer(dust_client)
    controller = ReviewController(analyzer, github_client)

    asyncio.run(controller.review_pull_request(pr_id=pull_request))

if __name__ == "__main__":
    main(2)