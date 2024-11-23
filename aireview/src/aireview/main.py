import asyncio

from aireview.application.controllers.review_controller import ReviewController
from aireview.config import Config
from aireview.domain.services.code_analyzer import CodeAnalyzer
from aireview.infrastructure.dust_client import DustClient
from aireview.infrastructure.github_client import GitHubClient



def main():
    config = Config()
    # TODO: create dust agent for reviews
    dust_client = DustClient(config.dust_api_key)
    github_client = GitHubClient(config.github_token, "tehioant", "AIReview")

    analyzer = CodeAnalyzer(dust_client)
    controller = ReviewController(analyzer, github_client)

    asyncio.run(controller.review_pull_request(pr_id=1))

if __name__ == "__main__":
    main()