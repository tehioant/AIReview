from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.pull_request_file import PullRequestFile
from aireview.domain.entities.review import Review
from aireview.domain.entities.review_comment import ReviewComment
from aireview.infrastructure.llm_client import LLMClient


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
            print(f"prompt: {prompt}")
            analysis = self._ai_agent.analyse(prompt)
            print(f"analysis: {analysis}")
            review_comments.append(self._parse_analysis(analysis))
        return Review(1, review_comments,"summary of review", "COMMENT")

    def _build_analysis_prompt(self, file: PullRequestFile):
        return (f"<prompt>\n "
                f"status: {file.status}\n "
                f"file_path: {file.filename}\n "
                f"changes: {file.patch if file.patch else file.previous_filename}\n"
                f"</prompt>"
                )


    def _parse_analysis(self, analysis):
        return ReviewComment.from_json(analysis)