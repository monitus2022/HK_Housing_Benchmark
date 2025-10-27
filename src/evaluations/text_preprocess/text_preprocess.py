from models.prompts import BasePromptModel
from logger import housing_logger
from llm import LocalOllamaConnector, OpenRouterConnector

class TextPreprocessor:
    def __init__(self, local_model: bool = True):
        if local_model:
            self.llm_connector = LocalOllamaConnector()
        else:
            self.llm_connector = OpenRouterConnector()
    
    def set_model(self, model_name: str):
        self.llm_connector.set_model(model_name)
        
