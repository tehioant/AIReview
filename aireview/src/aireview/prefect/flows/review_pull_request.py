
from prefect import flow

from aireview.config import AIReviewSettings
from aireview.main import main


@flow()
def review_pull_request(pull_request: int, settings: AIReviewSettings=AIReviewSettings()):
    main(pull_request, settings)