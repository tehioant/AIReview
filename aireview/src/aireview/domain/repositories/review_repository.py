from abc import ABC, abstractmethod
from aireview.domain.entities.review import Review

class ReviewRepository(ABC):
    @abstractmethod
    async def save(self, review: Review) -> None:
        pass

    @abstractmethod
    async def get_by_pr_id(self, pr_id: int) -> Review:
        pass