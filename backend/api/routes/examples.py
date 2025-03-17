import svcs
from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from starlette import status

from backend.domain import dto
from backend.service_layer import examples_service
from backend.views import examples as views

router = APIRouter()


@router.post(
    "",
)
def create_example(
    services: svcs.fastapi.DepContainer,
    example_in: dto.ExampleIn,
) -> int:
    """
    Create example.
    """
    session = services.get(Session)

    examples_service.add_example(session, example_in)

    return status.HTTP_201_CREATED


@router.get("/{example_id}", response_model=dto.ExampleIn)
def read_example_by_id(
    services: svcs.fastapi.DepContainer,
    example_id: int,
) -> dto.ExampleIn:
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
    response_model=dto.ExampleList,
)
def read_examples(
    services: svcs.fastapi.DepContainer,
    skip: int = 0,
    limit: int = 100,
) -> dto.ExampleList:
    """
    Retrieve examples.
    """
    session = services.get(Session)

    return views.read_examples(session, skip, limit)
