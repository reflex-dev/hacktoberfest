"""
Main app script
"""
import reflex as rx

from .components.display import pane
from .views import *

from .state import *
from .constants import *

def index() -> rx.Component:
    return rx.container(
            rx.vstack(
                header_bar(),
                rx.flex(
                    rx.spacer(),
                    pane(library_view(), LIBRARY_PANE_HEADER_TEXT, padding=None),
                    rx.spacer(),
                    pane(recommendations_view(), RECOMMENDATIONS_PANE_HEADER_TEXT),
                    rx.spacer(),
                    pane(search_view(), SEARCH_PANE_HEADER_TEXT),
                    rx.spacer(),
                    width='100vw'
                ),

            ),
    )

app = rx.App()
app.add_page(index, on_load=State.on_load_library_fetch)
app.compile()
