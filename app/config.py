from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_region: str
    dynamodb_table: str
    s3_bucket: str

    class Config:
        env_file = ".env"

settings = Settings()

