from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    vk_token: str = Field(..., env="VK_TOKEN")
    confirmation_token: str = Field(..., env="CONFIRMATION_TOKEN")
    group_id: str = Field(..., env="GROUP_ID")
    secret_key: str = Field(..., env="SECRET_KEY")
    api_version: str = "5.131"

    class Config:
        env_file = ".env"

settings = Settings()