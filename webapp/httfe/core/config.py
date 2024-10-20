from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UVICORN_")
    host: str = Field(
        "0.0.0.0",
        description="Uvicorn server deploy host",
        json_schema_extra={"env": "HOST"},
    )
    port: int = Field(
        8000,
        description="Uvicorn server deploy port",
        json_schema_extra={"env": "PORT"},
    )


class HandsModelSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HANDS_")

    path: str = Field(
        "/home/piotr/Workspaces/studies/htt-models/models/rf.pickle",
        description="Path to hands random forest model",
        json_schema_extra={"env": "PATH"},
    )


class ChatGPTSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CHATGPT_")
    key: str = Field(
        ..., description="Chat gpt api key", json_schema_extra={"env": "KEY"}
    )


class DeviceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DEVICE_")

    idx: int = Field(0, description="Camera device id", json_schema_extra={"env": "ID"})


class Settings(BaseSettings):
    logging_level: str = Field(
        "DEBUG", description="Logging level", json_schema_extra={"env": "LOGLEVEL"}
    )
    hands: HandsModelSettings = HandsModelSettings()
    device: DeviceSettings = DeviceSettings()
    server: ServerSettings = ServerSettings()
    chat: ChatGPTSettings = ChatGPTSettings()


_settings = None


def settings() -> Settings:
    global _settings
    if not _settings:
        _settings = Settings()
    return _settings
