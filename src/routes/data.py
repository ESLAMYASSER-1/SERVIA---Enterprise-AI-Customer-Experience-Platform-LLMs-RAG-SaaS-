from fastapi import APIRouter, status, Request
from datetime import datetime
from fastapi.responses import JSONResponse
from helpers import Settings
from models import ResponseEnums, AdminModel, CompanyModel, ChunkModel
from controllers import DataController
from models.db_schemas import Chunk

dataRouter = APIRouter(prefix="/data", tags=["data"])
settings = Settings()

@dataRouter.get("/start/{company_name}")
async def InitiateCompany(request: Request, company_name:str, Admin_name: str|None = None, Admin_password: str|None = None):
    if Admin_name is None or Admin_password is None:
        return JSONResponse(content={
            "Message": ResponseEnums.AUTHENTICATION_FAILED.value
        },
        status_code=status.HTTP_403_FORBIDDEN,
        )
    
    adminModel = await AdminModel.create_instance(
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

    companyModel = await CompanyModel.create_instance(
                            db_client= request.app.db_client
                            )
    
    company = await companyModel.get_company_or_create_one(
        company_name = company_name
    )

    dataController = DataController()
    chunks = dataController.get_company_chunks(settings.GOOGLE_SHEET_URL, company_name)

    if len(chunks) <= 0 :
        return JSONResponse(content={
            "Message": "Company data does not exist",
            "chunks": f"chunks len: {len(chunks)}"
        },
        status_code=status.HTTP_404_NOT_FOUND,
        )

    mod_chunks = [
        Chunk(
            company_name= company.Name,
            company_id= str(company.id),
            chunk_id= i,
            text= txt
        )
        for i, txt in enumerate(chunks, 1)
    ]

    chunkModel = await ChunkModel.create_instance(
                    db_client= request.app.db_client
                )
    
    out = await chunkModel.add_and_delete_chunks(
        chunks = mod_chunks,
        company_name = company.Name,
        company_id = str(company.id)
    )
    
    return JSONResponse(content={
        "message" : ResponseEnums.ADDED_TO_DATA_BASE.value,
    },
    status_code=status.HTTP_201_CREATED
    )
    



    
    

    
     