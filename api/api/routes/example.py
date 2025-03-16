import svcs
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.domain import dto
from api.views import examples as views

router = APIRouter()


@router.post(
    "/example",
)
def create_example(
    services: svcs.fastapi.DepContainer,
    example: dto.ExampleDto,
) -> int:
    """
    Create example.
    """
    session = services.get(Session)
    session.add(example)
    session.commit()

    return status.HTTP_201_CREATED


@router.get("/{example_id}", response_model=dto.ExampleDto)
def read_example_by_id(
    services: svcs.fastapi.DepContainer,
    example_id: int,
) -> dto.ExampleDto:
    """
    Get a specific example by id.
    """
    session = services.get(Session)
    example = views.read_example_by_id(session, example_id)
    if not example:
        raise HTTPException(
            status_code=404,
            detail="The example with this id does not exist in the system.",
        )
    return example


@router.get(
    "",
    response_model=dto.ExamplesDto,
)
def read_examples(
    services: svcs.fastapi.DepContainer,
    skip: int = 0,
    limit: int = 100,
) -> dto.ExamplesDto:
    """
    Retrieve examples.
    """
    session = services.get(Session)

    return views.read_examples(session, skip, limit)
