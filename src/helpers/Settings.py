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

    WEAVIATE_URL: str = "http://localhost:8080"
    WEAVIATE_GENERAL_INFO_COLLECTION:str = "GENERAL_INFO"
    WEAVIATE_ITEMS_COLLECTION:str = "ITEMS"

    ASSETS_FOLDER: str = "assets/"
    RAW_DATA_FOLDER:str = "RAW_DATA"
    RAW_DATA_FILE_NAME: str = "CSAB.csv"

    GOOGLE_SHEET_URL: str

    EMBEDDING_MODEL_FOLDER: str = "EMBEDDING_MODELS"
    EMBEDDING_PROVIDER: str|list = ["INTFLOAT"]
    EMBEDDING_MODEL: str|list = ["intfloat/multilingual-e5-large"]
    EMBEDDING_MODEL_SIZE: int


    VLLM_PORT: str|int = "8000"
    VLLM_URL: str = f"http://localhost:{VLLM_PORT}/v1"
    ENABLE_THINKING: bool = False

    class ConfigDict:
        env_file = ".env"

