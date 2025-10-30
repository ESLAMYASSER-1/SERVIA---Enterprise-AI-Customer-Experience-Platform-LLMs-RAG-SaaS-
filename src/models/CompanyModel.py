from .BaseDataModel import BaseDataModel
from logging import getLogger
from .db_schemas import Company

logger = getLogger(__name__)


class CompanyModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
    
        self.collection = self.db_client[self.settings.MONGODB_COMPANY_COLLECTION]
            
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if self.settings.MONGODB_COMPANY_COLLECTION not in all_collections:
            self.collection = self.db_client[self.settings.MONGODB_COMPANY_COLLECTION]
            
            await self.collection.create_index(
                "Name"
            )
    
    async def create_company(self, company: Company):
        result = await self.collection.insert_one(company.model_dump())
        return company
    
    async def get_company_or_create_one(self, company_name: str):
        res = await self.collection.find_one({"Name":company_name})

        if res is None:
            company = Company(Name = company_name)
            company = await self.create_company(company=company)

            return company
        
        return Company(**res)
    
    
        

                

    