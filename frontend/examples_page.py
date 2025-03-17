# pyright: basic
import httpx
from fasthtml import ft, pico
from fasthtml.fastapp import fast_app

from frontend import clients, dto, requests
from frontend.config import settings

app, rt = fast_app()

request = requests.HTTPXRequests(httpx.Client())
client = clients.BackendClient(request=request, be_url=settings.BASE_BE_URL)

examples: list[dto.ExampleIn] = []


def get_add_example_form():
    name_input = ft.Input(id="new-title", name="name", placeholder="Example Name")
    description_input = ft.Input(
        id="new-description", name="description", placeholder="Example Description"
    )
    add_example_form = ft.Form(
        pico.Group(name_input, description_input, ft.Button("Add")),
        hx_post="/",
        target_id="example-list",
        hx_swap="afterbegin",
    )
    return add_example_form


def get_example_component(example: dto.ExampleIn):
    return ft.Li(f"{example.name}: {example.description}")


@app.get("/")  # type: ignore
def get_examples():
    examples_dto = client.get_examples()
    examples.clear()
    examples.extend(examples_dto.data)

    title = "Examples List"
    top = pico.Grid(ft.H1(title))

    add_example_form = get_add_example_form()

    examples_element = ft.Ul(
        *[get_example_component(example) for example in examples], id="example-list"
    )
    card = pico.Card(footer=examples_element, header=add_example_form)

    return ft.Title(title), pico.Container(top, card)


@app.post("/")  # type: ignore
def post_example(example: dto.ExampleIn):
    example_element = get_example_component(example)
    examples.append(example)
    client.add_example(example)
    return example_element
