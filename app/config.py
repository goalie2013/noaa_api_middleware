from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_hostname: str
    api_port: str
    api_token: str
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
    
settings = Settings()

# print(settings.api_token)
