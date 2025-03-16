import logging

import svcs
import typer
from sqlmodel import SQLModel

from api.bootstrap import bootstrap
from api.core.db import engine

_log = logging.getLogger(__name__)

cli = typer.Typer()


@cli.command(name="healthy")
def healthy() -> None:
    registry = svcs.Registry()
    bootstrap(registry)
    services = svcs.Container(registry=registry)

    for svc in services.get_pings():
        try:
            svc.ping()
            _log.info("Service %s is healthy!", svc.name)
        except Exception as e:
            _log.warning("Service %s is NOT healthy because %s", svc.name, str(e))


@cli.command(name="create-db")
def create_db() -> None:
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    cli()
