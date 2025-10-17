from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from models import ResponseEnums, AdminModel, CompanyModel

dataRouter = APIRouter(prefix="/data", tags=["data"])


@dataRouter.get("/start/{company_name}")
async def InitiateCompany(request: Request, company_name:str, Admin_name: str|None = None, Admin_password: str|None = None):
    if Admin_name is None or Admin_password is None:
        return JSONResponse(content={
            "Message": ResponseEnums.AUTHENTICATION_FAILED.value
        },
        status_code=status.HTTP_403_FORBIDDEN,
        )
    
    adminModel = AdminModel.create_instance(
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

    companyModel = CompanyModel.create_instance(
                            db_client= request.app.db_client
                            )
    
    company = companyModel.get_company_or_create_one(
        company_name = company_name
    )

    
    

    
     