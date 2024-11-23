from dataclasses import dataclass
from typing import List
from aireview.domain.entities.review import Review
from aireview.domain.entities.review_comment import ReviewComment

@dataclass
class ReviewCommentDTO:
    file_path: str
    line: int
    content: str
    type: str

    @classmethod
    def from_entity(cls, entity: ReviewComment) -> 'ReviewCommentDTO':
        return cls(
            file_path=entity.file_path,
            line=entity.line,
            content=entity.content,
            type=entity.type
        )

@dataclass
class ReviewDTO:
    pr_id: int
    comments: List[ReviewCommentDTO]
    summary: str
    status: str

    @classmethod
    def from_entity(cls, entity: Review) -> 'ReviewDTO':
        return cls(
            pr_id=entity.pr_id,
            comments=[ReviewCommentDTO.from_entity(c) for c in entity.comments],
            summary=entity.summary,
            status=entity.status
        )