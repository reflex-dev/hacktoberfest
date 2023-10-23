import reflex as rx
from prompt_go.states import State
from .pipeline.pipeline_view import pipeline_main
from .api.api_view import api_main
from .dataset.dataset_view import dataset_main
from .history.history_view import history_main


def main():
    return rx.box(
        rx.center(
            rx.vstack(
                rx.button(
                    "History",
                    border_radius="15px",
                    border_width="thick",
                    width="100%",
                    h="15vh",
                    on_click=State.history_show,
                ),
                rx.button(
                    "Pipeline",
                    border_radius="15px",
                    border_width="thick",
                    width="100%",
                    h="15vh",
                    on_click=State.pipeline_show,
                ),
                rx.button(
                    "Dataset",
                    border_radius="15px",
                    border_width="thick",
                    width="100%",
                    h="15vh",
                    on_click=State.dataset_show
                ),
                rx.button(
                    "API",
                    border_radius="15px",
                    border_width="thick",
                    width="100%",
                    h="15vh",
                    on_click=State.api_show
                ),
                width="20%",
                padding="1em"
            ),
            rx.box(
                rx.cond(
                    State.hello_word,
                    hello_prompt(),
                ),
                rx.cond(
                    State.open_history,
                    history_main(),
                ),
                rx.cond(
                    State.open_pipeline,
                    pipeline_main(),
                ),
                rx.cond(
                    State.open_api,
                    api_main()
                ),
                rx.cond(
                    State.open_dataset,
                    dataset_main()
                ),
                bg="white",
                width="80%",
                border_radius="15px",
                h="80vh"
            ),
            width="80%",
            height="80%",
            margin="0 auto"
        ),
        h="100vh",
        pt=16,
        background="url(bg.svg)",
        background_repeat="no-repeat",
        background_size="cover"
    )


def hello_prompt():
    return rx.center(
        rx.text(
            "Hello Prompt",
            as_='strong',
            font_size="6em"
        ),
        height="100%"
    )
