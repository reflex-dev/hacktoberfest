import reflex as rx
from .pipeline_state import PipelineState
from .run_chat_modal import run_chat_modal, new_version_modal, role_item
from ..utils import ToastProvider


def pipeline_main() -> rx.Component:
    return rx.box(
        ToastProvider.create(),
        rx.tabs(
            rx.tab_list(
                rx.tab(
                    "Pipelines",
                    is_selected=False,
                    custom_attrs={'isSelected': False}
                ),
                rx.tab(
                    "New",
                    is_selected=True,
                    custom_attrs={'isSelected': True}
                )
            ),
            rx.tab_panels(
                rx.tab_panel(
                    node_list(),
                    del_confirm_dialog(),
                    left_drawer(),
                    height="100%"
                ),
                rx.tab_panel(
                    rx.cond(
                        PipelineState.init_node_page,
                        new_node_page(),
                        init_prompt_page()
                    )
                ),
                height="100%"
            ),
            align="center",
            is_fitted=True,
            height="100%"
        ),
        run_chat_modal(),
        new_version_modal(),
        width="100%",
        height="100%"
    )


def new_node_page() -> rx.Component:
    return rx.box(
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.text("Node Name: ", width='50%'),
                    rx.box(
                        rx.form_control(
                            rx.input(
                                id='node_name',
                                is_required=True,
                                on_blur=PipelineState.set_node_name,
                                default_value=PipelineState.node_name
                            ),
                            rx.cond(
                                PipelineState.node_exists,
                                rx.form_error_message(
                                    "Name already exists."
                                )
                            ),
                            is_invalid=PipelineState.node_exists
                        ),
                        width="50%"
                    ),
                    width="40%"
                ),
                rx.hstack(
                    rx.text("Node Version: ", width='50%'),
                    rx.input(
                        id='node_version',
                        type_="number",
                        width='50%',
                        default_value=PipelineState.default_node_version,
                        is_read_only=True
                    ),
                    width="40%"
                ),
                rx.hstack(
                    rx.text(
                        "Param Model: ",
                        width='50%'
                    ),
                    rx.box(
                        rx.select(
                            PipelineState.params_model,
                            color_schemes="twitter",
                            id="api_model"
                        ),
                        width='50%'
                    ),
                    width="40%"
                ),
                rx.hstack(
                    rx.text(
                        "Param Temprature: ",
                        width='50%'
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(PipelineState.node_temperature_value),
                            rx.slider(
                                rx.slider_track(
                                    rx.slider_filled_track(bg="tomato"),
                                    bg="red.100"
                                ),
                                rx.slider_thumb(
                                    rx.icon(tag="sun", color="white"),
                                    box_size="1em",
                                    bg="tomato"
                                ),
                                custom_attrs={"step": 10},
                                id="api_temperature",
                                on_change_end=PipelineState.set_node_temperature,
                                default_value=PipelineState.default_temperature
                            )
                        ),
                        width="50%"
                    ),
                    width="40%"
                ),
                rx.hstack(
                    rx.text("Description: ", width='50%'),
                    rx.box(
                        rx.input(id='description'),
                        width='50%'
                    ),
                    width='40%'
                ),
                rx.hstack(
                    rx.button(
                        "Next",
                        type_="submit"
                    )
                ),
                text_align="left"
            ),
            whiteSpace="pre",
            on_submit=PipelineState.next_prompt_page
        )
    )


def init_prompt_page() -> rx.Component:
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
                ),
            ),
            rx.box(
                role_list(),
                overflow="auto",
                h="40vh",
                width="100%",
                border_radius="15px",
                border_width="thick"
            ),
            rx.hstack(
                rx.button(
                    "Back",
                    on_click=PipelineState.back_node_page
                ),
                rx.button(
                    "Save",
                    on_click=PipelineState.save_role
                )
            )
        )
    )


def role_list() -> rx.Component:
    """render role list"""
    return rx.list(
        rx.foreach(PipelineState.role_items, role_item),
        width="100%"
    )


def node_list() -> rx.Component:
    return rx.flex(
        node_panel(),
        rx.cond(
            PipelineState.has_node,
            rx.box(),
            rx.vstack(
                rx.image(src='/right.png', w="35%", h="auto"),
                rx.center(rx.text("Empty!  Create a new node first.", as_='b')),
                m="auto"
            )
        ),
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.text("Dataset: ", width='50%'),
                    rx.box(
                        rx.select(
                            PipelineState.dataset_list,
                            color_schemes="twitter",
                            on_change=PipelineState.set_dataset_option,
                            default_value=PipelineState.dataset_option
                        ),
                        width='50%'
                    ),
                    width='30%'
                ),
                rx.hstack(
                    rx.text("Iteration: ", width='50%'),
                    rx.number_input(
                        default_value=PipelineState.dataset_iteration,
                        input_mode="numeric",
                        min_=1,
                        max_=10,
                        on_change=PipelineState.set_dataset_iteration,
                        width='50%'
                    ),
                    width='30%'
                ),
                rx.hstack(
                    rx.text("Score_API: ", width='50%'),
                    rx.box(
                        rx.select(
                            PipelineState.scoreAPI_list,
                            color_schemes="twitter",
                            id="scoreAPI",
                            on_change=PipelineState.set_score_api,
                            default_value=PipelineState.score_api
                        ),
                        width='50%'
                    ),
                    width='30%'
                )
            ),
            rx.hstack(
                rx.button(
                    "view",
                    on_click=PipelineState.show_prompt()
                ),
                rx.button(
                    "add",
                    on_click=PipelineState.add_version()
                ),
                rx.button(
                    "del",
                    on_click=PipelineState.remove_version()
                ),
                rx.button(
                    "run",
                    on_click=PipelineState.run_selected_node()
                ),
                justify="center",
                m="1em"
            ),
            mt="auto"
        ),
        check_alert(),
        height="95%",
        flexDirection="column"
    )


