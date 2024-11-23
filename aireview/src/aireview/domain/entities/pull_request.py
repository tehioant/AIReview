from dataclasses import dataclass
from typing import List

@dataclass
class PullRequest:
    id: int
    title: str
    description: str
    files: List[str]
    diff: str
    base_branch: str
    head_branch: str