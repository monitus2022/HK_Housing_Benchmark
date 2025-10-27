import ollama
from models.prompts import BasePromptModel
from logger import housing_logger
from abc import ABC, abstractmethod
from config import housing_benchmark_config


class BaseLLMConnector(ABC):
    def __init__(self):
        self.model = None

    @abstractmethod
    def set_model(self, model: str):
        pass

    @abstractmethod
    def generate_response(self, user_messages: str, **args) -> str | None:
        pass

    # @abstractmethod
    # def get_prompt_metrics(self):
    #     pass


class LocalOllamaConnector(BaseLLMConnector):
    def __init__(self):
        super().__init__()
        default_model = housing_benchmark_config.llm.ollama.default_model
        self.model = default_model if default_model else None

    def set_model(self, model: str):
        self.model = model

    def generate_response(self, user_messages: str, **args) -> str | None:
        system_messages = args.get('system_messages') or ""
        messages = BasePromptModel(
                    user_messages=user_messages, 
                    system_messages=system_messages
                ).template()
        housing_logger.info(f"Generating response using Ollama model: {self.model}")
        housing_logger.debug(f"Prompt messages: {messages}")
        try:
            chat_session = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "max_tokens": args.get("max_tokens", 1000),
                    "temperature": args.get("temperature", 0.7),
                    "format": "json"
                }
            )
            return chat_session
        except Exception as e:
            housing_logger.error(f"Error generating response from Ollama: {str(e)}")
            return None


class OpenRouterConnector:
    pass
