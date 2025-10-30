from .BaseDataModel import BaseDataModel
from logging import getLogger

logger = getLogger(__name__)



class AdminModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        
        self.collection = self.db_client[self.settings.MONGODB_ADMIN_COLLECTION]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance
    

    async def check_if_admin_exists(self, Admin_name: str|None = None, Admin_password: str|None = None)->bool:
        result = await self.collection.find_one({"Name":Admin_name, "Password":Admin_password})
        if result is None:
            logger.info(f"Admin_name:{Admin_name}, Admin_password:{Admin_password}. has been denied as admin data")
            return False
        result["mongo_id"] = str(result["_id"])
        del result["_id"]


        logger.info(f"Admin{result["mongo_id"]} has logged in to the system")
        return True

        
