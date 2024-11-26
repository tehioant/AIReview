from abc import ABC, abstractclassmethod, abstractmethod

class LLMClient(ABC):

    url: str

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    async def analyse(self, prompt: str):
        pass