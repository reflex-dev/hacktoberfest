import reflex as rx
from .pipeline_state import PipelineState


def run_chat_modal() -> rx.Component:
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Running Chat"),
                rx.modal_body(
                    rx.vstack(
                        rx.heading('Waiting to execute'),
                        rx.circular_progress(
                            rx.circular_progress_label(
                                PipelineState.run_chat_progress),
                            is_indeterminate=True
                        )
                    )
                )
            )
        ),
        is_open=PipelineState.open_run_chat,
        is_centered=True
    )


def new_version_modal() -> rx.Component:
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("New Version"),
                rx.modal_body(
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.select(
                                    PipelineState.params_model,
                                    color_schemes="twitter",
                                    on_change=PipelineState.set_new_api_model,
                                    default_value=PipelineState.default_api_model
                                ),
                                width='25%'
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.text(
                                        PipelineState.node_temperature_value),
                                    rx.slider(
                                        rx.slider_track(
                                            rx.slider_filled_track(
                                                bg="tomato"),
                                            bg="red.100"
                                        ),
                                        rx.slider_thumb(
                                            rx.icon(tag="sun", color="white"),
                                            box_size="1em",
                                            bg="tomato"
                                        ),
                                        custom_attrs={"step": 10},
                                        on_change_end=PipelineState.set_node_temperature,
                                        default_value=PipelineState.default_temperature,
                                    )
                                ),
                                width="25%"
                            ),
                            rx.box(
                                rx.input(on_change=PipelineState.set_new_description,
                                         default_value=PipelineState.default_description),
                                width='50%'
                            ),
                            w="80%"
                        ),
                        rx.box(h='1em'),
                        edit_prompt_page(),
                        w="100%"
                    ),
                    w="100%"
                ),
                rx.modal_footer(
                    rx.hstack(
                        rx.button(
                            "OK", on_click=PipelineState.ok_version
                        ),
                        rx.button(
                            "Cancel", on_click=PipelineState.cancel_version
                        )
                    )
                )
            ),
            w="100%"
        ),
        is_open=PipelineState.open_version_modal,
        size="5xl",
    )


def edit_prompt_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.button(
                    "-",
                    color_scheme="red",
                    border_radius="1em",
                    on_click=PipelineState.remove_role
                ),
                rx.heading("Role"),
                rx.button(
                    "+",
                    color_scheme="green",
                    border_radius="1em",
                    on_click=PipelineState.add_role
                )
            ),
            rx.box(
                exist_role_list(),
                overflow="auto",
                h="40vh",
                width="100%",
                border_radius="15px",
                border_width="thick"
            )
        ),
        w='100%',
    )


def exist_role_list() -> rx.Component:
    """render role list"""
    return rx.list(
        rx.foreach(PipelineState.role_items, role_item),
        width="100%"
    )


def role_item(item: rx.Var[dict]) -> rx.Component:
    """ NOTE: When using `rx.foreach`, the item will be a Var[str] rather than a str."""
    return rx.list_item(
        rx.vstack(
            rx.select(
                PipelineState.role_options,
                default_value=item['role'],
                on_change=lambda c: PipelineState.change_tmp(
                    'role', c, item['index']),
                width="30%",
                position="center"
            ),
            rx.text_area(
                item['content'],
                on_blur=lambda c: PipelineState.change_tmp(
                    'content', c, item['index']),
                width="90%",
                height="25vh"
            ),
            padding="1em",
            align_items="baseline"
        )
    )
