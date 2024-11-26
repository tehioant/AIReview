from langchain.chains.summarize.refine_prompts import prompt_template
from tenacity import retry_unless_exception_type

from aireview.domain.entities.pull_request import PullRequest
from aireview.domain.entities.pull_request_file import PullRequestFile
from aireview.domain.entities.review import Review
from aireview.domain.entities.review_comment import ReviewComment


class CodeAnalyzer:
    def __init__(self, ai_agent, call_limit: int = 10):
        self._ai_agent = ai_agent
        self._call_count = 0
        self._call_limit = call_limit

    async def analyze_code(self, pull_request: PullRequest) -> Review:
        if self._call_count >= self._call_limit:
            raise Exception("Dust API call limit reached")
        for index, file in enumerate(pull_request.files):
            prompt = self._build_analysis_prompt(file)
        print(f"prompt: {prompt}")
        analysis = await self._ai_agent.analyze(prompt)
        self._call_count += 1
        print(f"analysis: {analysis}")
        return self._parse_analysis(analysis)

    def _build_analysis_prompt(self, file: PullRequestFile):
        return (f"<prompt>\n "
                f"status: {file.status}\n "
                f"file_path: {file.filename}\n "
                f"changes: {file.patch if file.patch else file.previous_filename}\n"
                f"</prompt>"
                )


    def _parse_analysis(self, analysis):
        return Review(1, [ReviewComment("aireview/src/aireview/infrastructure/github_client.py", 34, "get_pull_request", "naming")], "summary of review", "COMMENT")