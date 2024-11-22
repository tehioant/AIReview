import os

from aireview.domain.assistant import Assistant
from aireview.interfaces.az_devops import AzureDevopsClient
from aireview.models.llms.llm_model import LlmModel


def main():
    print("Hello World")

    claude = LlmModel(os.getenv("claude_id"), os.getenv("dust_api_key"), "https://dust.tt/api/v1/w/SB0HhCoUEW/assistant/conversations")
    dust_assistant = Assistant("claude_agent", claude)

    azdevops = AzureDevopsClient()
    azdevops.get_projects()
    # response = dust_assistant.create_conversation("Hello, tell me about yourself")
    # print(dust_assistant.get_message(response))


if __name__ == "__main__":
    main()