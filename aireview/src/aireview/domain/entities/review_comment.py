from dataclasses import dataclass
from typing import Any


@dataclass
class ReviewComment:
    sha: str
    file_path: str
    line: int
    content: str
    type: str  # 'naming', 'style', 'indentation', 'documentation', 'test_coverage'

    @staticmethod
    def from_json(data: Any) -> 'ReviewComment':
        return ReviewComment(
            sha=data["sha"],
            file_path=data["file_path"],
            line=data["line"],
            content=data["content"],
            type=data["type"]
        )