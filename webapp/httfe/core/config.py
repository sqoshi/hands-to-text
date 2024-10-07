from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class HandsModelSettings(BaseSettings):
    path: str = "../../models/model.pickle"


class DeviceSettings(BaseSettings):
    idx: int = 0


class Settings(BaseSettings):
    logging_level: str = "DEBUG"
    hands: HandsModelSettings = HandsModelSettings()
    device: DeviceSettings = DeviceSettings()
    server: ServerSettings = ServerSettings()


settings = Settings()
