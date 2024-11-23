from importlib.metadata import files

import requests

# infrastructure/github_client.py
from typing import List, Dict, Any, Optional
import logging

from setuptools.unicode_utils import filesys_decode

from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.review import Review
from aireview.domain.entities.review_comment import ReviewComment

logger = logging.getLogger(__name__)

class GitHubClient:

    def __init__(self, pat: str, base_url: str = "https://api.github.com"):
        """Initialize GitHub client with authentication token.

        Args:
            token (str): GitHub personal access token
            base_url (str, optional): GitHub API base URL. Defaults to "https://api.github.com".
        """
        self._pat = pat
        self._base_url = base_url.rstrip('/')
        self._headers = {
            "Authorization": f"Bearer {pat}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    async def get_pull_request(self, owner: str, repo: str, pr_number: int) -> PullRequest:
        """Fetch pull request details from GitHub.

        Args:
            owner (str): Repository owner
            repo (str): Repository name
            pr_number (int): Pull request number

        Returns:
            PullRequest: Domain entity representing the pull request
        """
        # Fetch PR details :cite[ri]
        pr_data = requests.get(f"/repos/{owner}/{repo}/pulls/{pr_number}")
        print(pr_data)

        # Fetch PR files
        files_data = requests.get(f"/repos/{owner}/{repo}/pulls/{pr_number}/files")
        print(files_data)

        return PullRequest(
            id=pr_data["id"],
            title=pr_data["title"],
            description=pr_data["body"] or "",
            files=[f["filename"] for f in files_data],
            diff="".join(f["patch"] for f in files_data if "patch" in f),
            base_branch=pr_data["base"]["ref"],
            head_branch=pr_data["head"]["ref"]
        )

    # async def submit_review(
    #         self,
    #         owner: str,
    #         repo: str,
    #         pr_number: int,
    #         review: Review
    # ) -> None:
    #     """Submit a review for a pull request.
    #
    #     Args:
    #         owner (str): Repository owner
    #         repo (str): Repository name
    #         pr_number (int): Pull request number
    #         review (Review): Review to submit
    #
    #     Raises:
    #         GitHubAPIError: If review submission fails
    #     """
    #     # Prepare review comments :cite[cc,aw]
    #     comments = [
    #         {
    #             "path": comment.file_path,
    #             "line": comment.line,
    #             "body": f"**{comment.type}**: {comment.content}"
    #         }
    #         for comment in review.comments
    #     ]
    #
    #     review_data = {
    #         "event": review.status,  # APPROVE, REQUEST_CHANGES, or COMMENT
    #         "body": review.summary,
    #         "comments": comments
    #     }
    #
    #     try:
    #         await self._make_request(
    #             "POST",
    #             f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews",
    #             data=review_data
    #         )
    #         logger.info(f"Successfully submitted review for PR #{pr_number}")
    #     except Exception as e:
    #         logger.error(f"Failed to submit review for PR #{pr_number}: {str(e)}")
    #         raise
    #
    # async def get_file_content(
    #         self,
    #         owner: str,
    #         repo: str,
    #         path: str,
    #         ref: str
    # ) -> str:
    #     """Fetch file content from GitHub.
    #
    #     Args:
    #         owner (str): Repository owner
    #         repo (str): Repository name
    #         path (str): File path
    #         ref (str): Git reference (branch, commit)
    #
    #     Returns:
    #         str: File content
    #     """
    #     try:
    #         response = await self._make_request(
    #             "GET",
    #             f"/repos/{owner}/{repo}/contents/{path}",
    #             data={"ref": ref}
    #         )
    #
    #         import base64
    #         return base64.b64decode(response["content"]).decode("utf-8")
    #     except Exception as e:
    #         logger.error(f"Failed to fetch file content for {path}: {str(e)}")
    #         raise
    #
    # async def get_diff_stats(
    #         self,
    #         owner: str,
    #         repo: str,
    #         pr_number: int
    # ) -> Dict[str, Any]:
    #     """Get pull request diff statistics.
    #
    #     Args:
    #         owner (str): Repository owner
    #         repo (str): Repository name
    #         pr_number (int): Pull request number
    #
    #     Returns:
    #         Dict[str, Any]: Diff statistics
    #     """
    #     files_data = await self._make_request(
    #         "GET",
    #         f"/repos/{owner}/{repo}/pulls/{pr_number}/files"
    #     )
    #
    #     return {
    #         "total_changes": sum(f["changes"] for f in files_data),
    #         "additions": sum(f["additions"] for f in files_data),
    #         "deletions": sum(f["deletions"] for f in files_data),
    #         "changed_files": len(files_data)
    #     }
