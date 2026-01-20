from typing import Protocol, List, Dict


class LLMClient(Protocol):
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        ...
