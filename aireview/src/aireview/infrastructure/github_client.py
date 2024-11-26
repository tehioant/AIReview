import base64
from http.client import responses

import requests
from typing import Dict, Any
import logging

from litellm.llms.custom_httpx.http_handler import headers
from requests import Response
from typer.cli import state

from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.pull_request_file import PullRequestFile
from aireview.domain.entities.review import Review

logger = logging.getLogger(__name__)

class GitHubClient:

    def __init__(self, pat: str, owner: str, repo: str, base_url: str = "https://api.github.com"):
        self._pat = pat
        self.owner = owner
        self.repo = repo
        self._base_url = base_url.rstrip('/')
        self._session = requests.Session()
        self._headers = {
            "Authorization": f"Bearer {pat}",
            "Accept": "application/vnd.github.v3+json",
            'X-GitHub-Api-Version': '2022-11-28'
        }

    async def get_pull_request(self, pr_number: int) -> PullRequest:
        pr_data = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}")
        pr_data.raise_for_status()

        files_data = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/files")
        files_data.raise_for_status()
        json_pr_data = pr_data.json()

        return PullRequest(
            id=json_pr_data["id"],
            number=json_pr_data["number"],
            title=json_pr_data["title"],
            description=json_pr_data["body"] or "",
            files=[PullRequestFile.from_json(f) for f in files_data.json()],
            base_branch=json_pr_data["base"]["ref"],
            head_branch=json_pr_data["head"]["ref"],
            state= json_pr_data["state"],
            draft= json_pr_data["draft"]
        )

    async def submit_review(
            self,
            pr_number: int,
            review: Review
    ) -> None:
        response: Response
        try:
            for comment in review.comments:
                review_data = {
                    "body": f"**{comment.type}**: {comment.content}",
                    "commit_id": '0bc1452063f61711e9bda6b4a1f49410bc621c7b',
                    "path": comment.file_path,
                    "start_line": comment.line,
                    "start_side": 'RIGHT',
                    "line": comment.line+1,
                    "side": 'RIGHT'
                }

                response = self._session.post(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/comments",headers=self._headers, json=review_data)
                response.raise_for_status()

            logger.info(f"Successfully submitted review for PR #{pr_number}")
            print(f"Successfully submitted review for PR #{pr_number} :: response {response.json()}")
        except Exception as e:
            logger.error(f"Failed to submit review for PR #{pr_number}: {str(e)}")
            raise

    async def get_file_content(
            self,
            path: str,
            ref: str
    ) -> str:
        try:
            response = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/contents/{path}",
                headers=self._headers,
                data={"ref": ref}
            )
            response.raise_for_status()
            return base64.b64decode(response.json()["content"]).decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to fetch file content for {path}: {str(e)}")
            raise

    async def get_diff_stats(
            self,
            pr_number: int
    ) -> Dict[str, Any]:
        files_data = self._session.get(f"{self._base_url}/repos/{self.owner}/{self.repo}/pulls/{pr_number}/files", headers=self._headers,)
        files_data.raise_for_status()
        return {
            "total_changes": sum(f["changes"] for f in files_data),
            "additions": sum(f["additions"] for f in files_data),
            "deletions": sum(f["deletions"] for f in files_data),
            "changed_files": len(files_data.json())
        }
