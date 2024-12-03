from pydantic_settings import BaseSettings

class AIReviewSettings(BaseSettings):
    dust_api_key: str
    github_token: str
    claude_id: str
    workspace_id: str
    max_dust_calls: int = 10

    class AIReviewSettings:
        env_file = ".env"