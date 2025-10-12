from dotenv import load_dotenv
from fastapi import FastAPI
from helpers import Settings
from routes import baseRouter

load_dotenv()
settings = Settings()

app = FastAPI()


app.include_router(baseRouter)



