


class GitHubClient:
    async def submit_review(self, pr_id: int, review: Review) -> None:
        # Submit review using GitHub API :cite[cc]
        comments = [
            {"path": comment.file_path, "line": comment.line, "body": comment.content}
            for comment in review.comments
        ]

        await self._github.pulls.create_review(
            pull_number=pr_id,
            event=review.status,
            body=review.summary,
            comments=comments
        )