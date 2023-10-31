import reflex as rx

# import State and style
from reflex_ocr_system.state import State
from reflex_ocr_system import style

# color for the upload component
color = "rgb(107,99,246)"


def index():
    """The main view."""
    return rx.vstack(
        rx.heading("OCR System - Extract text from Images",style=style.topic_style),
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Drag and drop files here or click to select files",
                    color="white",
                ),
            ),
            multiple=False,
            accept={
                "image/png": [".png"],
                "image/jpeg": [".jpg", ".jpeg"],
                "image/gif": [".gif"],
                "image/webp": [".webp"],
            },
            max_files=1,
            disabled=False,
            on_keyboard=True,
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(rx.foreach(rx.selected_files, rx.text,), color="white",),
        rx.button(
            "Click to Upload and Extract the text from selected Image",
            on_click=lambda: State.handle_upload(
                rx.upload_files()
            ),
            is_loading=State.is_loading,
            loading_text=State.loading_text,
            spinner_placement="start",
        ),
        rx.text(State.extracted_text_heading, text_align="center", font_weight="bold", color="white",),      
        rx.text(State.extracted_text, text_align="center",style=style.extracted_text_style),
    )

# Add state and page to the app.
app = rx.App(style=style.style)
app.add_page(index)
app.compile()