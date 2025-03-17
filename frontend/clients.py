from backend.core.config import settings
from frontend import dto, requests


class BackendClient:
    def __init__(self, request: requests.Requests, be_url: str) -> None:
        self.request = request
        self.be_url = be_url

    def get_examples(self) -> dto.ExampleList:
        evaluation = self.request.get(
            base=self.be_url,
            path="/examples",
            response_type=dto.ExampleList,
            timeout=settings.DEFAULT_TIMEOUT,
        )
        return evaluation

    def add_example(self, example: dto.ExampleIn) -> None:
        self.request.post(
            base=self.be_url,
            path="/examples",
            content=example.model_dump_json(),
            timeout=settings.DEFAULT_TIMEOUT,
        )
