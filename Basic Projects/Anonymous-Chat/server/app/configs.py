from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_password: str = "rex000777"
    database_name: str = "postgres"
    database_username: str = "postgres"

settings = Settings()





