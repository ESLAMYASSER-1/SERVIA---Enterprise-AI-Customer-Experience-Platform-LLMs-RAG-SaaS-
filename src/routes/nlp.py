from fastapi import APIRouter, status, Request, WebSocket
from fastapi.responses import JSONResponse




from helpers import Settings
from logging import getLogger


logger = getLogger(__name__)


nlpRouter = APIRouter(prefix="/nlp", tags=["nlp"])

# @nlpRouter.get("/query/{query}")
# async def query(reqeust: Request, query: str, company_name:str):


#     records = await reqeust.app.vdb_service.retrieve(
#         collection= await reqeust.app.vdb_service.General_info_collection,
#         query = query,
#         vector = reqeust.app.llmService.embed_text(
#             text = query,
#             doc_type = "assistant"
#         ).detach().cpu().tolist(),
#         company_name = company_name,
#     )

#     if not records:
#         return JSONResponse(
#         content={
#             "message": "Can't retrieve data!"
#         },
#         status_code=status.HTTP_404_NOT_FOUND,
#     )

#     print(records, sep="\n\n")
    
#     docs = []
#     for i, rec in enumerate(records, 1):
#         docs.append("\n".join(
#             [
#                 f"document # {i}",
#                 f"-> {rec.text}"
#             ]
#         ))
#     docs = "\n\n".join([*docs, f"User message: {query} \n Response: "])
    
#     system_prompt = "\n".join(
#     [
#         "You are a routing model. Your job is to classify the user message into exactly one category and classify the language of the prompt:",
#         "",
#         "1. item — questions about items/products (details, specs, price, availability, item-related customer service).",
#         "2. general — questions about the business, company info, services, offers, policies, or general customer support.",
#         "3. other — anything unrelated to the business or customer service.",
#         "",
#         "Rules:",
#         "- Output only the category name: item, general, or other,",
#         "- Do not explain.",
#         "- Do not add extra text.",
#     ]
# )
#     messages = [
#     {"role": "system", "content": "your are a cutomer service chat bot who answer just based on the documents provided"},
#     {"role": "user", "content": docs},
# ]
    
    
#     response = reqeust.app.llmService.generate_text(messages)
#     print(response)

#     return JSONResponse(
#         content={
#             "status":"ok"
#         },
#         status_code=status.HTTP_201_CREATED,
#     )
    

@nlpRouter.websocket("/query/{company_name}")
async def query(websocket: WebSocket, company_name: str):
    await websocket.accept()
    
    messages = [
        {"role": "system", "content": "your are a cutomer service chat bot who answer just based on the documents provided"},
    ]

    
    while True:
        query = await websocket.receive_text()
        records = await websocket.app.vdb_service.retrieve(
            collection= await websocket.app.vdb_service.General_info_collection,
            query = query,
            vector = websocket.app.llmService.embed_text(
                text = query,
                doc_type = "assistant"
            ).detach().cpu().tolist(),
            company_name = company_name,
        )

        if not records:
            return JSONResponse(
            content={
                "message": "Can't retrieve data!"
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

        # print(records, sep="\n\n")
        
        docs = []
        for i, rec in enumerate(records, 1):
            docs.append("\n".join(
                [
                    f"document # {i}",
                    f"-> {rec.text}"
                ]
            ))
        docs = "\n\n".join([*docs, f"User message: {query} \n Response: "])
        messages.append({"role": "user", "content": docs})
        
        response = await websocket.app.llmService.generate_text(messages)
        messages.append({"role":"assistant", "content":response["text"]})
        print(response)

        await websocket.send_text(response["text"]+" \n\n"+f"TOTAL_TOKENS: {response["total_tokens"]}")