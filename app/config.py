from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# Reading a .env file
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

# `@lru_cache`` modifies the function it decorates to return the same 
# value that was returned the first time, instead of computing it again

@lru_cache
def get_settings():
    return Settings()
