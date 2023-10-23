import reflex as rx
from .dataset_state import DatasetState

color = "rgb(107,99,246)"


def dataset_main() -> rx.Component:
    return rx.box(
        rx.tabs(
            rx.tab_list(
                rx.tab("Dataset"),
                rx.tab("New")
            ),
            rx.tab_panels(
                rx.tab_panel(
                    data_list(),
                    del_confirm_dialog(),
                    left_drawer()
                ),
                rx.tab_panel(
                    new_panel(),
                    up_done_show(),
                    error_show()
                )
            ),
            align="center",
            is_fitted=True,
            height="100%"
        ),
        width="100%",
        height="100%"
    )


def new_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            upload_content(),
            rx.cond(
                DatasetState.upload_dataset_content,
                dataset_meta()
            )
        ),
        mt="2em",
    )


def data_list():
    return rx.box(
        rx.foreach(DatasetState.data_list, data_item),
        width="90%",
        h="70vh",
        overflow="auto"
    )


def data_item(item: rx.Var[dict]):
    return rx.box(
        rx.hstack(
            rx.span(item['dataset_name'], width='20%', as_='b'),
            rx.span(item['description'], width='60%'),
            rx.cond(
                item['dataset_name'].__ne__('None'),
                rx.hstack(
                    rx.button(
                        rx.icon(tag="delete"),
                        on_click=DatasetState.remove_data(item),
                        width='50%'
                    ),
                    rx.button(
                        rx.icon(tag="view"),
                        on_click=DatasetState.show_data(item['dataset_name']),
                        width='50%'
                    ),
                    width='20%'
                )
            ),
            bg="lightgray",
            border_radius="md",
            padding="1em"
        ),
        m="1em"
    )


def upload_content() -> rx.Component:
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}"
                ),
                rx.text("Drag and drop file here or click to select file"),
                text_align="center"
            ),
            multiple=False,
            accept={"application/json": [".json"]},
            border="1px dotted rgb(107,99,246)",
            padding="1em"
        ),
        rx.hstack(rx.foreach(rx.selected_files, rx.text)),
        rx.hstack(
            rx.button(
                "check",
                on_click=lambda: DatasetState.handle_upload(
                    rx.upload_files()
                ),
            ),
            rx.popover(
                rx.popover_trigger(
                    rx.icon(tag="question")
                ),
                rx.popover_content(
                    rx.popover_body(
                        rx.unordered_list(
                            rx.list_item("file format support json now"),
                            rx.list_item(
                                "content format:[{'input': '', 'target': '', 'placeholders': {}}]"),
                            text_align="left"
                        )
                    )
                )
            )
        )
    )


def dataset_meta() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.box(
                rx.divider(border_color="black"),
                width="70%",
                margin="2em"
            ),
            rx.hstack(
                rx.text("Dataset Name: ", width='50%'),
                rx.box(
                    rx.form_control(
                        rx.input(
                            id='dataset_name',
                            is_required=True,
                            default_value=DatasetState.input_data_name,
                            on_change=DatasetState.set_input_data_name
                        ),
                        rx.cond(
                            DatasetState.dataname_exists,
                            rx.form_error_message("Name already exists.")
                        ),
                        is_invalid=DatasetState.dataname_exists
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
            rx.button("submit", type_="submit",
                      is_disabled=DatasetState.dataname_exists)
        ),
        whiteSpace="pre",
        on_submit=DatasetState.upload_dataset,
        width="100%"
    )


def up_done_show() -> rx.Component:
    return rx.box(
        rx.alert_dialog(
            rx.alert_dialog_overlay(
                rx.alert_dialog_content(
                    rx.alert_dialog_header("Info"),
                    rx.alert_dialog_body(
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title("dataset upload success!"),
                            status="success",
                            variant="solid"
                        )
                    ),
                    rx.alert_dialog_footer(
                        rx.button("OK", on_click=DatasetState.up_dataset_done)
                    )
                )
            ),
            is_open=DatasetState.data_upload_done
        )
    )


def error_show() -> rx.Component:
    return rx.box(
        rx.alert_dialog(
            rx.alert_dialog_overlay(
                rx.alert_dialog_content(
                    rx.alert_dialog_header("Tip!"),
                    rx.alert_dialog_body(
                        rx.alert(
                            rx.alert_icon(),
                            rx.alert_title(
                                "The uploaded data format does not meet the requirements, please upload again"),
                            status="error"
                        )
                    ),
                    rx.alert_dialog_footer(
                        rx.button(
                            "OK", on_click=DatasetState.up_datasset_error)
                    )
                )
            ),
            is_open=DatasetState.data_upload_error
        )
    )


def left_drawer() -> rx.Component:
    return rx.drawer(
        rx.drawer_overlay(
            rx.drawer_content(
                rx.drawer_header("Dataset"),
                rx.drawer_body(
                    rx.stat(
                        rx.stat_label(DatasetState.show_data_content['name']),
                        rx.stat_number(
                            DatasetState.show_data_content['number']),
                        rx.stat_help_text(
                            DatasetState.show_data_content['description'])
                    ),
                    rx.code_block(
                        DatasetState.show_data_content['content'],
                        language="json",
                        is_format=True
                    )
                ),
                rx.drawer_footer(
                    rx.button("Close", on_click=DatasetState.data_drawer_close)
                )
                # bg="rgba(0, 0, 0, 0.3)",
            )
        ),
        is_open=DatasetState.show_data_drawer,
        return_focus_on_close=True,
        on_close=DatasetState.data_drawer_close,
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
                            "Yes", on_click=DatasetState.del_confirm_status(True)),
                        rx.button(
                            "No", on_click=DatasetState.del_confirm_status(False))
                    )
                )
            )
        ),
        is_open=DatasetState.delete_confirm
    )
