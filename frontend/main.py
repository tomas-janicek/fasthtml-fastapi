# pyright: basic
import logging.config

from fasthtml import serve
from fasthtml.fastapp import fast_app
from starlette.routing import Mount

from frontend.config import LOGGING
from frontend.examples_page import app as example_app

logging.config.dictConfig(config=LOGGING)

app, rt = fast_app(routes=(Mount("/", example_app),))

serve()
