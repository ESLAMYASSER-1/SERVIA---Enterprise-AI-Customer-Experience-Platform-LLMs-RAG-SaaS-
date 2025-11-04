import weaviate 
from weaviate import Client
from weaviate.classes.query import Filter

from .WeaviateDB_Schema import weaviate_info_schema

from logging import getLogger


logger = getLogger(__name__)

class WeaviateDB:
    def __init__(self, vdb_client: Client):
        self.client = vdb_client

    async def get_collection_or_create_if_not_exists(self, collection_name: str):
        existing = [c for c in await self.client.collections.list_all()]
        if collection_name in existing:
            collection = self.client.collections.get(collection_name)
            logger.info(f"- connected to existed VDB collection: ({collection_name}).")
        else:
            collection = await self.client.collections.create(
                name = collection_name,
                properties = weaviate_info_schema,
            )
            logger.info(f"- Created new VDB collection: ({collection_name}) and connected to it.")
        return collection
    
    async def insert_many(self, collection,  Objects: list, company_name:str):
        await collection.data.delete_many(
                                        where=Filter.by_property("company_name").equal(company_name)
                                    )
        
        return await collection.data.insert_many(Objects)
        
