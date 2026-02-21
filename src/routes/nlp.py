from fastapi import APIRouter, status, Request, WebSocket
from fastapi.responses import JSONResponse
from typing import List
import base64
from pathlib import Path

from helpers import Settings
from logging import getLogger


logger = getLogger(__name__)
settings = Settings()

nlpRouter = APIRouter(prefix="/chat", tags=["chat"])

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
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.wb_chat_histories = dict()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.wb_chat_histories[websocket] = [] 

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        self.wb_chat_histories.pop(websocket, "")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
    
    async def send_text(self, data: dict, websocket: WebSocket):
        await websocket.send_text(data)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


# @nlpRouter.websocket("/query/{company_name}")
# async def query(websocket: WebSocket, company_name: str):
#     await manager.connect(websocket)

#     chat_history = []


#     while True:
#         query = await websocket.receive_text()
#         print(query)
#         records = await websocket.app.vdb_service.retrieve(
#             collection= await websocket.app.vdb_service.General_info_collection,
#             query = query,
#             vector = websocket.app.llmService.embed_text(
#                 text = query,
#                 doc_type = "query"
#             ).detach().cpu().tolist(),
#             company_name = company_name,
#         )

#         print(records, sep="\n\n")
        
        
        
#         response, chat_history = await websocket.app.llmService.generate_text(query, records, chat_history)
        
#         print(response)

#         await websocket.send_text(response["text"]+" \n\n"+f"TOTAL_TOKENS: {response["total_tokens"]}")


@nlpRouter.websocket("/query/{company_name}")
async def query(websocket: WebSocket, company_name: str):
    print("websocket")
    await manager.connect(websocket)

    chat_history = []


    while True:
        message  = await websocket.receive_json()

        if message["type"] == "text":
            query = message["content"]
            # print(query)
            # print(records, sep="\n\n")
            
        elif message ["type"] == "audio":
            audio_bytes = base64.b64decode(message["content"])
            audio_path =Path(settings.ASSETS_FOLDER)/"audio.wav"
            
            with open(audio_path, "wb") as f:
                f.write(audio_bytes)
            
            segments, info = websocket.app.audioService.transcribe(audio_path)
            
            query = " ".join(seg.text for seg in segments) # the transcript 
            
            # print(query)

        lang = await websocket.app.llmService.classify_prompt(query,
                                                            websocket.app.llmService.generation_provider.client
                                                        )
        if not lang:
            lang = "en"

        # print(lang)
        websocket.app.llmService.generation_provider.template_parser.language = lang

        records = await websocket.app.vdb_service.retrieve(
                collection= await websocket.app.vdb_service.General_info_collection,
                query = query,
                vector = websocket.app.llmService.embed_text(
                    text = query,
                    doc_type = "query"
                ).detach().cpu().tolist(),
                company_name = company_name,
            )   

        response, chat_history = await websocket.app.llmService.generate_text(query, records, manager.wb_chat_histories[websocket])
        manager.wb_chat_histories[websocket] = chat_history
        # print(chat_history)
        # print(response)

        await manager.send_text(response["text"], websocket)
