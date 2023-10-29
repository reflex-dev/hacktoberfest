from typing import List

"""The home page of the app."""

from graph_generator import styles
from graph_generator.templates import template

# from graph_generator.data import data

import reflex as rx

class FormState(rx.State):
    data = [
        {"age": 12, "weight": 45},
        {"age": 12, "weight": 45},
    ]

    # def change_value(self):
    #     self.data[0]["age"] =
    #     self.data[0]["weight"] =
    #     self.data[1]["age"] =
    #     self.data[1]["weight"] =

    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        # self.data = form_data
        self.data[0]["age"] = form_data["age1"]
        self.data[0]["weight"] = form_data["weight1"]
        self.data[1]["age"] = form_data["age2"]
        self.data[1]["weight"] = form_data["age3"]
        print(form_data["age1"])


@template(route="/", title="Home", image="/github.svg")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    # with open("README.md", encoding="utf-8") as readme:
    #     content = readme.read()
    return rx.vstack(
        rx.vstack(
            rx.heading("Graph Generator", font_size="3.5em"),
            background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
            background_clip="text",
            font_weight="bold",
            font_size="2em",
            text_align="center",
            width="1800px",
            margin_top="20px",
        ),
        rx.hstack(
            rx.form(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.input(placeholder="Age 1", id="age1", width="100px"),
                            rx.input(
                                placeholder="Weight 1", id="weight1", width="100px"
                            ),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Age 2", id="age2", width="100px"),
                            rx.input(
                                placeholder="Weight 2", id="weight2", width="100px"
                            ),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Age 3", id="age3", width="100px"),
                            rx.input(
                                placeholder="Weight 3", id="weight3", width="100px"
                            ),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Age 4", id="age4", width="100px"),
                            rx.input(
                                placeholder="Weight 4", id="weight4", width="100px"
                            ),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Age 5", id="age5", width="100px"),
                            rx.input(
                                placeholder="Weight 5", id="weight5", width="100px"
                            ),
                        ),
                    ),
                ),
                rx.button("Submit", type_="submit"),
                on_submit=FormState.handle_submit,
            ),
            rx.vstack(
                rx.recharts.bar_chart(
                    rx.recharts.bar(
                        data_key="weight", stroke="#8884d8", fill="#8884d8"
                    ),
                    rx.recharts.x_axis(data_key="age"),
                    rx.recharts.y_axis(),
                    data=FormState.data,
                ),
                width="800px",
            ),
        ),
    )
