import pydantic


class ExampleDto(pydantic.BaseModel):
    name: str


class ExamplesDto(pydantic.BaseModel):
    data: list[ExampleDto]
    count: int
