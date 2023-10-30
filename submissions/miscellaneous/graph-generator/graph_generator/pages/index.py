from typing import List

"""The home page of the app."""

from graph_generator import styles
from graph_generator.templates import template

# from graph_generator.data import data

import reflex as rx


class FormState(rx.State):
    data = [
        {
            "age": 12,
            "weight": 145,
            "name": "A",
            "value": 500,
            "fill": "#8884d8",
            "pv": 2400,
            "uv": 2400,
        },
        {
            "age": 13,
            "weight": 5,
            "name": "B",
            "value": 400,
            "fill": "#83a6ed",
            "pv": 1398,
            "uv": 2210,
        },
        {
            "age": 11,
            "weight": 55,
            "name": "C",
            "value": 100,
            "fill": "#8dd1e1",
            "pv": 9800,
            "uv": 2290,
        },
        {
            "age": 1,
            "weight": 21,
            "name": "D",
            "value": 10,
            "fill": "#82ca9d",
            "pv": 3908,
            "uv": 2000,
        },
        {
            "age": 82,
            "weight": 79,
            "name": "E",
            "value": 210,
            "fill": "#a4de6c",
            "pv": 4800,
            "uv": 2181,
        },
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
        self.data[1]["weight"] = form_data["weight2"]

    def handle_submit_row2(self, form_data: dict):
        self.data[0]["value"] = form_data["quantity1"]
        self.data[1]["value"] = form_data["quantity2"]
        self.data[2]["value"] = form_data["quantity3"]
        self.data[3]["value"] = form_data["quantity4"]
        self.data[4]["value"] = form_data["quantity5"]

    def handle_submit_row3(self, form_data: dict):
        self.data[0]["uv"] = form_data["uv1"]
        self.data[0]["pv"] = form_data["pv1"]
        self.data[1]["uv"] = form_data["uv2"]
        self.data[1]["pv"] = form_data["pv2"]
        self.data[2]["uv"] = form_data["uv3"]
        self.data[2]["pv"] = form_data["pv3"]
        self.data[3]["uv"] = form_data["uv4"]
        self.data[3]["pv"] = form_data["pv4"]
        self.data[4]["uv"] = form_data["uv5"]
        self.data[4]["pv"] = form_data["pv5"]


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
            rx.heading("Play with Graphs", font_size="3.5em"),
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
                    rx.text("Age Vs Weight Graph", font_size="1.5em"),
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
                        margin_top="35px",
                    ),
                    rx.button("Submit", type_="submit"),
                ),
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
                height="400px",
            ),
        ),
        # 3rd row
        rx.hstack(
            rx.form(
                rx.vstack(
                    rx.text("Green and Violet Graph", font_size="1.5em"),
                    rx.hstack(
                        rx.vstack(
                            rx.input(placeholder="Green 1", id="uv1", width="100px"),
                            rx.input(placeholder="Violet 1", id="pv1", width="100px"),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Green 2", id="uv2", width="100px"),
                            rx.input(placeholder="Violet 2", id="pv2", width="100px"),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Green 3", id="uv3", width="100px"),
                            rx.input(placeholder="Violet 3", id="pv3", width="100px"),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Green 4", id="uv4", width="100px"),
                            rx.input(placeholder="Violet 4", id="pv4", width="100px"),
                        ),
                        rx.vstack(
                            rx.input(placeholder="Green 5", id="uv5", width="100px"),
                            rx.input(placeholder="Vioet 5", id="pv5", width="100px"),
                        ),
                        margin_top="35px",
                    ),
                    rx.button("Submit", type_="submit"),
                ),
                on_submit=FormState.handle_submit_row3,
            ),
            rx.vstack(
                rx.recharts.line_chart(
                    rx.recharts.line(
                        data_key="pv",
                        stroke="#8884d8",
                    ),
                    rx.recharts.line(
                        data_key="uv",
                        stroke="#82ca9d",
                    ),
                    rx.recharts.x_axis(data_key="name"),
                    rx.recharts.y_axis(),
                    data=FormState.data,
                ),
                width="800px",
                height="400px",
            ),
        ),
        rx.hstack(
            rx.form(
                rx.vstack(
                    rx.text("Product A, B, C, ... and its quantity", font_size="1.5em"),
                    rx.hstack(
                        rx.vstack(
                            rx.input(
                                placeholder="Quantity for A",
                                id="quantity1",
                                width="150px",
                            ),
                        ),
                        rx.vstack(
                            rx.input(
                                placeholder="Quantity for B",
                                id="quantity2",
                                width="150px",
                            ),
                        ),
                        rx.vstack(
                            rx.input(
                                placeholder="Quantity for C",
                                id="quantity3",
                                width="150px",
                            ),
                        ),
                        rx.vstack(
                            rx.input(
                                placeholder="Quantity for D",
                                id="quantity4",
                                width="150px",
                            ),
                        ),
                        rx.vstack(
                            rx.input(
                                placeholder="Quantity for E",
                                id="quantity5",
                                width="150px",
                            ),
                        ),
                    ),
                    rx.button("Submit", type_="submit"),
                ),
                on_submit=FormState.handle_submit_row2,
            ),
            rx.vstack(
                rx.recharts.funnel_chart(
                    rx.recharts.funnel(
                        rx.recharts.label_list(
                            position="right",
                            data_key="name",
                            fill="#000",
                            stroke="none",
                        ),
                        rx.recharts.label_list(
                            position="right",
                            data_key="name",
                            fill="#000",
                            stroke="none",
                        ),
                        data_key="value",
                        data=FormState.data,
                    ),
                    rx.recharts.graphing_tooltip(),
                    width=730,
                    height=250,
                ),
                width="800px",
                height="400px",
            ),
        ),
    )
