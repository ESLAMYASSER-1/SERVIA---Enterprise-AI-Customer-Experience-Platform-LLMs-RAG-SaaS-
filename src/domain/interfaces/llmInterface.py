from abc import abstractmethod, ABC

class LLMInterface(ABC):
    
    @abstractmethod
    def set_embedding_model(self, embedding_model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def set_generation_model(self, generation_model_id: str):
        pass

    @abstractmethod
    def text_process(self, text: str):
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list = [], temperature: float = None):
        pass

    @abstractmethod
    def embed_text(self, text: str, doc_type: str = "query"):
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass
