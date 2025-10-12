from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI
from helpers import Settings
from routes import baseRouter, dataRouter

load_dotenv()
settings = Settings()


async def lifespan(app:FastAPI):
    # Startup code
    print("🚀 App starting up...")
    yield
    # Shutdown code
    print("🛑 App shutting down...")




app = FastAPI(lifespan=lifespan)


app.include_router(baseRouter)
app.include_router(dataRouter)

