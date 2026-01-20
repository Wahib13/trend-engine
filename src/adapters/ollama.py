from typing import List, Dict

import ollama

from adapters.interfaces import LLMClient


class OllamaClient(LLMClient):
    def __init__(self, model: str):
        self.model = model

    def chat(self, messages: List[Dict[str, str]], stream=False, **kwargs):
        response = ollama.chat(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        return response["message"]["content"]
