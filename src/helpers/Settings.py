from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_VERSION: str
    APP_NAME: str

    MONGO_URL: str
    MONGO_DB: str
    MONGODB_ADMIN_COLLECTION: str = "ADMIN"
    MONGODB_COMPANY_COLLECTION: str = "COMPANY"
    MONGODB_CHUNKS_COLLECTION: str = "CHUNKS"

    ASSETS_FOLDER: str
    RAW_DATA_FOLDER:str = "RAW_DATA"
    RAW_DATA_FILE_NAME: str = "CSAB.csv"

    GOOGLE_SHEET_URL: str

    class Config:
        env_file = ".env"

