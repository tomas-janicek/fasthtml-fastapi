from sqlmodel import Session

from backend.domain import dto, models


def add_example(session: Session, example_in: dto.ExampleIn) -> None:
    example = models.Example(**example_in.model_dump())
    session.add(example)
    session.commit()
