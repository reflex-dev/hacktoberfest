import reflex as rx
from .states import State
from .components import navbar, main


def index() -> rx.Component:
    return rx.box(
        navbar(),
        main()
    )


app = rx.App(state=State)
app.add_page(index, image='logo.png', title='PromptGo',
             description='Welcome to PromptGo!')
app.compile()
