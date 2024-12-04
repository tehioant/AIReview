from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.pull_request_file import PullRequestFile
from aireview.domain.entities.review import Review
from aireview.domain.entities.review_comment import ReviewComment
from aireview.infrastructure.llm_client import LLMClient
from aireview.utils.extract_json import extract_json


class CodeAnalyzer:
    def __init__(self, ai_agent: LLMClient, call_limit: int = 10):
        self._ai_agent = ai_agent
        self._call_count = 0
        self._call_limit = call_limit

    def analyze_code(self, pull_request: PullRequest) -> Review:
        review_comments: [ReviewComment] = []
        # self._ai_agent.initialize(f"Creating context for review of pull request {pull_request.number}")
        for index, file in enumerate(pull_request.files):
            prompt = self._build_analysis_prompt(file)
            analysis = self._ai_agent.analyse(prompt)
            comments = self._parse_analysis(analysis)
            review_comments.extend(comments)
        return Review(pull_request.number, review_comments,"summary of review", "COMMENT")

    def _build_analysis_prompt(self, file: PullRequestFile):
        return (f"<prompt>\n "
                f"sha: {file.sha}\n"
                f"status: {file.status}\n "
                f"file_path: {file.filename}\n "
                f"changes: {file.patch if file.patch else file.previous_filename}\n"
                f"</prompt>"
                )


    def _parse_analysis(self, analysis):
        review_comments: [ReviewComment] = []
        analysis_comments = extract_json(analysis)
        for comment in analysis_comments:
            review_comments.append(ReviewComment.from_json(comment))
        return review_comments