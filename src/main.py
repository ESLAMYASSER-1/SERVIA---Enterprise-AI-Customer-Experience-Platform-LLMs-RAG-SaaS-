from dotenv import load_dotenv
from contextlib import asynccontextmanager
from logging import getLogger

from pymongo import AsyncMongoClient
import weaviate 

from helpers import Settings, setup_logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import baseRouter, dataRouter, nlpRouter






load_dotenv()
settings = Settings()
setup_logging()

logger = getLogger(__name__)
logger.info("CSAP system started")

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Startup code
    print("🚀 App starting up...")
    from domain.services import LLMService, VectorDBService
    
    app.mongo_conn = AsyncMongoClient(settings.MONGO_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DB]
    logger.info("########### 1 ###########")
    app.vdb_service = await VectorDBService.initialize_service()
    if not app.vdb_service:
        yield
        print("🛑 App Forced to shutting down Can't Initialize VDB service")
    logger.info("########### 2 ###########")
    
    app.llmService = LLMService.initialize_service()
    if not app.llmService:
        yield
        print("🛑 App Forced to shutting down Can't Initialize LLM Sercice")
    logger.info("########### 3 ###########")


    yield
    # Shutdown code
    print("🛑 App shutting down...")
    await app.mongo_conn.close()
    await app.vdb_service.close()




app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(baseRouter)
app.include_router(dataRouter)
app.include_router(nlpRouter)

