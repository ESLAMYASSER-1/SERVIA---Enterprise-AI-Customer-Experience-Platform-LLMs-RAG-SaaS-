from domain.interfaces import LLMInterface
from helpers import Settings
from logging import getLogger
from domain.templates import RouterTemplateParser

logger = getLogger(__name__)


class LLMRouterOpenAIProvider(LLMInterface):
    def __init__(self):
        self.LLMRouter_model_id = None 
        self.template_parser = RouterTemplateParser()
        self.settings = Settings()


    def text_process(self, text: str):
        text = text.strip(" ").replace("\n", " ")

        return text

    async def classify_prompt(self, prompt: str, client: float = None):
        prompt = self.text_process(prompt)
        routing_prompt= self.construct_prompt(prompt)

        response = await client.chat.completions.create(
            messages=routing_prompt,
            model=self.LLMRouter_model_id,
            extra_body={
                "chat_template_kwargs": {
                "enable_thinking": self.settings.ENABLE_THINKING,
                }
            }
        )

        if not response.choices[0].message.content:
            return False
        
        return response.choices[0].message.content
    
    def construct_prompt(self, prompt: str,):

        routing_prompt = []
        routing_prompt.append(
            {
                "role":"system",
                "content":self.template_parser.system_prompt()
            }
        )

        routing_prompt.append(
            {
                "role":"user",
                "content":self.template_parser.user_prompt(prompt)
            }
        )

        return routing_prompt


    def generate_text(self, prompt: str, chat_history: list = [], temperature: float = None):
        pass

    def set_generation_model(self, generation_model_id: str):
        pass

    def set_embedding_model(self, embedding_model_id: str, embedding_size: int):
        pass

    def embed_text(self, text: str, doc_type: str = "query"):
        pass
    

