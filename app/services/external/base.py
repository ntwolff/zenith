from abc import ABC, abstractmethod
from pydantic import BaseModel

class ExternalService(ABC):
    @abstractmethod
    async def enrich(self, model: BaseModel) -> BaseModel:
        pass