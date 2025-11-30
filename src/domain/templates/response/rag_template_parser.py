from helpers import Settings
from pathlib import Path
import importlib.util

settings = Settings()
class RAGTemplateParser:

    def __init__(self):
        self._language = None
        self.system_prompt = None
        self.user_prompt = None
        


    @property
    def language(self):
        if self._language is None:
            self.language = settings.DEFAULT_LANGUAGE
        return self._language
    
    @language.setter
    def language(self, language):

        if Path.exists(self.get_lang_module_path(language)):

            module = self.import_from_path(self.get_lang_module_path(language))
            if module:
                self._language = language
                self.system_prompt = getattr(module, "system_prompt")
                self.user_prompt = getattr(module, "user_prompt")
                print(language, "ok one")

        elif Path.exists(self.get_lang_module_path()):
            
            module = self.import_from_path(self.get_lang_module_path())
            if module:
                self._language = settings.DEFAULT_LANGUAGE
                self.system_prompt = getattr(module, "system_prompt")
                self.user_prompt = getattr(module, "user_prompt")
                print(language, "ok two")

        else:
            print(language, "ok three")

            return None


    def get_lang_module_path(self, language:str=None):
        if language is None:
            return Path("domain") / "templates" / "response" / "localization" /  settings.DEFAULT_LANGUAGE / "rag.py"
        else:
            return Path("domain") / "templates" / "response" /  "localization" / language / "rag.py"
    
    

    def import_from_path(self, path: str):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
        
            
    
            
    

            

