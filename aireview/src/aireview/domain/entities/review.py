from dataclasses import dataclass
from typing import List

from aireview.domain.entities.review_comment import ReviewComment


@dataclass
class Review:
    pr_id: int
    comments: List[ReviewComment]
    summary: str
    status: str  # APPROVE, REQUEST_CHANGES, COMMENT