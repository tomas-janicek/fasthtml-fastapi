import pydantic


class ExampleIn(pydantic.BaseModel):
    name: str
    description: str | None


class ExampleList(pydantic.BaseModel):
    data: list[ExampleIn]
    count: int
