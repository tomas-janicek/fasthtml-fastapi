from sqlalchemy.orm import Session
from sqlmodel import func, select

from api.domain import dto, models


def read_example_by_id(session: Session, id: int) -> dto.ExampleDto | None:
    stmt = select(models.Example).where(models.Example.id == id)
    example = session.scalar(stmt)

    return dto.ExampleDto(name=example.name) if example else None


def read_examples(session: Session, skip: int = 0, limit: int = 100) -> dto.ExamplesDto:
    count_statement = select(func.count()).select_from(models.Example)
    # count statement always return 0 even if there are no examples
    count = session.scalar(count_statement)

    statement = select(models.Example).offset(skip).limit(limit)
    examples = session.scalars(statement).all()

    examples_dtos = [dto.ExampleDto(name=e.name) for e in examples]
    return dto.ExamplesDto(data=examples_dtos, count=count)  # type: ignore
