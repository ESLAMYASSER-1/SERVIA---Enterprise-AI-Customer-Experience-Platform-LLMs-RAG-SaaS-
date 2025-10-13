from dotenv import load_dotenv
from contextlib import asynccontextmanager

from pymongo import AsyncMongoClient

from helpers import Settings

from fastapi import FastAPI
from routes import baseRouter, dataRouter

load_dotenv()
settings = Settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Startup code
    print("🚀 App starting up...")
    app.mongo_conn = AsyncMongoClient(settings.MONGO_URL)
    app.db_client = app.mongo_conn[settings.MONGO_DB]


    yield
    # Shutdown code
    print("🛑 App shutting down...")
    await app.mongo_conn.close()




app = FastAPI(lifespan=lifespan)


app.include_router(baseRouter)
app.include_router(dataRouter)

