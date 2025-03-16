import svcs
from sqlalchemy.orm import Session, sessionmaker

from api.core import db


def bootstrap(registry: svcs.Registry) -> None:
    session_factory = sessionmaker(bind=db.engine)
    registry.register_factory(
        svc_type=Session,
        factory=session_factory,
        ping=db.ping_db,
    )
