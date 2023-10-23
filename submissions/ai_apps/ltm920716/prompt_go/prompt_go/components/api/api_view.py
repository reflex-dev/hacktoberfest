import reflex as rx
from .api_state import ApiState


def api_main() -> rx.Component:
    return rx.box(
        rx.tabs(
            rx.tab_list(
                rx.tab(
                    "APIs"
                ),
                rx.tab(
                    "New"
                )
            ),
            rx.tab_panels(
                rx.tab_panel(
                    api_list()
                ),
                rx.tab_panel(
                    api_meta()
                )
            ),
            align='center',
            is_fitted=True
        ),
        width="100%",      
    )


def api_list() -> rx.Component:
    return rx.box(
        rx.foreach(ApiState.api_list, api_item),
        width="100%",
        h="70vh",
        overflow="auto"
    )


def api_item(item: rx.Var[dict]) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.span(item['api_name'], width='20%', as_='b'),
            rx.span(item['api_version'], width='5%'),
            rx.span(item['api_url'], width='40%'),
            rx.span(item['tips'], width='25%'),
            rx.button(
                rx.icon(tag="delete"),
                # on_click=State.remove_api(item['index'])
                is_disabled=True,
                width='5%'
            ),
            rx.button(
                rx.icon(tag="edit"),
                # on_click=State.edit_api(item['index'])
                is_disabled=True,
                width='5%'
            ),
            bg="lightgray",
            border_radius="md",
            p="1em",
        ),
        m="1em",
    )


def api_meta() -> rx.Component:
    return rx.form(
            rx.vstack(
                rx.hstack(
                    rx.text("API Name: ", width='50%'),
                    rx.input(
                        id='api_name',
                        is_required=True,
                        width='50%'
                    ),
                    width="40%"
                ),
                rx.hstack(
                    rx.text("API Version: ", width='50%'),
                    rx.input(
                        id='api_version',
                        is_required=True,
                        width='50%'
                    ),
                    width='40%'
                ),
                rx.hstack(
                    rx.text("API URL: ", width='50%'),
                    rx.input(
                        id='api_url',
                        is_required=True,
                        width='50%'
                    ),
                    width='40%'
                ),
                rx.hstack(
                    rx.text("API Params: ", width='50%'),
                    rx.input(
                        id='api_params',
                        is_required=True,
                        width='50%'
                    ),
                    width='40%'
                ),
                rx.hstack(
                    rx.text(
                        "API Type: ",
                        width='50%'
                    ),
                    rx.box(
                        rx.select(
                            ApiState.api_types,
                            color_schemes="twitter",
                            id="api_type"
                        ),
                        width='50%'
                    ),
                    width="40%"
                ),
                rx.hstack(
                    rx.text("API Tips: ", width='50%'),
                    rx.input(
                        id='api_tips',
                        width='50%'
                    ),
                    width='40%'
                ),
                rx.hstack(
                    rx.button(
                        "Add API",
                        type="submit",
                        is_disabled=True
                    ),
                    m="1em"
                ),
                text_align="left"
            ),
            whiteSpace="pre"
        )