from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_level: str = "DEBUG"
    hands_model_path: str = "../../models/model.pickle"
    device_id: int = 0


settings = Settings()
