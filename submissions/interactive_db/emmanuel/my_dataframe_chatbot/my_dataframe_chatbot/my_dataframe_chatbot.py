import reflex as rx

from my_dataframe_chatbot import style
from my_dataframe_chatbot.state import State


def error_text() -> rx.Component:
    """return a text component to show error."""
    return rx.text(State.error_texts, text_align="center", font_weight="bold", color="red",)  


def head_text() -> rx.Component:
    """The header: return a text, text, divider"""
    return rx.vstack(
        rx.text("Chat with your data", font_size="2em", text_align="center", font_weight="bold", color="white",),
        rx.text("(Note: input your openai api key, upload your csv file then click submit to start chat)", 
                  text_align="center", color="white",),
        rx.divider(border_color="white"),
    )



def openai_key_input() -> rx.Component:
    """return a password component"""
    return rx.password(
            value=State.openai_api_key,
            placeholder="Enter your openai key",
            on_change=State.set_openai_api_key,
            style=style.openai_input_style,
    )


color = "rgb(107,99,246)"


def upload_csv():
    """The upload component."""
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Drag and drop files here or click to select files"
                ),
                ),
                multiple=False,
                accept = {
                    "text/csv": [".csv"],  # CSV format
                },
                max_files=1,
                border=f"1px dotted {color}",
                padding="2em",
                ),
                rx.hstack(rx.foreach(rx.selected_files, rx.text)),
                rx.button(
                    "Submit to start chat",
                    on_click=lambda: State.handle_upload(
                        rx.upload_files()
                    ),
                ),
                padding="2em",
            )


def confirm_upload() -> rx.Component:
    """text component to show upload confirmation."""
    return rx.text(State.upload_confirmation, text_align="center", font_weight="bold", color="green",)  


def qa(question: str, answer: str) -> rx.Component:
    """return the chat component."""
    return rx.box(
        rx.box(
            rx.text(question, text_align="right", color="black"),
            style=style.question_style,
        ),
        rx.box(
                rx.text(answer, text_align="left", color="black"),
                style=style.answer_style,
        ),
        margin_y="1em",
    )


def chat() -> rx.Component:
    """iterate over chat_history."""
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def loading_skeleton() -> rx.Component:
    """return the skeleton component."""
    return  rx.container(
                rx.skeleton_circle(
                            size="30px",
                            is_loaded=State.is_loaded_skeleton,
                            speed=1.5,
                            text_align="center",
                        ),  
                        display="flex",
                        justify_content="center",
                        align_items="center",
                    )



def action_bar() -> rx.Component:
    """return the chat input and ask button."""
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ask a question about your data",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),margin_top="3rem",
    )


def index() -> rx.Component:
    return rx.container(
        error_text(),
        head_text(),
        openai_key_input(),
        upload_csv(),
        confirm_upload(),
        chat(),
        loading_skeleton(),
        action_bar(),
    )


app = rx.App()
app.add_page(index)
app.compile()