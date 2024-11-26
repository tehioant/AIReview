from dataclasses import dataclass
from typing import List

from aireview.domain.entities.pull_request_file import PullRequestFile


@dataclass
class PullRequest:
    id: int
    number: int
    title: str
    description: str
    files: List[PullRequestFile]
    base_branch: str
    head_branch: str
    state: str
    draft: str
