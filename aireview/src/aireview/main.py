import os

from aireview.domain.assistant import Assistant
from aireview.interfaces.github import GithubClient
from aireview.models.llms.llm_model import LlmModel


def main():
    print("Hello World")

    claude = LlmModel(os.getenv("claude_id"), os.getenv("dust_api_key"), "https://dust.tt/api/v1/w/SB0HhCoUEW/assistant/conversations")
    dust_assistant = Assistant("claude_agent", claude)

    azdevops = GithubClient()
    print(azdevops.get_repositories())
    # response = dust_assistant.create_conversation("Hello, tell me about yourself")
    # print(dust_assistant.get_message(response))


if __name__ == "__main__":
    main()