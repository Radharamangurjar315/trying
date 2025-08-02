# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str
    port:int
    GeminiKey:str
    Token:str
    class Config:
        env_file = ".env"

settings = Settings()
