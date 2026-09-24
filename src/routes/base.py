from fastapi import APIRouter

baseRouter = APIRouter(tags=["base"])



@baseRouter.get("/")
async def FirstLanding():
    return {"message": "Welcome To CSAB APP"}