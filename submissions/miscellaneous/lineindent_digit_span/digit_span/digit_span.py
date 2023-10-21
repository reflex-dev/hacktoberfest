import reflex as rx
from .info import faq, how_to_play
from .style import css, brain
from .announcement import Announcement


class State(rx.State):
    pass


class Header(rx.Hstack):
    def __init__(self):
        super().__init__(style=css.get("header"))
        self.brain = rx.image(
            src="/brain.png",
            html_width="24px",
            html_height="24px",
            _dark={"filter": "brightness(0) invert(1)"},
            style=brain,
        )
        self.title = rx.heading(
            "Digit Span - Memory Test", size="md", font_weight="400"
        )

        self.theme = rx.color_mode_button(
            rx.color_mode_icon(),
            color_scheme="None",
            _dark={"color": "white"},
            _light={"color": "black"},
        )

        self.info = rx.popover(
            rx.color_mode_cond(
                light=rx.popover_trigger(rx.icon(tag="info_outline", cursor="pointer")),
                dark=rx.popover_trigger(rx.icon(tag="info", cursor="pointer")),
            ),
            rx.popover_content(
                rx.popover_body(
                    rx.markdown(how_to_play),
                    box_shadow="0px 10px 20px 0px rgba(0, 0, 0, 0.35)",
                    border="none",
                ),
                rx.popover_close_button(),
            ),
        )

        self.children = [self.brain, self.title, rx.spacer(), self.info, self.theme]


class GameButton(rx.Button):
    def __init__(self, idx: str, image_path: str, func: callable):
        super().__init__(id=idx, padding="0", color_scheme="None", on_click=func)
        self.image = rx.image(
            src=image_path,
            html_width="32px",
            html_height="32px",
            _dark={"filter": "brightness(0) invert(1)"},
        )

        self.children = [self.image]


class Footer(rx.Hstack):
    def __init__(self):
        super().__init__(style=css.get("footer"))
        self.attributes = rx.text(
            "Copyright © 2023 S. Ahmad P. Hakimi",
            font_size=["13px", "14px", "14px", "14px", "14px"],
            transition="all 550ms ease",
        )
        self.faq = rx.link(
            "FAQ", href="/faq", _hover={"text_decoration": "None"}, padding="0 0.35rem"
        )
        self.game = rx.link(
            "Game", href="/", _hover={"text_decoration": "None"}, padding="0 0.35rem"
        )

        self.git = rx.link(
            "GitHub",
            href="https://github.com/LineIndent",
            _hover={"text_decoration": "None"},
            padding="0 0.35rem",
        )

        self.children = [self.attributes, rx.spacer(), self.game, self.faq, self.git]


@rx.page(title="Digit Span Game")
def index() -> rx.Component:
    header: rx.Hstack = Header()
    footer: rx.Hstack = Footer()
    announcement = Announcement()

    return rx.vstack(
        announcement,
        header,
        rx.vstack(
            rx.script(src="/numbers.js"),
            rx.divider(height="5em", border_color="transparent"),
            rx.hstack(
                rx.heading(
                    id="digit",
                    font_size="105px",
                    text_align="center",
                ),
                style=css.get("number"),
            ),
            rx.divider(height="3.5em", border_color="transparent"),
            rx.hstack(
                GameButton("start", "/play.png", rx.client_side("startNewLevel(args)")),
                GameButton(
                    "check", "/check.png", rx.client_side("checkUserSequence(args)")
                ),
            ),
            rx.divider(height="0.5em", border_color="transparent"),
            rx.hstack(
                rx.input(
                    id="userSequence",
                    height="70px",
                    font_size="50px",
                    text_align="center",
                    transition="all 550ms ease",
                    letter_spacing="0.25rem",
                ),
                width="100%",
                height="70px",
                align_items="center",
                justify_content="center",
                padding=["0 1rem", "0 1rem", "0 3rem", "0 15rem", "0 30rem"],
            ),
            rx.divider(height="0.5em", border_color="transparent"),
            rx.hstack(
                rx.text("Lives: ", rx.span("3", id="lives"), font_size="19px"),
                rx.text("Level: ", rx.span("1", id="level"), font_size="19px"),
                spacing="4rem",
            ),
            rx.text(id="result", text_align="center", padding="1rem 1rem"),
            rx.spacer(),
            style=css.get("content"),
        ),
        footer,
        spacing="0",
        width="100%",
        height="100vh",
    )


@rx.page(route="/faq", title="Frequently Asked Questions")
def faqs():
    header: rx.Hstack = Header()
    footer: rx.Hstack = Footer()
    return rx.vstack(
        header,
        rx.vstack(
            rx.heading("FAQs: Digit Span Test", size="lg"),
            rx.divider(height="2em", border_color="transparent"),
            rx.markdown(faq),
            style=css.get("content"),
            align_items="start",
            padding=[
                "3rem 1.5rem",
                "3rem 1.5rem",
                "3rem 1.5rem",
                "3rem 10rem",
                "3rem 20rem",
            ],
            transition="all 550ms ease",
            overflow="auto",
        ),
        footer,
        spacing="0",
        width="100%",
        height="100vh",
    )


app = rx.App(style=css)
app.add_page(index)
app.compile()
