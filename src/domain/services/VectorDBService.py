from helpers import Settings
from domain.providers.VectorDB import WeaviateDB

from logging import getLogger


logger = getLogger(__name__)

class VectorDBService:
    def __init__(self):
        self.settings = Settings()

        
    @classmethod
    def initialize_service(cls):
        pass