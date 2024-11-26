from dataclasses import dataclass
from typing import Optional


@dataclass
class PullRequestFile:
    sha: str
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str
    contents_url: str
    patch: Optional[str]
    previous_filename: Optional[str]

    @staticmethod
    def from_json(json_data: dict) -> 'PullRequestFile':
        return PullRequestFile(
            sha=json_data['sha'],
            filename=json_data['filename'],
            status=json_data['status'],
            additions=json_data['additions'],
            deletions=json_data['deletions'],
            changes=json_data['changes'],
            blob_url=json_data['blob_url'],
            raw_url=json_data['raw_url'],
            contents_url=json_data['contents_url'],
            patch=json_data.get('patch'),
            previous_filename=json_data.get('previous_filename')
        )
