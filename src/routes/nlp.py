from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse



from helpers import Settings
from logging import getLogger


logger = getLogger(__name__)


nlpRouter = APIRouter(prefix="/nlp", tags=["nlp"])

@nlpRouter.get("/query/{query}")
async def query(reqeust: Request, query: str, company_name:str):
    records = await reqeust.app.vdb_service.retrieve(
        collection= await reqeust.app.vdb_service.General_info_collection,
        query = query,
        vector = reqeust.app.llmService.embed_text(
            text = query,
            doc_type = "assistant"
        ).detach().cpu().tolist(),
        company_name = company_name,
    )

    rec_list=[]
    for rec in records:
        rec_list.append({
            "text": rec.properties["text"],
            "score": rec.metadata.score,
        })

    print(rec_list, sep="\n")
    return JSONResponse(
        content={
            "records": "ok"
        },
        status_code=status.HTTP_201_CREATED,
    )
    