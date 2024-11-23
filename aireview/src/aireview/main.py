import os

from aireview.config import Config
from aireview.domain.assistant import Assistant
from aireview.domain.services.code_analyzer import CodeAnalyzer
from aireview.infrastructure.dust_client import DustClient
from aireview.infrastructure.github_client import GitHubClient
from aireview.interfaces.github import GithubClient
from aireview.models.llms.llm_model import LlmModel


# def main():
#     print("Hello World")
#
#     claude = LlmModel(os.getenv("claude_id"), os.getenv("dust_api_key"), "https://dust.tt/api/v1/w/SB0HhCoUEW/assistant/conversations")
#     dust_assistant = Assistant("claude_agent", claude)
#
#     azdevops = GithubClient()
#     print(azdevops.get_repositories())
#     # response = dust_assistant.create_conversation("Hello, tell me about yourself")
#     # print(dust_assistant.get_message(response))

def main():
    config = Config()
    dust_client = DustClient(config.dust_api_key)
    github_client = GitHubClient(config.github_token)

    analyzer = CodeAnalyzer(dust_client)
    controller = ReviewController(analyzer, github_client)

    await controller.review_pull_request(pr_id=123)

if __name__ == "__main__":
    main()