from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    SLEEP_TIME: list[int] = [7200, 10800]
    START_DELAY: list[int] = [5, 25]
    AUTO_TASK: bool = True
    TASKS_TO_DO: list[str] = ["paint20pixels", "leagueBonusSilver"]
    AUTO_DRAW: bool = True
    JOIN_TG_CHANNELS: bool = True
    CLAIM_REWARD: bool = True
    AUTO_UPGRADE: bool = True
    REF_ID: str = 'f464869246'
    IGNORED_BOOSTS: list[str] = ['paintReward']

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()
