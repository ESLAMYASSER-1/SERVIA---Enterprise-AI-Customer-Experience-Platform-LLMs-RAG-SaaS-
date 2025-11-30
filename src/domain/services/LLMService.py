from helpers import Settings
from domain.providers import EmbedderSentenceTransformerProvider, GenerationOpenAIProvider

from logging import getLogger

logger = getLogger(__name__)
class LLMService:
    def __init__(self):
        self.settings = Settings()

        self.embedding_provider = None
        self.generation_provider = None

    @classmethod
    async def initialize_service(cls):
        self = cls()
        self.embedding_provider = EmbedderSentenceTransformerProvider()

        embed_model_is_created = self.embedding_provider.set_embedding_model(
                                                    provider_name=self.settings.EMBEDDING_PROVIDER, 
                                                    embedding_model_id=self.settings.EMBEDDING_MODEL,
                                                    embedding_size= self.settings.EMBEDDING_MODEL_SIZE,
                                                )
        
        if not embed_model_is_created:
            logger.error("embedding model service can't be initialized")
            return False


        # TODO:add generation model here 

        self.generation_provider = GenerationOpenAIProvider()
        await self.generation_provider.set_generation_language(self.settings.DEFAULT_LANGUAGE)
        generation_model_is_created = await self.generation_provider.set_generation_model()
        

        if not generation_model_is_created:
            logger.error("genration model service can't be initialized")
            return False

        # TODO: add LLMRouter provider here 


        return self
        
    def embed_text(self, text: str, doc_type: str = "query"):

        return self.embedding_provider.embed_text(text, doc_type)
    
    def generate_text(self, prompt: str, records:list=[], chat_history: list = [], temperature: float = None):
        
        return self.generation_provider.generate_text(prompt=prompt, records = records, chat_history= chat_history, temperature=temperature)
    
    async def close(self):
        await self.generation_provider.close()
    
        

        