def node_panel() -> rx.Component:
    return rx.box(
        rx.accordion(
            rx.foreach(
                PipelineState.query_node_list,
                lambda node_name: rx.accordion_item(
                    rx.accordion_button(
                        rx.heading(node_name),
                        rx.accordion_icon(),
                        on_click=PipelineState.set_query_node_name(
                            node_name)

                    ),
                    rx.accordion_panel(
                        rx.table(
                            rx.thead(
                                rx.tr(
                                    rx.th("Node_Name"),
                                    rx.th("Version"),
                                    rx.th("Description"),
                                    rx.th("Check")
                                )
                            ),
                            rx.tbody(
                                rx.foreach(
                                    PipelineState.query_node_by_name,
                                    lambda item, index: rx.tr(
                                        rx.td(item.node_name),
                                        rx.td(
                                            item.node_version),
                                        rx.td(
                                            item.description),
                                        rx.td(rx.checkbox(name=str(index), id=str(index), color_scheme="green",
                                                          on_change=lambda val: PipelineState.set_select_node_item(
                                                              val, item),
                                                          is_checked=PipelineState.selected_node_status.__getitem__(
                                                              item.id)
                                                          )
                                              )
                                    )
                                )
                            )
                        ),
                        overflow="auto",
                        max_height="30vh"
                    )
                ),
                allow_toggle=True,
                width="100%",
                # allow_multiple=True
            ),
            width="100%"
        ),
        width="100%",
        max_height="50vh",
        overflow="auto"
    )


def check_alert() -> rx.Component:
    return rx.box(
        rx.alert_dialog(
            rx.alert_dialog_overlay(
                rx.alert_dialog_content(
                    rx.alert_dialog_header("Tip!"),
                    rx.alert_dialog_body(
                        "Please check and only check one record for operation"
                    ),
                    rx.alert_dialog_footer(
                        rx.button(
                            "Close",
                            on_click=PipelineState.check_node_select
                        )
                    )
                )
            ),
            is_open=PipelineState.node_select_check,
            is_centered=True
        )
    )


def left_drawer() -> rx.Component:
    return rx.drawer(
        rx.drawer_overlay(
            rx.drawer_content(
                rx.drawer_header("Prompt"),
                rx.drawer_body(
                    rx.stat(
                        rx.stat_label(
                            PipelineState.drawer_show_param['model']),
                        rx.stat_number(
                            PipelineState.drawer_show_param['temperature']),
                        rx.stat_help_text(
                            PipelineState.drawer_show_param['description'])
                    ),
                    rx.divider(),
                    rx.foreach(
                        PipelineState.drawer_show_prompt,
                        lambda item: rx.vstack(
                            rx.box(
                                rx.text(item['role'], as_='b', width='100%'), width='100%'),
                            rx.code_block(
                                item['content'],
                                is_format=True,
                                wrap_long_lines=True,
                                width='100%',
                                textAlign=item['align']
                            ),
                            rx.box(h='1em'),
                            textAlign=item['align']
                        )
                    )
                ),
                rx.drawer_footer(
                    rx.button(
                        "Close", on_click=PipelineState.prompt_drawer_close
                    )
                )
            )
        ),
        is_open=PipelineState.show_prompt_drawer,
        return_focus_on_close=True,
        on_close=PipelineState.prompt_drawer_close,
        placement='left',
        size='lg'
    )


def del_confirm_dialog() -> rx.Component:
    return rx.alert_dialog(
        rx.alert_dialog_overlay(
            rx.alert_dialog_content(
                rx.alert_dialog_header("Confirm"),
                rx.alert_dialog_body(
                    rx.vstack(
                        rx.text(
                            "Associated history record will also be deleted!"),
                        rx.text("Do Delete?", as_='b')
                    )
                ),
                rx.alert_dialog_footer(
                    rx.hstack(
                        rx.button(
                            "Yes",
                            on_click=PipelineState.del_confirm_status(
                                True)
                        ),
                        rx.button(
                            "No",
                            on_click=PipelineState.del_confirm_status(
                                False)
                        )
                    )
                )
            )
        ),
        is_open=PipelineState.delete_confirm
    )
