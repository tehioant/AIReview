from dataclasses import dataclass
from typing import Any


@dataclass
class ReviewComment:
    file_path: str
    line: int
    content: str
    type: str  # 'naming', 'style', 'indentation', 'documentation', 'test_coverage'

    @staticmethod
    def from_json(data: Any) -> 'ReviewComment':
        return ReviewComment(
            file_path=data.get("file_path", ""),
            line=data.get("line", 0),
            content=data.get("content", ""),
            type=data.get("type", "")
        )