from domain.interfaces import LLMInterface
from helpers import Settings
from logging import getLogger
from openai import OpenAI


logger = getLogger(__name__)


class GenerationOpenAIProvider(LLMInterface):
    def __init__(self):
        self.generation_model_id = None 

        self.client = None

        self.settings = Settings()



    def set_generation_model(self,):
        self.client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="Empty",
        base_url=self.settings.VLLM_URL,
        )


        self.generation_model_id = self.client.models.list().data[0].id

        if not self.client or not self.generation_model_id:
            logger.error("❌ error connecting to Generation model client")
            return False
        
        return True


    def text_process(self, text: str):
        text = text.strip(" ").replace("\n", " ")

        return text

    def generate_text(self, prompt: str, chat_history: list = [], temperature: float = None):
        response = self.client.chat.completions.create(
            messages=chat_history,
            model=self.generation_model_id,
            extra_body={
                "chat_template_kwargs": {
                "enable_thinking": self.settings.ENABLE_THINKING,
                }
            }
        )
        if not response.choices[0].message.content:
            return False
        
        return {
            "text":response.choices[0].message.content,
            "reasoning":getattr(response.choices[0].message, "reasoning_content", None),
            "completion_tokens":response.usage.completion_tokens,
            "prompt_tokens":response.usage.prompt_tokens,
            "total_tokens":response.usage.total_tokens,
        }
    
    def construct_prompt(self, prompt: str, role: str):
        pass


    def set_embedding_model(self, embedding_model_id: str, embedding_size: int):
        pass

    def embed_text(self, text: str, doc_type: str = "query"):
        pass
    

