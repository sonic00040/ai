from pydantic_settings import BaseSettings, SettingsConfigDict

import os

# Construct the absolute path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=dotenv_path, extra='ignore')

    TELEGRAM_BOT_TOKEN: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GOOGLE_API_KEY: str
    WEBHOOK_DOMAIN: str = "https://your-domain.com"

settings = Settings()