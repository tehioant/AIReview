from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.review import Review
from aireview.domain.repositories.review_repository import ReviewRepository

class ReviewService:
    def __init__(self, repository: ReviewRepository, code_analyzer):
        self._repository = repository
        self._analyzer = code_analyzer

    async def create_review(self, pull_request: PullRequest) -> Review:
        review = await self._analyzer.analyze_code(pull_request)
        await self._repository.save(review)
        return review