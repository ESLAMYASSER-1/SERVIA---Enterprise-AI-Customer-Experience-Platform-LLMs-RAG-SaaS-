from domain.interfaces import LLMInterface
from domain.enums import EmbedEnums, DefaultEmbedEnums
from helpers import Settings

from logging import getLogger
from pathlib import Path

from sentence_transformers import SentenceTransformer

logger = getLogger(__name__)

class EmbedderSentenceTransformerProvider(LLMInterface):
    def __init__(self):
        self.provider_name = None
        self.embedding_model_id = None 
        self.embedding_size = None

        self.model = None

        self.settings = Settings()

    def set_embedding_model(self, provider_name:str, embedding_model_id: str, embedding_size: int):
        self.provider_name = provider_name
        self.embedding_model_id = embedding_model_id
        self.embedding_size = embedding_size


        cache_folder = Path(self.settings.ASSETS_FOLDER)/ self.settings.EMBEDDING_MODEL_FOLDER / self.embedding_model_id
        cache_folder.mkdir(parents= True, exist_ok= True)

        self.model = SentenceTransformer(self.embedding_model_id,
                                         cache_folder= cache_folder)

        if not self.model:
            logger.error("can't load Embedding model")
            return False

        return True

    def text_process(self, text: str):
        text = text.strip(" ").replace("\n", " ")

        return text

    def embed_text(self, text: str, doc_type: str = "query"):
        text = self.text_process(text)
        
        try:
            idx = EmbedEnums.PROVIDERS_NAMES.value.index(self.provider_name)
            providerEnum = EmbedEnums.PROVIDERS.value[idx]

        except Exception as e:
            print(e)
            logger.error(e)
            providerEnum = DefaultEmbedEnums

        if doc_type == "query":
            text = providerEnum.QUERY.value+ text
        elif doc_type == "assistant":
            text = providerEnum.ASSISTANT.value+ text
        elif doc_type == "system":
            text = providerEnum.SYSTEM.value+ text
        else:
            return False
        

        return self.model.encode(text, normalize_embeddings=True, convert_to_tensor=True)
    


    # ** from abstract class 
    def generate_text(self, prompt: str, chat_history: list = [], temperature: float = None):
        pass

    def construct_prompt(self, prompt: str, role: str):
        pass

    def set_generation_model(self, generation_model_id: str):
        pass

            
        


        




    
