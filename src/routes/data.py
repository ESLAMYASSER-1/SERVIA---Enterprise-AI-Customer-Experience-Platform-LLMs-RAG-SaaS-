from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models import ResponseEnums

dataRouter = APIRouter(prefix="/data", tags=["data"])


@dataRouter.get("/upload/{company_name}")
async def upload(company_name:str, Admin_name: str|None = None, Admin_password: str|None = None):
    if Admin_name or Admin_password is None:
        return JSONResponse(content={
            "Message": ResponseEnums.AUTHENTICATION_FAILED.value
        },
        status_code=status.HTTP_403_FORBIDDEN,
        )
    
    
    
     