from dotenv import load_dotenv
from helpers import Settings
load_dotenv()

class BaseDataModel:
    def __init__(self, db_client: object):
        self.settings = Settings()
        self.db_client = db_client
