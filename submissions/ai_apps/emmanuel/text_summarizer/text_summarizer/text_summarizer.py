import reflex as rx

# import State and style
from text_summarizer.state import State
from text_summarizer import style


def full_text() -> rx.Component:
    """return a vertical component of heading and text_area."""
    return rx.vstack(
        rx.heading("Text Summarizer",style=style.topic_style),
        rx.text_area(
            value=State.large_text,
            placeholder="Enter your full text here",
            on_change=State.set_large_text,
            style=style.textarea_style,
        ),
    )


def openai_key_input() -> rx.Component:
    """return a password component"""
    return rx.password(
            value=State.openai_api_key,
            placeholder="Enter your openai key",
            on_change=State.set_openai_api_key,
            style=style.openai_input_style,
    )


def submit_button() -> rx.Component:
    """return a button."""
    return rx.button(
        "Summarize text",
        on_click=State.start_process,
        is_loading=State.is_loading,
        loading_text=State.loading_text,
        spinner_placement="start",
        style=style.submit_button_style,
    )


def summary_output() -> rx.Component:
    """return summary."""
    return rx.box(
            rx.text(State.summary, text_align="center"),
            style=style.summary_style,
    )


def index() -> rx.Component:
    """return a full_text, openai_key_input, submit_button, summary_output respectively."""
    return rx.container(
        full_text(),
        openai_key_input(),
        submit_button(),
        summary_output(),
    )

# Add state and page to the app.
app = rx.App(style=style.style)
app.add_page(index)
app.compile()