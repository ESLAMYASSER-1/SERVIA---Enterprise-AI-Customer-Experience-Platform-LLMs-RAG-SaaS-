from dotenv import load_dotenv
from contextlib import asynccontextmanager
from logging import getLogger

from pymongo import AsyncMongoClient

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

    app.llmService = LLMService.initialize_service()
    if not app.llmService:
        yield
        print("🛑 App Forced to shutting down Can't Initialize Embedding model")


    yield
    # Shutdown code
    print("🛑 App shutting down...")
    await app.mongo_conn.close()




app = FastAPI(lifespan=lifespan)


app.include_router(baseRouter)
app.include_router(dataRouter)

