from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UVICORN_")
    host: str = Field("0.0.0.0", description="Uvicorn server deploy host", env="HOST")
    port: int = Field(8000, description="Uvicorn server deploy port", env="PORT")


class HandsModelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HANDS_")

    path: str = Field(
        "../../models/model.pickle",
        description="Path to hands random forest model",
        env="PATH",
    )


class ChatGPTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHATGPT_")
    key: str = Field(..., description="Chat gpt api key", env="KEY")


class DeviceSettings(BaseSettings):
    idx: int = 0


class Settings(BaseSettings):
    logging_level: str = Field("DEBUG", description="Logging level", env="LOGLEVEL")
    hands: HandsModelSettings = HandsModelSettings()
    device: DeviceSettings = DeviceSettings()
    server: ServerSettings = ServerSettings()
    chat: ChatGPTSettings = ChatGPTSettings()


settings = Settings()
