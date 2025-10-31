import weaviate 
from weaviate import Client

from WeaviateDB_Schema import weaviate_info_schema

from logging import getLogger


logger = getLogger(__name__)

class WeaviateDB:
    def __init__(self, vdb_client: Client):
        self.client = vdb_client
        self.collection = None

    async def get_collection_or_create_if_not_exists(self, collection_name: str):
        existing = [c.name for c in await self.client.collections.list_all()]
        if collection_name in existing:
            self.collection = await self.client.collections.get(collection_name)
            logger.info(f"- connected to existed VDB collection: ({collection_name}).")
        else:
            self.collection = await self.client.collections.create(
                name = collection_name,
                properties = weaviate_info_schema,
            )
            logger.info(f"- Created new VDB collection: ({collection_name}) and connected to it.")
    
    async def insert_many(self, Objects: list):
        return await self.collectionl.data.insert_many(Objects)
        
