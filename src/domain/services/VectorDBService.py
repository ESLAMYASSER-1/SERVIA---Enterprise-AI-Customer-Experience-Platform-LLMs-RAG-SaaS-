import weaviate
from weaviate.classes.init import Auth 

from helpers import Settings
from domain.providers.VectorDB import WeaviateDB

from logging import getLogger


logger = getLogger(__name__)

class VectorDBService:
    def __init__(self):
        self.settings = Settings()

        self.client = None
        self.VDBprovider = None
        self._General_info_collection = None
        self._Items_collection = None

        
    @classmethod
    async def initialize_service(cls):
            self = cls()

            if self.settings.WEAVIATE_LOCAL_OR_CLOUD in ["local", "LOCAL"]:
                weaviate_params = weaviate.connect.ConnectionParams.from_url(
                    url= self.settings.WEAVIATE_URL,
                    grpc_port = 50051,
                )

                self.client =  weaviate.WeaviateAsyncClient(connection_params= weaviate_params)
                await self.client.connect()
            elif self.settings.WEAVIATE_LOCAL_OR_CLOUD in ["cloud", "CLOUD"]:
                self.client = weaviate.use_async_with_weaviate_cloud(
                    cluster_url=self.settings.WEAVIATE_URL,
                    auth_credentials=Auth.api_key(self.settings.WEAVIATE_API_KEY),
                )
                await self.client.connect()


            self.VDBprovider = WeaviateDB(vdb_client= self.client)
            
            return self
            
    @property
    async def General_info_collection(self):
        if not self._General_info_collection:
            self._General_info_collection = await self.VDBprovider.get_collection_or_create_if_not_exists(
                                                                        self.settings.WEAVIATE_GENERAL_INFO_COLLECTION
                                                                    )
        return self._General_info_collection
    
    @property
    async def Items_collection(self):
        if not self._Items_collection:
            self._Items_collection = await self.VDBprovider.get_collection_or_create_if_not_exists(
                                                                        self.settings.WEAVIATE_GENERAL_INFO_COLLECTION
                                                                    )
        return self._Items_collection
    
    async def add_to_VDB(self,collection,  Objects:list, company_name:str):

        return await self.VDBprovider.insert_many(collection, Objects, company_name)
    
    async def retrieve(self,collection, query:str, vector:list, company_name:str):
         return await self.VDBprovider.retrieve(collection, query, vector, company_name)


    async def close(self):
         await self.client.close()

         
