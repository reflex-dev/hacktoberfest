"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from LinguaFlex.state import TranslationState
import LinguaFlex.style as style
import reflex as rx
from LinguaFlex.constants import languages



def inputVertical() -> rx.Component:
    return rx.vstack(
        rx.card(
            rx.box(
                rx.hstack(
                    rx.select(
                        languages,
                        on_change=TranslationState.set_source_language,
                        value=TranslationState.source_language,
                        placeholder="Select a language",
                        style={
                            **style.select,
                            "color":rx.cond(rx.color_mode == "light", "black", "white"),
                            "border_color": rx.cond(rx.color_mode == "light", "black", "white")
                        }
                    ),
                ),
                rx.text_area(
                    placeholder="Enter text to translate",
                    on_change=TranslationState.set_input_text,
                    value=TranslationState.input_text,
                    style={
                        **style.text_area,
                        "color":rx.cond(rx.color_mode == "light", "black", "white"),
                        "border_color": rx.cond(rx.color_mode == "light", "black", "white"),
                    }
                ),
            ),
            header=rx.heading("Input Text:"),
            style=style.heading,
        ),
    )

def outputVertical() -> rx.Component:
    return rx.vstack(
        rx.card(
            rx.box(
                rx.hstack(
                    rx.select(
                        languages,
                        on_change=TranslationState.set_destination_language,
                        value=TranslationState.destination_language,
                        placeholder="Select a language",
                        style={
                            **style.select,
                            "color":rx.cond(rx.color_mode == "light", "black", "white"),
                            "border_color": rx.cond(rx.color_mode == "light", "black", "white"),
                        }
                    ),
                ),
                rx.text_area(
                    value=TranslationState.current_translation.translated_text,
                    style={
                        **style.text_area,
                        "color":rx.cond(rx.color_mode == "light", "black", "white"),
                        "border_color": rx.cond(rx.color_mode == "light", "black", "white"),
                    }
                ),
            ),
            header=rx.heading("Output Text:"),
            style=style.heading,
        )
    )


def structure() -> rx.Component:
    return rx.hstack(
        inputVertical(),
        rx.vstack(
            rx.image(
                src=TranslationState.image, 
                alt="=swap lang image",
                on_click=TranslationState.swap_languages,
                style=style.image_icon,
            ),
            rx.alert_dialog(
                rx.alert_dialog_overlay(
                    rx.alert_dialog_content(
                        rx.alert_dialog_header("Invalid input language"),
                        rx.alert_dialog_body(
                            "Please select a valid input language before swapping"
                        ),
                        rx.alert_dialog_footer(
                            rx.button(
                                "Close",
                                on_click=TranslationState.change,
                            )
                        ),
                    ),
                ),
                is_open=TranslationState.show,
            ),
            rx.button(
                "Translate", 
                on_click=TranslationState.translate,
                style=style.button,
            ),
        ),
        outputVertical(),
        style=style.structure,
    )


@rx.page(route="/", on_load=TranslationState.on_load)
def index() -> rx.Component:
    return rx.container(
        rx.box(
            rx.heading("LinguaFlex"),
            rx.text("Translate text between languages"),
            style=style.hero_banner_text,            
        ),
        rx.button(
            rx.icon(tag="moon"),
            on_click=rx.toggle_color_mode,
            style=style.border,
        ),
        structure(),
        style=style.index,
        center_content=True,
    )



# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()

