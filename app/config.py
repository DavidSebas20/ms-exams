from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_region: str
    dynamodb_table: str
    s3_bucket: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str

    class Config:
        env_file = ".env"

settings = Settings()