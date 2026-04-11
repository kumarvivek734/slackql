from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    SLACK_BOT_TOKEN: SecretStr
    SLACK_SIGNING_SECRET: SecretStr
    SLACK_APP_TOKEN: SecretStr
    
    GEMINI_API_KEY: SecretStr
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    DATABASE_URL: str
    DB_MAX_ROWS:int = 100
    DB_QUERY_TIMEOUT_SECONDS: int = 10
    
    APP_ENV: str = 'development'
    LOG_LEVEL: str = 'INFO'
    PORT: int = 3000
    
settings = Settings()

