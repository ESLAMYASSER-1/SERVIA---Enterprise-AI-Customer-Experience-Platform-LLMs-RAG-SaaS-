from .BaseDataModel import BaseDataModel
from logging import getLogger
from .db_schemas import Chunk

logger = getLogger(__name__)


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
    
        self.collection = self.db_client[self.settings.MONGODB_CHUNKS_COLLECTION]
            
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if self.settings.MONGODB_CHUNKS_COLLECTION not in all_collections:
            self.collection = self.db_client[self.settings.MONGODB_CHUNKS_COLLECTION]
            
            await self.collection.create_index(
                "company_name"
            )
            await self.collection.create_index(
                "company_id"
            )
            await self.collection.create_index([
                ("company_name", 1),
                ("company_id", 1),
            ])
    

    async def insert_one(self, chunk: Chunk):
        result = await self.collection.insert_one(chunk.model_dump())
        return chunk
    
    async def insert_many(self, chunks: list[Chunk]):
        chunks = [c.model_dump(by_alias= True) for c in chunks]
        result = await self.collection.insert_many(chunks)

    async def delete_chunks(self, company_name:str|None = None, company_id:str|None = None):
        if company_name and company_id:
            result = await self.collection.delete_many(
                {
                    "company_name": company_name,
                    "company_id": company_id,
                }
            )
        elif company_name:
            result = await self.collection.delete_many(
                {
                    "company_name": company_name,
                }
            )
        elif company_id:
            result = await self.collection.delete_many(
                {
                    "company_id": company_id,
                }
            )
        return result
    
    async def add_and_delete_chunks(self, chunks: list[Chunk], company_name:str|None = None, company_id:str|None = None):
        
        await self.delete_chunks(company_name, company_id)

        res = await self.insert_many(chunks)

        return res
        

    
