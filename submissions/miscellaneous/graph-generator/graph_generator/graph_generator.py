"""Welcome to Reflex!."""

from graph_generator import styles

# Import all the pages.
from graph_generator.pages import *

import reflex as rx

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.compile()
