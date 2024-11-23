from pydantic_settings import BaseSettings

class Config(BaseSettings):
    dust_api_key: str
    github_token: str
    claude_id: str
    max_dust_calls: int = 10

    class Config:
        env_file = ".env"