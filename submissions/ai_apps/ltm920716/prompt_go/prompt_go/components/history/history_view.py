import reflex as rx
from .history_state import HistoryState
from typing import List
from ..utils import ToastProvider


def history_main() -> rx.Component:
    return rx.box(
        ToastProvider.create(),
        rx.tabs(
            rx.tab_list(
                rx.tab("Records"),
                rx.tab("Detial")
            ),
            rx.tab_panels(
                rx.tab_panel(
                    chat_record_list(),
                    rx.cond(
                        HistoryState.has_record,
                        rx.box(),
                        rx.vstack(
                            rx.image(src='/down.png', w="23%", h="auto"),
                            rx.center(
                                rx.text("Empty!  Go to Pipeline panel.", as_='b')),
                            mt="5em"
                        )
                    ),
                    compare_alert()
                ),
                rx.tab_panel(
                    rx.cond(
                        HistoryState.get_compare_num > 0,
                        run_result(),
                        rx.vstack(
                            rx.image(src='/left.png', w="23%", h="auto"),
                            rx.center(
                                rx.text("Empty!  Check one or two record.", as_='b')),
                            mt="5em"
                        )
                    ),
                    left_drawer()
                    # on_mount=HistoryState.on_mount,
                )
            ),
            align="center",
            is_fitted=True,
            height="100%",
            w="100%"
        ),
        width="100%",
        height="100%"
    )


options: List[str] = ['0', '1', '2', '3', '4', '5']


def chat_record_list() -> rx.Component:
    return rx.box(
        rx.accordion(
            rx.foreach(
                HistoryState.query_history_list,
                lambda node_name: rx.accordion_item(
                    rx.accordion_button(
                        rx.heading(node_name),
                        rx.accordion_icon(),
                        on_click=HistoryState.set_history_node_name(
                            node_name)

                    ),
                    rx.accordion_panel(
                        rx.table(
                            rx.thead(
                                rx.tr(
                                    rx.th("Node_Name"),
                                    rx.th("Version"),
                                    rx.th("Dataset"),
                                    rx.th("Items"),
                                    rx.th("Check"),
                                    rx.th("")
                                ),
                                # position="sticky",
                                # top="0px",
                            ),
                            rx.tbody(
                                rx.foreach(
                                    HistoryState.query_history_by_name,
                                    lambda item, index: rx.tr(
                                        rx.td(item.node_name),
                                        rx.td(item.node_version),
                                        rx.td(item.dataset),
                                        rx.td(item.items),
                                        rx.td(rx.checkbox(name=str(index), id=str(index), color_scheme="green",
                                                          on_change=lambda val: HistoryState.set_select_history_item(
                                                              index, val, item),
                                                          is_checked=HistoryState.selected_item_status.__getitem__(
                                                              item.id)
                                                          )
                                              ),
                                        rx.td(
                                            rx.button(
                                                rx.icon(tag="delete"), on_click=HistoryState.remove_history_item(item.id)
                                            )
                                        )
                                    )
                                ),
                                width="100%"
                            )
                        ),
                        overflow="auto",
                        maxHeight="33vh"
                    )
                ),
                allow_toggle=True,
                width="100%",
                # allow_multiple=True
            )
        ),
        check_alert(),
        overflow="auto",
        maxHeight="70vh"
    )


