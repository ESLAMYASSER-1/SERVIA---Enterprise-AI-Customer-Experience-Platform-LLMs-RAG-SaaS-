from fastapi import APIRouter, status, Request
from datetime import datetime
from fastapi.responses import JSONResponse
from helpers import Settings
from models import ResponseEnums, AdminModel, CompanyModel, ChunkModel
from controllers import DataController
from models.db_schemas import Chunk

from weaviate.classes.data import DataObject

from logging import getLogger


logger = getLogger(__name__)

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

    adminIsExist, adminRole = await adminModel.check_if_admin_exists(
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
    

    vec_chunks = [
            DataObject(properties= {
                "company_name": company_name, 
                "text": chunk,
            },
            vector= request.app.llmService.embed_text(chunk, "query").detach().cpu().tolist())
        for chunk in chunks
    ]

    if vec_chunks is None or len(vec_chunks) <1:
        return JSONResponse(content={
        "message" : ResponseEnums.FAILED_TO_EMBED_TEXT.value,
        },
        status_code=status.HTTP_201_CREATED
    )

    vdb_res = await request.app.vdb_service.add_to_VDB(
                                                        collection= await request.app.vdb_service.General_info_collection,
                                                        Objects= vec_chunks, 
                                                        company_name =company_name
                                                    )
    
    if vdb_res.has_errors:
        logger.error("Some records failed to be added to VDB, retrying...")
        
        failed_indices = list(vdb_res.errors.keys())
        
        retry_data = [vec_chunks[idx] for idx in failed_indices]
        
        retry_result = await request.app.vdb_service.add_to_VDB(
                                                        collection= await request.app.vdb_service.General_info_collection,
                                                        Objects= retry_data, 
                                                        company_name =company_name
                                                    )

        if retry_result.has_errors:
            for idx, error in retry_result.errors.items():
                logger.error(f"Retry failed for object #{failed_indices[idx]}: {error}")
            logger.error("Some records could not be inserted after retry.")
        else:
            logger.info("All previously failed inserts succeeded on retry.")
            
    else:
        logger.info("All records inserted successfully to VDB!")
        
        
    
    
    return JSONResponse(content={
        "message" : ResponseEnums.ADDED_TO_DATA_BASE.value,
    },
    status_code=status.HTTP_201_CREATED
    )

    


    



    
    

    
     