from domain.interfaces import LLMInterface
from helpers import Settings
from logging import getLogger
from openai import AsyncOpenAI
from domain.templates import RAGTemplateParser

logger = getLogger(__name__)


class GenerationOpenAIProvider(LLMInterface):
    def __init__(self):
        self.generation_model_id = None 

        self.client = None

        self.settings = Settings()

        self.template_parser = RAGTemplateParser()
        



    async def set_generation_model(self,):
        self.client = AsyncOpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="Empty",
        base_url=self.settings.VLLM_URL,
        )


        self.generation_model_id = self.settings.GENERATION_MODEL_NAME

        if not self.client or not self.generation_model_id:
            logger.error("❌ error connecting to Generation model client")
            return False
        
        return True

    async def set_generation_language(self, lang):
        self.template_parser.language = lang
        return True

    def text_process(self, text: str):
        text = text.strip(" ").replace("\n", " ")

        return text

    async def generate_text(self, prompt: str, records:list=[], chat_history: list = [], temperature: float = None):

        chat_history = self.construct_prompt(prompt, records, chat_history)

        response = await self.client.chat.completions.create(
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
        
        response = {
            "text":response.choices[0].message.content,
            "reasoning":getattr(response.choices[0].message, "reasoning_content", None),
            "completion_tokens":response.usage.completion_tokens,
            "prompt_tokens":response.usage.prompt_tokens,
            "total_tokens":response.usage.total_tokens,
        }

        chat_history = self.construct_prompt(prompt, records, chat_history)

        return response, chat_history
    
    def construct_prompt(self, prompt: str, records:list=[], chat_history: list= []):

        if chat_history == [] or len(chat_history) == 0:
            chat_history = []
            chat_history.append(
                {
                    "role":"system",
                    "content":self.template_parser.system_prompt()
                }
            )
        
        if isinstance(prompt, dict):
            chat_history.append(
                {"role":"assistant", "content":prompt["text"]}
            )
        
        if isinstance(prompt, str):
            chat_history.append(
                {"role":"user", "content": self.template_parser.user_prompt(prompt, records)}
            )
        return chat_history
        



    def set_embedding_model(self, embedding_model_id: str, embedding_size: int):
        pass

    def embed_text(self, text: str, doc_type: str = "query"):
        pass

    async def close(self):
        await self.client.close()
    