def run_result() -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.table(
                rx.thead(
                    rx.cond(
                        HistoryState.get_compare_num == 2,
                        rx.tr(
                            rx.th("input", w="4%"),
                            rx.th("output", w="38%"),
                            rx.th("score", w="5%"),
                            rx.th("output", w="38%"),
                            rx.th("score", w="5%")
                        )
                    ),
                    rx.cond(
                        HistoryState.get_compare_num == 1,
                        rx.tr(
                            rx.th("input", w="4%"),
                            rx.th("output", w="91%"),
                            rx.th("score", w="5%"),
                        )
                    ),

                ),
                rx.tbody(
                    rx.foreach(
                        HistoryState.query_history_result,
                        lambda item, index:
                            rx.cond(
                                HistoryState.get_compare_num == 2,
                                rx.tr(
                                    rx.td(
                                        rx.button(
                                            'show',
                                            on_click=HistoryState.show_input(
                                                index)
                                        )
                                    ),
                                    rx.td(item[0]['output']),
                                    rx.td(
                                        rx.radio_group(
                                            options,
                                            default_value=item[0]['score'],
                                            default_checked=True,
                                            on_change=lambda value: HistoryState.set_manual_score(
                                                0, index, value),

                                        )
                                    ),
                                    rx.td(item[1]['output']),
                                    rx.td(
                                        rx.radio_group(
                                            options,
                                            default_value=item[1]['score'],
                                            default_checked=True,
                                            on_change=lambda value: HistoryState.set_manual_score(
                                                1, index, value)
                                        )
                                    )
                                ),
                                rx.tr(
                                    rx.td(
                                        rx.button(
                                            'show',
                                            on_click=HistoryState.show_input(
                                                index)
                                        )
                                    ),
                                    rx.td(item[0]['output']),
                                    rx.td(
                                        rx.radio_group(
                                            options,
                                            default_value=item[0]['score'],
                                            default_checked=True,
                                            on_change=lambda value: HistoryState.set_manual_score(
                                                0, index, value)
                                            # rx.radio_group(
                                            #     rx.vstack(
                                            #         rx.foreach(
                                            #             options,
                                            #             lambda option: rx.radio(
                                            #                 option, custom_attrs={
                                            #                     "size": 'sm'}
                                            #             )
                                            #         )
                                            #     ),
                                            #     default_value=item[0]['score'],
                                            #     default_checked=True,
                                            #     on_change=lambda value: HistoryState.set_manual_score(
                                            #         0, index, value)
                                            # )
                                        )
                                    )
                                )
                            )
                    )
                ),
                w="100%"
            ),
            overflow="auto",
            h="60vh",
            w="100%"
        ),
        rx.cond(
            HistoryState.get_compare_num > 0,
            rx.box(
                rx.table(
                    rx.tbody(
                        rx.cond(
                            HistoryState.get_compare_num == 2,
                            rx.tr(
                                rx.td(rx.tooltip(rx.button(
                                    'average', on_click=HistoryState.save_avg), label="click to compute and save"), w="10%"),
                                rx.td('', w="32%"),
                                rx.td(
                                    HistoryState.compute_avgerage[0], w="5%"),
                                rx.td('', w="38%"),
                                rx.td(HistoryState.compute_avgerage[1], w="5%")
                            ),
                            rx.tr(
                                rx.td(rx.tooltip(rx.button(
                                    'average', on_click=HistoryState.save_avg), label="click to compute and save"), w="10%"),
                                rx.td('', w="85%"),
                                rx.td(
                                    HistoryState.compute_avgerage[0], w="5%"),
                                # position="sticky",
                                # bottom="0px",
                            )
                        )
                    ),
                    w="100%"
                ),
                w="100%"
            )
        ),
        w='100%'
    )


def check_alert() -> rx.Component:
    return rx.box(
        rx.alert_dialog(
            rx.alert_dialog_overlay(
                rx.alert_dialog_content(
                    rx.alert_dialog_header("Tip!"),
                    rx.alert_dialog_body(
                        "The maximum number of comparison currently supported is 2"
                    ),
                    rx.alert_dialog_footer(
                        rx.button(
                            "Close",
                            on_click=HistoryState.close_check_max_compare
                        )
                    )
                )
            ),
            is_open=HistoryState.check_max_compare,
            is_centered=True
        )
    )


def compare_alert() -> rx.Component:
    return rx.box(
        rx.alert_dialog(
            rx.alert_dialog_overlay(
                rx.alert_dialog_content(
                    rx.alert_dialog_header("Tip!"),
                    rx.alert_dialog_body(
                        "Selected nodes' result item number is inconsistent"
                    ),
                    rx.alert_dialog_footer(
                        rx.button(
                            "Close",
                            on_click=HistoryState.close_compare_error
                        )
                    )
                )
            ),
            is_open=HistoryState.compare_error,
            is_centered=True
        )
    )


def left_drawer() -> rx.Component:
    return rx.drawer(
        rx.drawer_overlay(
            rx.drawer_content(
                rx.drawer_header("Detial"),
                rx.drawer_body(
                    rx.hstack(
                        rx.foreach(
                            HistoryState.show_detial,
                            lambda item: rx.vstack(
                                rx.text('dataset', as_='b', width='100%'),
                                rx.divider(),
                                rx.code_block(
                                    item['dataset'][0],
                                    language="json",
                                    is_format=True
                                ),
                                rx.spacer(),
                                rx.text('prompt', as_='b', width='100%'),
                                rx.divider(),
                                rx.foreach(
                                    item['prompt'],
                                    lambda pitem: rx.vstack(
                                        rx.box(
                                            rx.text(pitem['role'], as_='b', width='100%'), width='100%'),
                                        rx.code_block(
                                            pitem['content'],
                                            is_format=True,
                                            wrap_long_lines=True,
                                            width='100%',
                                            textAlign=pitem['align']
                                        ),
                                        rx.box(h='1em'),
                                        textAlign=pitem['align']
                                    )
                                )
                            )
                        ),
                        rx.spacer()
                    )
                ),
                rx.drawer_footer(
                    rx.button("Close", on_click=HistoryState.drawer_close)
                )
            )
        ),
        is_open=HistoryState.detail_drawer,
        return_focus_on_close=True,
        on_close=HistoryState.drawer_close,
        placement='left',
        size='lg'
    )
