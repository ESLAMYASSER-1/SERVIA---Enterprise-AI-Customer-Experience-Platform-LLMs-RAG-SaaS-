from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from models import ResponseEnums, AdminModel

dataRouter = APIRouter(prefix="/data", tags=["data"])


@dataRouter.get("/upload/{company_name}")
async def upload(request: Request, company_name:str, Admin_name: str|None = None, Admin_password: str|None = None):
    if Admin_name is None or Admin_password is None:
        return JSONResponse(content={
            "Message": ResponseEnums.AUTHENTICATION_FAILED.value
        },
        status_code=status.HTTP_403_FORBIDDEN,
        )
    
    adminModel = AdminModel(
                            db_client=request.app.db_client
                            )

    adminIsExist = await adminModel.check_if_admin_exists(
                            Admin_name=Admin_name,
                            Admin_password=Admin_password
                            )
    
    if not adminIsExist :
        return JSONResponse(content={
            "Message": ResponseEnums.AUTHENTICATION_FAILED.value
        },
        status_code=status.HTTP_403_FORBIDDEN,
        )
    
    return JSONResponse(content={
            "Message": ResponseEnums.AUTHENTICATION_SUCCESS.value
        },
        status_code=status.HTTP_202_ACCEPTED,
        )
    
    

    
     