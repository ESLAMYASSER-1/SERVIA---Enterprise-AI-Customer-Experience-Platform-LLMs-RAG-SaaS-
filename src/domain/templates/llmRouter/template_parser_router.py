from helpers import Settings
from .localization.en import system_prompt, user_prompt

settings = Settings()
class RouterTemplateParser:

    def __init__(self):
        self._language = None
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        
