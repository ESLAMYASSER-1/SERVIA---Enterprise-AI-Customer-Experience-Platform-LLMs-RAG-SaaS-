from dotenv import load_dotenv
from contextlib import asynccontextmanager
from logging import getLogger

from pymongo import AsyncMongoClient
import weaviate 

from helpers import Settings, setup_logging

from fastapi import FastAPI
from routes import baseRouter, dataRouter

from domain.services import LLMService



load_dotenv()
settings = Settings()
setup_logging()

logger = getLogger(__name__)
logger.info("CSAP system started")

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Startup code
    print("🚀 App starting up...")
    app.mongo_conn = AsyncMongoClient(settings.MONGO_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DB]

    weaviate_params = weaviate.connect.ConnectionParams.from_url(url= settings.WEAVIATE_URL, grpc_port = 50051, )
    app.vdb_client = weaviate.WeaviateAsyncClient(connection_params= weaviate_params)
    await app.vdb_client.connect()

    app.llmService = LLMService.initialize_service()
    if not app.llmService:
        yield
        print("🛑 App Forced to shutting down Can't Initialize Embedding model")


    yield
    # Shutdown code
    print("🛑 App shutting down...")
    await app.mongo_conn.close()
    await app.vdb_client.close()




app = FastAPI(lifespan=lifespan)


app.include_router(baseRouter)
app.include_router(dataRouter)

