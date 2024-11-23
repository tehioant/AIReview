import pytest
from domain.entities.pull_request import PullRequest
from domain.services.code_analyzer import CodeAnalyzer

class TestCodeAnalyzer:
    @pytest.fixture
    def analyzer(self):
        mock_dust_client = MockDustClient()
        return CodeAnalyzer(mock_dust_client)

    async def test_analyze_code_respects_call_limit(self, analyzer):
        pr = PullRequest(id=1, title="Test", description="Test", files=[], diff="", base_branch="main", head_branch="feature")

        # Make max calls
        for _ in range(10):
            await analyzer.analyze_code(pr)

        # Next call should raise exception
        with pytest.raises(Exception, match="Dust API call limit reached"):
            await analyzer.analyze_code(pr)